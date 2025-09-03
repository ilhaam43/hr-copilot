import os, uuid, re, io, requests
from typing import List
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from pypdf import PdfReader

# ==== Konfigurasi ====
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLL = os.getenv("QDRANT_COLLECTION", "hr_policies")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")
GEN_MODEL = os.getenv("GEN_MODEL", "llama3.2:3b-instruct")  # SLM default
PRESIDIO_URL = os.getenv("PRESIDIO_URL", "http://localhost:3000")
MASK_FOR_RETRIEVAL = os.getenv("MASK_FOR_RETRIEVAL", "true").lower() == "true"
MIN_SIM = float(os.getenv("MIN_SIM", "0.28"))
MAX_CHUNK = int(os.getenv("MAX_CHUNK", "900"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))

HORILLA_BASE_URL = os.getenv("HORILLA_BASE_URL", "http://localhost:8000")
HORILLA_API_TOKEN = os.getenv("HORILLA_API_TOKEN", "")

TOPIC_DENYLIST = re.compile(r"(password|kata\s?sandi|otp|nik|npwp|rekening|gaji\s*perorangan|slip gaji pribadi)", re.I)

# ==== App & Qdrant ====
app = FastAPI(title="HR Copilot (RAG + PII + Guardrails + Horilla Bridge)")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
qdrant = QdrantClient(url=QDRANT_URL)
def ensure_collection():
    names = [c.name for c in qdrant.get_collections().collections]
    if COLL not in names:
        qdrant.recreate_collection(COLL, vectors_config=VectorParams(size=768, distance=Distance.COSINE))
ensure_collection()

# ==== Ollama ====
def embed(text: str) -> List[float]:
    r = requests.post("http://localhost:11434/api/embeddings",
                      json={"model": EMBED_MODEL, "input": text}, timeout=60)
    r.raise_for_status()
    return r.json()["embedding"]

def generate(prompt: str) -> str:
    r = requests.post("http://localhost:11434/api/generate",
                      json={"model": GEN_MODEL, "prompt": prompt, "stream": False}, timeout=120)
    r.raise_for_status()
    return r.json()["response"]

# ==== PII masking ====
# Gunakan format string list (sesuai API Presidio)
DEFAULT_ENTITIES = ["EMAIL_ADDRESS","PHONE_NUMBER","PERSON","CREDIT_CARD","IBAN_CODE"]

def mask_with_spans(text, spans, fmt="[REDACTED:{t}]"):
    spans_sorted = sorted(spans, key=lambda s: s["start"], reverse=True)
    for s in spans_sorted:
        text = text[:s["start"]] + fmt.format(t=s.get("entity_type","PII")) + text[s["end"]:]
    return text

def presidio_mask(text: str):
    try:
        r = requests.post(f"{PRESIDIO_URL.rstrip('/')}/analyze",
                          json={"text": text, "language": "en", "entities": DEFAULT_ENTITIES}, timeout=10)
        if r.ok:
            return mask_with_spans(text, r.json())
    except Exception:
        pass
    return None

EMAIL_RE = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
PHONE_RE = re.compile(r"(?:\+62|62|0)8[1-9][0-9]{6,11}")
def regex_mask(t: str)->str: return PHONE_RE.sub("[REDACTED:PHONE]", EMAIL_RE.sub("[REDACTED:EMAIL]", t))
def mask_pii(t: str)->str: return t if not t else (presidio_mask(t) or regex_mask(t))

# ==== Util ====
def chunk_text(s: str, n=900, overlap=150):
    i=0; L=len(s)
    while i<L:
        j=min(i+n,L); yield s[i:j]; i=j-overlap
def pdf_to_text(b: bytes)->str:
    r=PdfReader(io.BytesIO(b)); return "\n".join((p.extract_text() or "") for p in r.pages)

# ==== Schemas ====
class IngestDoc(BaseModel): id:str; text:str; source:str
class IngestReq(BaseModel): docs:list[IngestDoc]
class AskReq(BaseModel): q:str; k:int=5
class LeaveBalanceReq(BaseModel): employee_id:str

# ==== Endpoints: ingest ====
@app.post("/ingest")
def ingest(req: IngestReq):
    pts=[]
    for d in req.docs:
        t=mask_pii(d.text); v=embed(t)
        pts.append(PointStruct(id=str(uuid.uuid4()), vector=v, payload={"id":d.id,"text":t,"source":d.source}))
    if pts: qdrant.upsert(collection_name=COLL, points=pts)
    return {"ok":True,"count":len(pts)}

@app.post("/ingest/upload")
async def ingest_upload(file: UploadFile=File(...), source: str=Form(None)):
    raw = (pdf_to_text(await file.read()) if file.filename.lower().endswith(".pdf")
           else (await file.read()).decode("utf-8","ignore") if file.filename.lower().endswith(".txt")
           else None)
    if raw is None: return {"ok":False,"error":"Gunakan PDF atau TXT."}
    safe=mask_pii(raw); pts=[]; src=source or file.filename
    for i,ch in enumerate(chunk_text(safe)):
        v=embed(ch)
        pts.append(PointStruct(id=str(uuid.uuid4()), vector=v, payload={"id":f"{file.filename}#{i}","text":ch,"source":f"{src}#{i}"}))
    if pts: qdrant.upsert(collection_name=COLL, points=pts)
    return {"ok":True,"file":file.filename,"chunks":len(pts)}

# ==== Endpoints: ask (guardrails) ====
@app.post("/ask")
def ask(req: AskReq):
    if TOPIC_DENYLIST.search(req.q or ""):
        return {"answer":"Maaf, topik sensitif tersebut tidak bisa dibantu. Hubungi HR.","citations":[]}
    q = mask_pii(req.q) if MASK_FOR_RETRIEVAL else req.q
    hits = qdrant.search(collection_name=COLL, query_vector=embed(q), limit=req.k)
    if not hits: return {"answer":"Maaf, belum ada dasar kebijakan untuk pertanyaan itu.","citations":[]}
    best=max(hits,key=lambda h:h.score)
    if best.score < MIN_SIM:
        return {"answer":"Maaf, referensi kebijakan belum cukup relevan. Mohon perjelas/cek HR.","citations":[]}
    ctx=[]; 
    for i,h in enumerate(hits,1):
        p=h.payload; ctx.append(f"[{i}] ({p.get('source','')}) {p['text']}")
    prompt=("Anda asisten kebijakan HR. Jawab hanya dari Konteks. "
            "Jika tidak cukup bukti, katakan tidak cukup. Sertakan sitasi [1],[2].\n\n"
            f"Pertanyaan: {mask_pii(req.q)}\n\nKonteks:\n" + "\n\n".join(ctx))
    return {"answer": generate(prompt), "citations": [h.payload.get("source","") for h in hits]}

# ==== Horilla bridge (opsional) ====
def hget(path:str):
    url=f"{HORILLA_BASE_URL.rstrip('/')}{path}"; hdrs={}
    if HORILLA_API_TOKEN: hdrs["Authorization"]=f"Bearer {HORILLA_API_TOKEN}"
    r=requests.get(url,headers=hdrs,timeout=15); r.raise_for_status(); return r.json()

@app.post("/bridge/leave_balance")
def bridge_leave_balance(req: LeaveBalanceReq):
    last=""
    for path in (f"/api/leave/balance/{req.employee_id}", f"/api/v1/leave/balance/{req.employee_id}"):
        try:
            data=hget(path); bal=data.get("balance") or data.get("remaining") or data
            return {"ok":True,"employee_id":req.employee_id,"balance":bal,"source":path}
        except Exception as e:
            last=str(e)
    return {"ok":False,"error":"Gagal panggil API Horilla. Cek token/endpoint.","details":last}

@app.get("/healthz")
def healthz(): return {"status":"ok","qdrant":QDRANT_URL,"model":GEN_MODEL,"min_sim":MIN_SIM}
