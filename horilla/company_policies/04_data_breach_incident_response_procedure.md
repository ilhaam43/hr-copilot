# PROSEDUR PENANGANAN PELANGGARAN DATA DAN INCIDENT RESPONSE
## Sesuai UU PDP dan Standar Internasional

---

## 1. DASAR HUKUM DAN STANDAR

### 1.1 Peraturan Perundang-undangan
- **Undang-Undang Nomor 27 Tahun 2022** tentang Perlindungan Data Pribadi (Pasal 62-67)
- **Undang-Undang Nomor 19 Tahun 2016** tentang Perubahan atas UU ITE
- **Peraturan Pemerintah Nomor 71 Tahun 2019** tentang Penyelenggaraan Sistem dan Transaksi Elektronik
- **Peraturan Menteri Komunikasi dan Informatika** tentang Pelaporan Insiden Siber

### 1.2 Standar Internasional
- **ISO/IEC 27035:2016** - Information Security Incident Management
- **NIST SP 800-61 Rev. 2** - Computer Security Incident Handling Guide
- **SANS Incident Response Process** - Six-Phase Incident Response Methodology
- **ENISA Guidelines** - Recommendations for a methodology of the assessment of severity of personal data breaches

### 1.3 Framework Compliance
- **GDPR Article 33-34** - Breach notification requirements (sebagai referensi)
- **PCI DSS Requirement 12.10** - Incident response plan
- **SOX Section 404** - Internal controls over financial reporting

---

## 2. RUANG LINGKUP PENERAPAN

### 2.1 Definisi Pelanggaran Data

#### 2.1.1 Data Breach (Pelanggaran Data Pribadi)
Sesuai UU PDP Pasal 1 angka 21:
"Pelanggaran Data Pribadi adalah setiap perbuatan melawan hukum yang mengakibatkan Data Pribadi yang sedang diproses hilang, bocor, rusak, musnah, berubah, dapat diakses oleh pihak yang tidak berwenang, atau diungkapkan tanpa izin."

#### 2.1.2 Security Incident (Insiden Keamanan)
Setiap kejadian yang dapat mengancam kerahasiaan, integritas, atau ketersediaan informasi dan sistem informasi perusahaan.

### 2.2 Kategori Insiden

#### 2.2.1 Berdasarkan Jenis
- **Malware Infection**: Virus, ransomware, trojan
- **Unauthorized Access**: Akses tidak sah ke sistem atau data
- **Data Exfiltration**: Pencurian atau kebocoran data
- **Denial of Service**: Serangan yang mengganggu layanan
- **Social Engineering**: Phishing, pretexting, baiting
- **Physical Security**: Pencurian perangkat, akses fisik tidak sah
- **Insider Threat**: Ancaman dari internal perusahaan

#### 2.2.2 Berdasarkan Dampak
- **Confidentiality Breach**: Kebocoran informasi rahasia
- **Integrity Compromise**: Perubahan data tidak sah
- **Availability Disruption**: Gangguan layanan atau sistem
- **Privacy Violation**: Pelanggaran privasi data pribadi

### 2.3 Severity Classification

#### 2.3.1 Critical (P1)
**Kriteria:**
- Dampak terhadap >10,000 subjek data
- Data kategori khusus (biometrik, kesehatan, keuangan)
- Potensi kerugian finansial >Rp 10 miliar
- Ancaman terhadap keselamatan jiwa
- Sistem critical business down >4 jam

**Response Time:** Immediate (15 menit)

#### 2.3.2 High (P2)
**Kriteria:**
- Dampak terhadap 1,000-10,000 subjek data
- Data pribadi umum dalam jumlah besar
- Potensi kerugian finansial Rp 1-10 miliar
- Sistem penting down >2 jam
- Reputational risk tinggi

**Response Time:** 1 jam

#### 2.3.3 Medium (P3)
**Kriteria:**
- Dampak terhadap 100-1,000 subjek data
- Data internal perusahaan
- Potensi kerugian finansial Rp 100 juta - 1 miliar
- Sistem non-critical down >8 jam

**Response Time:** 4 jam

#### 2.3.4 Low (P4)
**Kriteria:**
- Dampak terhadap <100 subjek data
- Data publik atau non-sensitif
- Potensi kerugian finansial <Rp 100 juta
- Gangguan minor tanpa dampak bisnis

**Response Time:** 24 jam

---

## 3. PROSEDUR OPERASIONAL STANDAR (SOP)

### 3.1 Incident Response Team (IRT)

#### 3.1.1 Struktur Organisasi
**Incident Commander (IC)**
- Data Protection Officer (DPO) atau designee
- Overall incident management dan decision making
- External communication dan regulatory reporting

**Technical Lead**
- Chief Information Security Officer (CISO) atau IT Security Manager
- Technical analysis dan containment
- Forensic investigation coordination

**Legal Counsel**
- In-house legal atau external legal advisor
- Legal implications assessment
- Regulatory compliance guidance

**Communications Lead**
- Corporate Communications Manager
- Internal dan external communications
- Media relations dan public statements

**HR Representative**
- HR Manager atau Business Partner
- Employee-related incidents
- Internal investigation support

**Business Continuity Lead**
- Operations Manager atau Business Unit Head
- Business impact assessment
- Recovery planning dan execution

#### 3.1.2 Escalation Matrix

| Severity | Notification Time | Escalation Level |
|----------|-------------------|------------------|
| P1 (Critical) | Immediate | CEO, Board of Directors |
| P2 (High) | 1 hour | C-Level Executives |
| P3 (Medium) | 4 hours | Department Heads |
| P4 (Low) | 24 hours | Team Managers |

### 3.2 Phase 1: Preparation

#### 3.2.1 Preventive Measures
**Technical Preparations:**
- Incident response tools dan software
- Forensic investigation capabilities
- Backup dan recovery systems
- Communication systems (secure channels)
- Documentation templates dan forms

**Organizational Preparations:**
- IRT member training dan certification
- Incident response playbooks
- Contact lists (internal/external)
- Legal dan regulatory guidance
- Vendor dan contractor agreements

#### 3.2.2 Detection Capabilities
**Automated Detection:**
- Security Information and Event Management (SIEM)
- Data Loss Prevention (DLP) systems
- Intrusion Detection/Prevention Systems (IDS/IPS)
- Endpoint Detection and Response (EDR)
- User and Entity Behavior Analytics (UEBA)

**Manual Detection:**
- Employee reporting mechanisms
- Customer complaints atau inquiries
- Third-party notifications
- Regulatory authority alerts
- Media monitoring

### 3.3 Phase 2: Detection and Analysis

#### 3.3.1 Initial Assessment (0-30 minutes)
**Step 1: Incident Verification**
1. Confirm incident occurrence
2. Gather initial information
3. Assign incident ID dan timestamp
4. Activate appropriate IRT members
5. Establish communication channels

**Step 2: Preliminary Classification**
1. Determine incident type dan category
2. Assess initial severity level
3. Identify affected systems dan data
4. Estimate potential impact
5. Document initial findings

#### 3.3.2 Detailed Analysis (30 minutes - 4 hours)
**Technical Analysis:**
- System logs dan audit trails review
- Network traffic analysis
- Malware analysis (if applicable)
- Vulnerability assessment
- Attack vector identification

**Impact Assessment:**
- Number of affected data subjects
- Types of data involved
- Potential harm to individuals
- Business impact evaluation
- Regulatory implications

**Evidence Collection:**
- Preserve digital evidence
- Document chain of custody
- Take system snapshots
- Collect relevant logs
- Interview witnesses

### 3.4 Phase 3: Containment, Eradication, and Recovery

#### 3.4.1 Immediate Containment (0-2 hours)
**Short-term Actions:**
- Isolate affected systems
- Disable compromised accounts
- Block malicious IP addresses
- Preserve evidence
- Prevent further damage

**Communication Actions:**
- Notify key stakeholders
- Prepare holding statements
- Coordinate with legal team
- Document all actions taken

#### 3.4.2 Long-term Containment (2-24 hours)
**System Actions:**
- Implement additional security controls
- Deploy patches atau updates
- Reconfigure security settings
- Monitor for continued activity
- Prepare for recovery phase

**Investigation Actions:**
- Conduct forensic analysis
- Determine root cause
- Assess full scope of breach
- Identify all affected data
- Prepare detailed incident report

#### 3.4.3 Eradication (1-7 days)
**Threat Removal:**
- Remove malware atau unauthorized access
- Close security vulnerabilities
- Strengthen security controls
- Update security policies
- Implement additional monitoring

**System Hardening:**
- Apply security patches
- Update configurations
- Enhance access controls
- Improve monitoring capabilities
- Conduct security testing

#### 3.4.4 Recovery (1-30 days)
**System Restoration:**
- Restore systems from clean backups
- Verify system integrity
- Conduct security testing
- Monitor for anomalies
- Gradually restore services

**Business Continuity:**
- Activate business continuity plans
- Communicate with customers
- Restore normal operations
- Monitor business metrics
- Document lessons learned

### 3.5 Phase 4: Post-Incident Activities

#### 3.5.1 Lessons Learned (Within 30 days)
**Review Process:**
- Conduct post-incident review meeting
- Analyze response effectiveness
- Identify improvement opportunities
- Update incident response procedures
- Provide additional training if needed

**Documentation:**
- Complete incident report
- Document timeline of events
- Record all actions taken
- Analyze costs dan impacts
- Archive evidence dan documentation

#### 3.5.2 Process Improvement
**Policy Updates:**
- Revise security policies
- Update incident response procedures
- Enhance detection capabilities
- Improve training programs
- Strengthen preventive controls

---

## 4. NOTIFICATION DAN REPORTING

### 4.1 Internal Notification

#### 4.1.1 Immediate Notification (Within 1 hour)
**Recipients:**
- Incident Commander
- Technical Lead
- Legal Counsel
- Relevant business unit heads

**Information to Include:**
- Incident description dan timeline
- Affected systems dan data
- Initial impact assessment
- Immediate actions taken
- Next steps dan timeline

#### 4.1.2 Executive Notification
**Criteria for CEO/Board Notification:**
- P1 (Critical) incidents - Immediate
- P2 (High) incidents - Within 4 hours
- Regulatory reporting required
- Media attention likely
- Legal action potential

### 4.2 External Notification

#### 4.2.1 Regulatory Notification (UU PDP)
**Timeline:** Within 72 hours of becoming aware

**Recipient:** Menteri yang menyelenggarakan urusan pemerintahan di bidang komunikasi dan informatika

**Required Information (Pasal 62):**
1. Identitas Pengendali Data Pribadi
2. Waktu terjadinya Pelanggaran Data Pribadi
3. Waktu Pengendali Data Pribadi mengetahui terjadinya Pelanggaran Data Pribadi
4. Kategori dan perkiraan jumlah Subjek Data Pribadi yang terkena dampak
5. Kategori dan perkiraan jumlah Data Pribadi yang terkena dampak
6. Uraian Pelanggaran Data Pribadi yang terjadi
7. Dampak yang ditimbulkan atau yang mungkin ditimbulkan dari Pelanggaran Data Pribadi
8. Langkah yang telah atau akan diambil untuk menangani Pelanggaran Data Pribadi
9. Langkah yang telah atau akan diambil untuk mencegah terulangnya Pelanggaran Data Pribadi

#### 4.2.2 Data Subject Notification (UU PDP)
**Timeline:** Segera setelah mengetahui (tanpa penundaan yang tidak perlu)

**Criteria:** Jika Pelanggaran Data Pribadi menimbulkan risiko tinggi terhadap hak dan kebebasan Subjek Data Pribadi

**Required Information (Pasal 63):**
1. Kategori dan perkiraan jumlah Data Pribadi yang terkena dampak
2. Dampak yang ditimbulkan atau yang mungkin ditimbulkan
3. Langkah yang telah atau akan diambil untuk menangani Pelanggaran Data Pribadi
4. Saran tindakan yang dapat dilakukan oleh Subjek Data Pribadi untuk memitigasi dampak negatif
5. Identitas dan detail kontak Pengendali Data Pribadi atau Prosesor Data Pribadi

#### 4.2.3 Other External Notifications
**Law Enforcement:**
- Criminal activity suspected
- Cyber terrorism indicators
- Organized crime involvement

**Business Partners:**
- Shared systems affected
- Contractual notification requirements
- Supply chain impacts

**Customers/Clients:**
- Service disruptions
- Data compromise affecting them
- Preventive measures needed

**Insurance Providers:**
- Cyber insurance claims
- Professional liability coverage
- Business interruption claims

### 4.3 Communication Templates

#### 4.3.1 Internal Incident Alert
```
SUBJECT: [URGENT] Security Incident - [Incident ID]

Incident Details:
- Incident ID: [ID]
- Severity: [P1/P2/P3/P4]
- Discovery Time: [Timestamp]
- Affected Systems: [List]
- Potential Data Impact: [Description]
- Current Status: [Status]

Immediate Actions Required:
- [Action 1]
- [Action 2]
- [Action 3]

Incident Commander: [Name, Contact]
Next Update: [Time]
```

#### 4.3.2 Regulatory Notification Template
```
Kepada: Menteri Komunikasi dan Informatika
Perihal: Laporan Pelanggaran Data Pribadi

1. Identitas Pengendali Data Pribadi:
   - Nama Perusahaan: [Nama]
   - Alamat: [Alamat Lengkap]
   - Kontak: [Email, Telepon]

2. Detail Pelanggaran:
   - Waktu Kejadian: [Tanggal dan Jam]
   - Waktu Penemuan: [Tanggal dan Jam]
   - Jenis Pelanggaran: [Deskripsi]

3. Data yang Terdampak:
   - Jumlah Subjek Data: [Angka]
   - Kategori Data: [Jenis Data]
   - Tingkat Sensitivitas: [Level]

4. Dampak dan Risiko:
   - Dampak Aktual: [Deskripsi]
   - Risiko Potensial: [Analisis]

5. Langkah Penanganan:
   - Tindakan Segera: [List]
   - Rencana Pemulihan: [Deskripsi]
   - Pencegahan: [Measures]

Hormat kami,
[Nama dan Jabatan]
[Tanda Tangan]
```

---

## 5. MEKANISME PENGAWASAN DAN EVALUASI

### 5.1 Monitoring dan Metrics

#### 5.1.1 Key Performance Indicators (KPI)
**Response Metrics:**
- Mean Time to Detection (MTTD)
- Mean Time to Response (MTTR)
- Mean Time to Recovery (MTTR)
- Incident resolution rate
- False positive rate

**Compliance Metrics:**
- Regulatory notification timeliness
- Data subject notification compliance
- Documentation completeness
- Training completion rates
- Exercise participation rates

#### 5.1.2 Incident Tracking
**Incident Database:**
- Incident ID dan classification
- Timeline dan response actions
- Impact assessment dan costs
- Lessons learned dan improvements
- Regulatory reporting status

### 5.2 Testing dan Exercises

#### 5.2.1 Tabletop Exercises
**Frequency:** Quarterly
**Participants:** IRT members, key stakeholders
**Scenarios:** Realistic breach scenarios
**Objectives:** Test procedures, identify gaps, improve coordination

#### 5.2.2 Simulation Exercises
**Frequency:** Semi-annually
**Scope:** Full incident response simulation
**Duration:** 4-8 hours
**Evaluation:** Response effectiveness, communication, decision-making

#### 5.2.3 Red Team Exercises
**Frequency:** Annually
**Scope:** Authorized penetration testing
**Objective:** Test detection dan response capabilities
**Follow-up:** Improvement plan implementation

### 5.3 Continuous Improvement

#### 5.3.1 Regular Reviews
**Monthly Reviews:**
- Incident trends analysis
- Metrics review dan reporting
- Process effectiveness assessment
- Training needs identification

**Quarterly Reviews:**
- Procedure updates
- Technology improvements
- Stakeholder feedback
- Regulatory changes impact

**Annual Reviews:**
- Comprehensive program assessment
- Strategic planning
- Budget planning
- Maturity assessment

#### 5.3.2 Industry Collaboration
**Information Sharing:**
- Industry threat intelligence
- Best practices sharing
- Regulatory guidance updates
- Technology trends monitoring

---

## 6. ROLES DAN RESPONSIBILITIES

### 6.1 Executive Leadership

#### 6.1.1 Chief Executive Officer (CEO)
- Ultimate accountability untuk incident response
- Strategic decision making untuk major incidents
- External stakeholder communication
- Resource allocation untuk response activities

#### 6.1.2 Chief Information Security Officer (CISO)
- Technical incident response leadership
- Security program oversight
- Regulatory compliance coordination
- Vendor dan third-party management

### 6.2 Operational Teams

#### 6.2.1 IT Operations
- System monitoring dan alerting
- Initial incident triage
- Technical containment actions
- System recovery dan restoration

#### 6.2.2 Security Operations Center (SOC)
- 24/7 monitoring dan detection
- Incident analysis dan investigation
- Threat intelligence correlation
- Forensic evidence collection

### 6.3 Support Functions

#### 6.3.1 Legal Department
- Legal implications assessment
- Regulatory compliance guidance
- External legal counsel coordination
- Litigation risk management

#### 6.3.2 Human Resources
- Employee-related incident investigation
- Internal communication coordination
- Disciplinary action implementation
- Training program management

---

## 7. SANKSI DAN KONSEKUENSI

### 7.1 Regulatory Penalties (UU PDP)

#### 7.1.1 Administrative Sanctions (Pasal 65)
- Peringatan tertulis
- Penghentian sementara kegiatan Pemrosesan Data Pribadi
- Penghapusan atau pemusnahan Data Pribadi
- Denda administratif paling banyak Rp 50,000,000,000 (lima puluh miliar rupiah)

#### 7.1.2 Criminal Penalties (Pasal 67)
- Pidana penjara paling lama 5 (lima) tahun
- Denda paling banyak Rp 5,000,000,000 (lima miliar rupiah)

### 7.2 Civil Liabilities
- Compensation untuk affected data subjects
- Class action lawsuits
- Business partner claims
- Insurance deductibles dan premium increases

### 7.3 Business Consequences
- Reputational damage
- Customer churn
- Revenue loss
- Regulatory scrutiny
- Competitive disadvantage

---

**Dokumen ini berlaku efektif sejak: [Tanggal Implementasi]**
**Versi: 1.0**
**Pemilik Dokumen: Data Protection Officer**
**Review Berikutnya: [Tanggal + 6 bulan]**