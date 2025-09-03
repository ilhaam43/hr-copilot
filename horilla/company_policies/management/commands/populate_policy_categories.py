from django.core.management.base import BaseCommand
from company_policies.models import PolicyCategory, CompanyPolicyDocument
from django.contrib.auth.models import User
from datetime import datetime


class Command(BaseCommand):
    help = 'Populate initial policy categories and documents based on UU PDP and CISO standards'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate policy categories...'))
        
        # Create policy categories
        categories_data = [
            {
                'name': 'Perlindungan Data Pribadi',
                'description': 'Kebijakan perlindungan data pribadi sesuai UU No. 27 Tahun 2022',
                'category_type': 'data_protection',
                'is_mandatory': True
            },
            {
                'name': 'Keamanan Informasi',
                'description': 'Kebijakan keamanan informasi berdasarkan standar CISO',
                'category_type': 'information_security',
                'is_mandatory': True
            },
            {
                'name': 'Klasifikasi Data Sensitif',
                'description': 'Prosedur klasifikasi dan penanganan data sensitif perusahaan',
                'category_type': 'data_classification',
                'is_mandatory': True
            },
            {
                'name': 'Penanganan Pelanggaran Data',
                'description': 'Prosedur incident response dan penanganan pelanggaran data',
                'category_type': 'data_breach',
                'is_mandatory': True
            },
            {
                'name': 'Hak dan Kewajiban Pengguna Data',
                'description': 'Dokumen hak dan kewajiban pengguna data sesuai regulasi',
                'category_type': 'user_rights',
                'is_mandatory': True
            }
        ]
        
        created_categories = []
        for category_data in categories_data:
            category, created = PolicyCategory.objects.get_or_create(
                name=category_data['name'],
                defaults=category_data
            )
            if created:
                created_categories.append(category)
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name}')
                )
        
        # Create sample policy documents
        documents_data = [
            {
                'title': 'Kebijakan Perlindungan Data Pribadi Karyawan',
                'content': '''# KEBIJAKAN PERLINDUNGAN DATA PRIBADI KARYAWAN

## 1. TUJUAN
Kebijakan ini bertujuan untuk melindungi data pribadi karyawan sesuai dengan UU No. 27 Tahun 2022 tentang Perlindungan Data Pribadi.

## 2. RUANG LINGKUP
- Data pribadi karyawan aktif dan non-aktif
- Proses pengumpulan, pengolahan, dan penyimpanan data
- Hak-hak subjek data pribadi

## 3. DEFINISI DATA PRIBADI
- Data identitas: nama, NIK, alamat, nomor telepon
- Data keuangan: gaji, rekening bank, NPWP
- Data kesehatan: riwayat medis, asuransi kesehatan
- Data biometrik: sidik jari, foto wajah

## 4. PRINSIP PENGOLAHAN DATA
- Lawfulness: pengolahan berdasarkan persetujuan atau kewajiban hukum
- Fairness: pengolahan dilakukan secara adil dan transparan
- Purpose limitation: data hanya digunakan sesuai tujuan
- Data minimization: hanya mengumpulkan data yang diperlukan
- Accuracy: memastikan data akurat dan terkini
- Storage limitation: penyimpanan sesuai periode yang ditentukan
- Security: menerapkan langkah keamanan yang memadai

## 5. HAK SUBJEK DATA
- Hak akses terhadap data pribadi
- Hak koreksi data yang tidak akurat
- Hak penghapusan data
- Hak portabilitas data
- Hak keberatan terhadap pengolahan

## 6. KEWAJIBAN PERUSAHAAN
- Menunjuk Data Protection Officer (DPO)
- Melakukan Data Protection Impact Assessment (DPIA)
- Melaporkan pelanggaran data dalam 72 jam
- Memberikan pelatihan kepada karyawan

## 7. SANKSI
Pelanggaran terhadap kebijakan ini dapat dikenakan sanksi sesuai peraturan perusahaan dan perundang-undangan yang berlaku.''',
                'category_type': 'data_protection',
                'version': '1.0'
            },
            {
                'title': 'Kebijakan Keamanan Informasi',
                'content': '''# KEBIJAKAN KEAMANAN INFORMASI

## 1. TUJUAN
Menetapkan standar keamanan informasi untuk melindungi aset informasi perusahaan dari ancaman internal dan eksternal.

## 2. KLASIFIKASI INFORMASI
### Public (Publik)
- Informasi yang dapat diakses oleh umum
- Tidak memerlukan perlindungan khusus

### Internal (Internal)
- Informasi untuk penggunaan internal perusahaan
- Memerlukan kontrol akses dasar

### Confidential (Rahasia)
- Informasi sensitif perusahaan
- Memerlukan perlindungan tinggi
- Akses terbatas pada personel yang berwenang

### Restricted (Sangat Rahasia)
- Informasi sangat sensitif
- Akses sangat terbatas
- Memerlukan otorisasi khusus

## 3. KONTROL AKSES
- Prinsip least privilege
- Autentikasi multi-faktor untuk sistem kritis
- Review akses berkala
- Pencabutan akses segera untuk karyawan yang keluar

## 4. KEAMANAN FISIK
- Kontrol akses ke ruang server dan fasilitas IT
- Penggunaan CCTV dan sistem alarm
- Kebijakan clear desk dan clear screen

## 5. KEAMANAN JARINGAN
- Firewall dan sistem deteksi intrusi
- Segmentasi jaringan
- Enkripsi untuk transmisi data sensitif
- VPN untuk akses remote

## 6. MANAJEMEN INSIDEN
- Tim respons insiden keamanan
- Prosedur pelaporan insiden
- Analisis dan pembelajaran dari insiden

## 7. PELATIHAN DAN KESADARAN
- Pelatihan keamanan informasi untuk semua karyawan
- Simulasi phishing berkala
- Update tentang ancaman keamanan terbaru''',
                'category_type': 'information_security',
                'version': '1.0'
            },
            {
                'title': 'Prosedur Klasifikasi Data Sensitif',
                'content': '''# PROSEDUR KLASIFIKASI DATA SENSITIF

## 1. TUJUAN
Menetapkan prosedur untuk mengklasifikasikan data berdasarkan tingkat sensitivitas dan menentukan kontrol keamanan yang sesuai.

## 2. KRITERIA KLASIFIKASI

### Data Publik
- Tidak berdampak jika diketahui publik
- Contoh: informasi produk, pengumuman umum

### Data Internal
- Dapat merugikan jika diketahui pihak luar
- Contoh: struktur organisasi, prosedur internal

### Data Rahasia
- Dapat merugikan secara signifikan jika bocor
- Contoh: data karyawan, laporan keuangan

### Data Sangat Rahasia
- Dapat merugikan secara serius jika bocor
- Contoh: strategi bisnis, data pribadi sensitif

## 3. PROSEDUR KLASIFIKASI
1. Identifikasi pemilik data
2. Evaluasi dampak jika data bocor
3. Tentukan klasifikasi berdasarkan kriteria
4. Beri label pada dokumen/sistem
5. Terapkan kontrol keamanan sesuai klasifikasi

## 4. KONTROL KEAMANAN

### Data Publik
- Tidak ada kontrol khusus

### Data Internal
- Akses terbatas pada karyawan
- Backup rutin

### Data Rahasia
- Akses berdasarkan need-to-know
- Enkripsi saat penyimpanan dan transmisi
- Audit trail

### Data Sangat Rahasia
- Otorisasi khusus untuk akses
- Enkripsi tingkat tinggi
- Monitoring ketat
- Non-disclosure agreement

## 5. REVIEW DAN UPDATE
- Review klasifikasi data setiap 6 bulan
- Update berdasarkan perubahan bisnis
- Dokumentasi perubahan klasifikasi''',
                'category_type': 'data_classification',
                'version': '1.0'
            },
            {
                'title': 'Prosedur Penanganan Pelanggaran Data',
                'content': '''# PROSEDUR PENANGANAN PELANGGARAN DATA

## 1. DEFINISI PELANGGARAN DATA
Pelanggaran data adalah insiden keamanan yang mengakibatkan akses, pengungkapan, perubahan, atau penghancuran data pribadi yang tidak sah.

## 2. TIM RESPONS INSIDEN
- Incident Response Manager
- Data Protection Officer
- IT Security Team
- Legal Team
- Communications Team

## 3. PROSEDUR RESPONS (72 JAM)

### Jam 0-1: Deteksi dan Pelaporan
- Identifikasi insiden
- Lapor ke Incident Response Manager
- Aktivasi tim respons

### Jam 1-4: Assessment Awal
- Evaluasi tingkat keparahan
- Identifikasi data yang terdampak
- Tentukan apakah perlu pelaporan ke otoritas

### Jam 4-24: Containment
- Isolasi sistem yang terdampak
- Hentikan penyebaran pelanggaran
- Kumpulkan bukti digital

### Jam 24-72: Investigasi dan Pelaporan
- Analisis mendalam penyebab insiden
- Dokumentasi temuan
- Lapor ke Kominfo jika diperlukan
- Notifikasi ke subjek data yang terdampak

## 4. KRITERIA PELAPORAN KE OTORITAS
- Pelanggaran data pribadi sensitif
- Jumlah subjek data > 1000 orang
- Risiko tinggi terhadap hak dan kebebasan
- Pelanggaran sistem kritis

## 5. KOMUNIKASI EKSTERNAL
- Template notifikasi untuk subjek data
- Press release jika diperlukan
- Koordinasi dengan media relations

## 6. RECOVERY DAN LESSONS LEARNED
- Pemulihan sistem dan data
- Implementasi perbaikan keamanan
- Update prosedur berdasarkan pembelajaran
- Pelatihan tambahan untuk karyawan

## 7. DOKUMENTASI
- Log semua aktivitas respons
- Laporan post-incident
- Rekomendasi perbaikan
- Update risk register''',
                'category_type': 'data_breach',
                'version': '1.0'
            },
            {
                'title': 'Hak dan Kewajiban Pengguna Data',
                'content': '''# HAK DAN KEWAJIBAN PENGGUNA DATA

## 1. HAK SUBJEK DATA PRIBADI

### Hak Informasi
- Mengetahui tujuan pengumpulan data
- Mengetahui dasar hukum pengolahan
- Mengetahui periode penyimpanan data
- Mengetahui pihak yang dapat mengakses data

### Hak Akses
- Meminta salinan data pribadi yang diolah
- Mengetahui status pengolahan data
- Mendapat informasi tentang penerima data

### Hak Koreksi
- Meminta perbaikan data yang tidak akurat
- Meminta pembaruan data yang tidak lengkap
- Meminta penghapusan data yang salah

### Hak Penghapusan
- Meminta penghapusan data jika tidak diperlukan
- Meminta penghapusan jika pengolahan tidak sah
- Meminta penghapusan jika ada keberatan

### Hak Portabilitas
- Meminta data dalam format yang dapat dibaca mesin
- Meminta transfer data ke pengendali lain

### Hak Keberatan
- Menolak pengolahan untuk tujuan tertentu
- Menolak profiling otomatis
- Menolak direct marketing

## 2. KEWAJIBAN SUBJEK DATA

### Memberikan Data yang Akurat
- Menyampaikan informasi yang benar
- Memberitahu perubahan data penting
- Tidak memberikan data palsu

### Menjaga Kerahasiaan
- Melindungi kredensial akses
- Tidak membagikan informasi sensitif
- Melaporkan dugaan pelanggaran keamanan

### Mematuhi Kebijakan
- Mengikuti prosedur yang ditetapkan
- Berpartisipasi dalam pelatihan
- Mematuhi batasan akses data

## 3. KEWAJIBAN PENGENDALI DATA

### Transparansi
- Memberikan privacy notice yang jelas
- Menjelaskan tujuan pengolahan data
- Memberikan informasi kontak DPO

### Keamanan
- Menerapkan langkah keamanan teknis
- Melakukan enkripsi data sensitif
- Membatasi akses berdasarkan kebutuhan

### Akuntabilitas
- Mendokumentasikan aktivitas pengolahan
- Melakukan audit kepatuhan berkala
- Melaporkan pelanggaran data

## 4. PROSEDUR PENGAJUAN HAK

### Cara Mengajukan
- Email ke: dpo@company.com
- Form online di portal karyawan
- Surat tertulis ke bagian HR

### Waktu Respons
- Konfirmasi penerimaan: 3 hari kerja
- Respons lengkap: 30 hari kerja
- Perpanjangan maksimal: 60 hari kerja

### Verifikasi Identitas
- Fotokopi KTP/identitas resmi
- Verifikasi melalui email perusahaan
- Konfirmasi melalui telepon jika diperlukan

## 5. ESKALASI DAN KELUHAN
- Keluhan internal ke DPO
- Keluhan eksternal ke Kominfo
- Mediasi melalui lembaga yang berwenang''',
                'category_type': 'user_rights',
                'version': '1.0'
            }
        ]
        
        # Get first superuser as creator, or create a default user
        try:
            creator = User.objects.filter(is_superuser=True).first()
            if not creator:
                creator = User.objects.create_user(
                    username='system',
                    email='system@company.com',
                    first_name='System',
                    last_name='Administrator'
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error getting creator user: {e}')
            )
            return
        
        # Create policy documents
        for doc_data in documents_data:
            # Find the corresponding category
            try:
                category = PolicyCategory.objects.get(
                    category_type=doc_data['category_type']
                )
                
                document, created = CompanyPolicyDocument.objects.get_or_create(
                    title=doc_data['title'],
                    defaults={
                        'content': doc_data['content'],
                        'category': category,
                        'version': doc_data['version'],
                        'status': 'active',
                        'effective_date': datetime.now().date()
                    }
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Created document: {document.title}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Document already exists: {document.title}')
                    )
                    
            except PolicyCategory.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(
                        f'Category not found for type: {doc_data["category_type"]}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated policy categories and documents!')
        )