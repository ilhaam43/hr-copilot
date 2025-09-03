# PROSEDUR KLASIFIKASI DATA SENSITIF PERUSAHAAN
## Dengan Tingkat Keamanan dan Penanganan Khusus

---

## 1. DASAR HUKUM DAN STANDAR

### 1.1 Peraturan Perundang-undangan
- **Undang-Undang Nomor 27 Tahun 2022** tentang Perlindungan Data Pribadi
- **Undang-Undang Nomor 19 Tahun 2016** tentang Perubahan atas UU ITE
- **Peraturan Pemerintah Nomor 71 Tahun 2019** tentang Penyelenggaraan Sistem dan Transaksi Elektronik
- **Peraturan Bank Indonesia** tentang Penerapan Manajemen Risiko dalam Penggunaan Teknologi Informasi

### 1.2 Standar Internasional
- **ISO/IEC 27001:2013** - Information Security Management Systems
- **ISO/IEC 27018:2019** - Code of Practice for Protection of PII in Public Clouds
- **NIST SP 800-60** - Guide for Mapping Types of Information and Information Systems to Security Categories
- **COBIT 2019** - Framework for Information and Technology Governance

### 1.3 Framework Klasifikasi
- **TLP (Traffic Light Protocol)** untuk sharing information
- **NATO Classification System** sebagai referensi
- **US Government Classification Standards** untuk best practices

---

## 2. RUANG LINGKUP PENERAPAN

### 2.1 Jenis Data yang Diklasifikasi
#### 2.1.1 Data Pribadi
- Data identitas personal
- Data kontak dan komunikasi
- Data keluarga dan dependents
- Data kesehatan dan medis
- Data keuangan personal
- Data biometrik

#### 2.1.2 Data Perusahaan
- Informasi strategis dan business plan
- Data keuangan perusahaan
- Intellectual property dan trade secrets
- Data pelanggan dan partner
- Informasi teknis dan sistem
- Data operasional dan proses bisnis

#### 2.1.3 Data Sistem dan Infrastruktur
- Konfigurasi sistem dan network
- Credentials dan authentication data
- Log files dan audit trails
- Backup dan recovery data
- Security policies dan procedures

### 2.2 Media dan Format Data
- **Digital**: Database, files, emails, cloud storage
- **Physical**: Dokumen cetak, CD/DVD, USB drives
- **Verbal**: Presentasi, meeting, phone calls
- **Visual**: Whiteboard, projector displays, screens

### 2.3 Lifecycle Data
- **Creation**: Saat data dibuat atau diterima
- **Processing**: Selama pengolahan dan analisis
- **Storage**: Penyimpanan jangka pendek dan panjang
- **Transmission**: Transfer internal dan eksternal
- **Archival**: Penyimpanan jangka panjang
- **Disposal**: Penghapusan dan pemusnahan

---

## 3. TINGKAT KLASIFIKASI DATA

### 3.1 Level 1: PUBLIC (Publik)

#### 3.1.1 Definisi
Informasi yang dapat diakses oleh publik tanpa risiko terhadap perusahaan, karyawan, atau stakeholder.

#### 3.1.2 Contoh Data
- Informasi perusahaan di website resmi
- Press release dan pengumuman publik
- Brosur marketing dan promotional materials
- Job posting dan career information
- Annual report yang dipublikasikan
- Contact information perusahaan

#### 3.1.3 Kriteria Klasifikasi
- Tidak ada dampak negatif jika dipublikasikan
- Sudah tersedia di domain publik
- Tidak mengandung informasi sensitif
- Tidak melanggar privacy atau confidentiality

#### 3.1.4 Kontrol Keamanan
- **Akses**: Tidak ada pembatasan khusus
- **Penyimpanan**: Standard file storage
- **Transmisi**: Email biasa, website, media sosial
- **Marking**: Label "PUBLIC" (opsional)
- **Disposal**: Standard deletion procedures

### 3.2 Level 2: INTERNAL (Internal)

#### 3.2.1 Definisi
Informasi yang ditujukan untuk penggunaan internal perusahaan dan dapat menyebabkan kerugian minor jika diakses oleh pihak yang tidak berwenang.

#### 3.2.2 Contoh Data
- Internal policies dan procedures
- Organizational chart dan struktur internal
- Training materials dan handbook
- Internal newsletter dan komunikasi
- Non-sensitive employee information
- Vendor contact information

#### 3.2.3 Kriteria Klasifikasi
- Dampak rendah jika terjadi unauthorized disclosure
- Informasi operasional sehari-hari
- Tidak mengandung data pribadi sensitif
- Tidak mempengaruhi competitive advantage

#### 3.2.4 Kontrol Keamanan
- **Akses**: Karyawan dan authorized contractors
- **Penyimpanan**: Corporate network dengan basic access control
- **Transmisi**: Corporate email, secure file sharing
- **Marking**: Label "INTERNAL" pada dokumen
- **Disposal**: Secure deletion, paper shredding

### 3.3 Level 3: CONFIDENTIAL (Rahasia)

#### 3.3.1 Definisi
Informasi sensitif yang dapat menyebabkan kerugian signifikan terhadap perusahaan, karyawan, atau stakeholder jika diakses oleh pihak yang tidak berwenang.

#### 3.3.2 Contoh Data
- Data pribadi karyawan (salary, performance)
- Customer data dan contact information
- Financial reports dan budget information
- Contract dan agreement details
- Strategic planning documents
- Vendor dan supplier information
- HR investigation reports

#### 3.3.3 Kriteria Klasifikasi
- Dampak sedang hingga tinggi jika terjadi breach
- Mengandung data pribadi atau business sensitive
- Dapat mempengaruhi competitive position
- Terikat oleh confidentiality agreements

#### 3.3.4 Kontrol Keamanan
- **Akses**: Need-to-know basis, role-based access
- **Penyimpanan**: Encrypted storage, access logging
- **Transmisi**: Encrypted email, secure file transfer
- **Marking**: Label "CONFIDENTIAL" wajib
- **Disposal**: Certified destruction, crypto-shredding

### 3.4 Level 4: RESTRICTED (Sangat Rahasia)

#### 3.4.1 Definisi
Informasi yang sangat sensitif dan dapat menyebabkan kerugian berat atau catastrophic terhadap perusahaan jika diakses oleh pihak yang tidak berwenang.

#### 3.4.2 Contoh Data
- Trade secrets dan intellectual property
- M&A information dan strategic initiatives
- Executive compensation dan board materials
- Security vulnerabilities dan incident reports
- Regulatory investigation materials
- Biometric data dan health records
- Financial fraud investigation
- Legal litigation documents

#### 3.4.3 Kriteria Klasifikasi
- Dampak severe atau catastrophic jika terjadi breach
- Critical untuk business continuity
- Regulated data dengan strict compliance requirements
- Dapat menyebabkan legal liability

#### 3.4.4 Kontrol Keamanan
- **Akses**: Explicit authorization, dual approval
- **Penyimpanan**: High-grade encryption, HSM, air-gapped systems
- **Transmisi**: End-to-end encryption, secure courier
- **Marking**: Label "RESTRICTED" dengan handling instructions
- **Disposal**: Witnessed destruction, certificate of destruction

---

## 4. PROSEDUR OPERASIONAL STANDAR (SOP)

### 4.1 Proses Klasifikasi Data

#### 4.1.1 Identifikasi dan Assessment
**Step 1: Data Discovery**
1. Inventory semua data assets
2. Identify data sources dan repositories
3. Map data flows dan processing activities
4. Document data lineage dan dependencies

**Step 2: Impact Assessment**
1. Evaluate potential impact of unauthorized disclosure
2. Consider regulatory dan compliance requirements
3. Assess business dan operational risks
4. Review contractual obligations

**Step 3: Classification Decision**
1. Apply classification criteria
2. Consider aggregation effects
3. Document classification rationale
4. Obtain stakeholder approval

#### 4.1.2 Classification Matrix

| Kriteria | PUBLIC | INTERNAL | CONFIDENTIAL | RESTRICTED |
|----------|---------|-----------|--------------|------------|
| **Business Impact** | None | Low | Medium-High | Severe |
| **Legal Impact** | None | Minimal | Moderate | High |
| **Regulatory Impact** | None | Low | Medium | High |
| **Reputational Impact** | None | Minor | Moderate | Major |
| **Financial Impact** | None | <$100K | $100K-$1M | >$1M |
| **Operational Impact** | None | Minor | Moderate | Critical |

#### 4.1.3 Automated Classification
**Data Loss Prevention (DLP) Rules:**
- Pattern matching untuk PII (KTP, phone numbers)
- Keyword detection untuk sensitive terms
- Machine learning untuk content analysis
- Regular expression untuk structured data

**Classification Tools:**
- Microsoft Purview Information Protection
- Symantec Data Loss Prevention
- Forcepoint DLP
- Custom classification engines

### 4.2 Handling Procedures per Classification

#### 4.2.1 Marking dan Labeling
**Digital Documents:**
```
CLASSIFICATION: [LEVEL]
HANDLING: [INSTRUCTIONS]
CREATED: [DATE]
OWNER: [DEPARTMENT/PERSON]
REVIEW DATE: [DATE]
```

**Physical Documents:**
- Header dan footer marking
- Color-coded labels atau stamps
- Watermarks untuk sensitive documents
- Envelope marking untuk mailed documents

#### 4.2.2 Storage Requirements

**PUBLIC Data:**
- Standard file systems
- Cloud storage (public cloud OK)
- No encryption required
- Standard backup procedures

**INTERNAL Data:**
- Corporate network storage
- Access controls implemented
- Basic encryption recommended
- Regular backup dan retention

**CONFIDENTIAL Data:**
- Encrypted storage mandatory
- Access logging enabled
- Private cloud atau on-premises
- Secure backup dengan encryption

**RESTRICTED Data:**
- High-grade encryption (AES-256)
- Hardware Security Module (HSM)
- Air-gapped systems untuk critical data
- Immutable backup dengan versioning

#### 4.2.3 Transmission Procedures

**Email Security:**
- PUBLIC: Standard email
- INTERNAL: Corporate email dengan basic security
- CONFIDENTIAL: Encrypted email (S/MIME atau PGP)
- RESTRICTED: Secure messaging platform atau encrypted file transfer

**File Transfer:**
- PUBLIC: Standard file sharing
- INTERNAL: Corporate file sharing platform
- CONFIDENTIAL: Secure file transfer protocol (SFTP)
- RESTRICTED: Dedicated secure transfer solution

**Physical Transfer:**
- CONFIDENTIAL: Sealed envelope, registered mail
- RESTRICTED: Secure courier, chain of custody documentation

### 4.3 Access Control Implementation

#### 4.3.1 Role-Based Access Control (RBAC)
**Access Levels:**
- **Read Only**: View access untuk authorized users
- **Read/Write**: Modify access untuk data owners
- **Admin**: Full control untuk data stewards
- **Audit**: Read-only access untuk compliance team

**Approval Workflow:**
- INTERNAL: Manager approval
- CONFIDENTIAL: Department head approval
- RESTRICTED: Executive approval + security review

#### 4.3.2 Attribute-Based Access Control (ABAC)
**Attributes Considered:**
- User role dan department
- Data classification level
- Time dan location of access
- Device dan network security posture
- Business justification

### 4.4 Data Lifecycle Management

#### 4.4.1 Retention Policies

| Classification | Retention Period | Review Frequency |
|----------------|------------------|------------------|
| PUBLIC | As needed | Annual |
| INTERNAL | 7 years | Annual |
| CONFIDENTIAL | 10 years | Semi-annual |
| RESTRICTED | 15 years atau permanent | Quarterly |

#### 4.4.2 Disposal Procedures

**Digital Data Disposal:**
- PUBLIC: Standard deletion
- INTERNAL: Secure deletion (3-pass overwrite)
- CONFIDENTIAL: Cryptographic erasure
- RESTRICTED: Physical destruction of storage media

**Physical Data Disposal:**
- INTERNAL: Cross-cut shredding
- CONFIDENTIAL: Micro-cut shredding
- RESTRICTED: Incineration atau pulverization

---

## 5. MEKANISME PENGAWASAN DAN EVALUASI

### 5.1 Monitoring dan Compliance

#### 5.1.1 Data Classification Metrics
**Key Performance Indicators:**
- Percentage of data classified
- Classification accuracy rate
- Time to classify new data
- Number of misclassification incidents
- Compliance dengan handling procedures

#### 5.1.2 Automated Monitoring
**DLP Monitoring:**
- Real-time monitoring untuk policy violations
- Automated alerts untuk suspicious activities
- User behavior analytics
- Data movement tracking

**Access Monitoring:**
- Privileged access monitoring
- Unusual access pattern detection
- Failed access attempt analysis
- Regular access certification

### 5.2 Audit dan Assessment

#### 5.2.1 Internal Audit Schedule
- **Monthly**: DLP policy effectiveness review
- **Quarterly**: Classification accuracy assessment
- **Semi-Annual**: Access rights review
- **Annual**: Comprehensive data governance audit

#### 5.2.2 External Assessment
- Third-party data governance maturity assessment
- Regulatory compliance audit
- Penetration testing untuk data protection controls
- Vendor security assessment

### 5.3 Incident Management

#### 5.3.1 Classification Incidents
**Types of Incidents:**
- Misclassification of sensitive data
- Unauthorized access to classified data
- Improper handling atau transmission
- Data leakage atau breach

#### 5.3.2 Incident Response
1. **Detection**: Automated alerts atau manual reporting
2. **Assessment**: Impact analysis dan classification review
3. **Containment**: Immediate protective measures
4. **Investigation**: Root cause analysis
5. **Remediation**: Corrective actions implementation
6. **Lessons Learned**: Process improvement

### 5.4 Continuous Improvement

#### 5.4.1 Regular Review Process
**Classification Review Triggers:**
- Regulatory changes
- Business process changes
- Technology updates
- Security incidents
- Audit findings

#### 5.4.2 Training dan Awareness
**Training Program:**
- Data classification awareness untuk all employees
- Specialized training untuk data handlers
- Regular refresher training
- Incident-based training updates

---

## 6. ROLES DAN RESPONSIBILITIES

### 6.1 Data Governance Roles

#### 6.1.1 Data Protection Officer (DPO)
**Responsibilities:**
- Overall data classification program oversight
- Policy development dan maintenance
- Regulatory compliance monitoring
- Incident response coordination

#### 6.1.2 Data Owners
**Responsibilities:**
- Initial data classification decisions
- Access authorization
- Data quality dan accuracy
- Retention dan disposal decisions

#### 6.1.3 Data Stewards
**Responsibilities:**
- Day-to-day data management
- Classification implementation
- Access control administration
- Monitoring dan reporting

#### 6.1.4 Data Users
**Responsibilities:**
- Comply dengan handling procedures
- Report classification issues
- Protect data according to classification
- Complete required training

### 6.2 IT Security Roles

#### 6.2.1 Information Security Officer
**Responsibilities:**
- Technical control implementation
- Security monitoring dan analysis
- Vulnerability assessment
- Incident response support

#### 6.2.2 System Administrators
**Responsibilities:**
- Access control configuration
- System security hardening
- Backup dan recovery procedures
- Audit log management

---

## 7. SANKSI DAN KONSEKUENSI

### 7.1 Internal Sanctions
**Violation Categories:**
- **Minor**: Incorrect labeling, minor handling errors
- **Moderate**: Unauthorized sharing, access violations
- **Major**: Intentional misclassification, data theft
- **Critical**: Malicious data exfiltration, sabotage

**Disciplinary Actions:**
- Minor: Verbal warning + additional training
- Moderate: Written warning + performance improvement plan
- Major: Suspension + formal investigation
- Critical: Termination + legal action

### 7.2 Legal dan Regulatory Consequences
**Potential Penalties:**
- Administrative fines (UU PDP): Up to Rp 50 billion
- Criminal penalties (UU ITE): Up to 12 years imprisonment
- Civil lawsuits dari affected parties
- Regulatory sanctions dan license revocation

---

**Dokumen ini berlaku efektif sejak: [Tanggal Implementasi]**
**Versi: 1.0**
**Pemilik Dokumen: Data Protection Officer**
**Review Berikutnya: [Tanggal + 6 bulan]**