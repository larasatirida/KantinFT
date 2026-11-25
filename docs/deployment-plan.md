# KantinFT: Deployment Plan

## 1. Tujuan

Deployment bertujuan untuk menyiapkan dan memverifikasi infrastruktur KantinFT menggunakan AWS Academy Sandbox. Proses deployment berfokus pada integrasi Lambda Function URL, AWS Lambda, dan Amazon S3 untuk memastikan setiap komponen dapat berkomunikasi dan menjalankan fungsinya dengan penggunaan kredit AWS yang efisien. Rancangan awal menggunakan Amazon API Gateway dan Amazon DynamoDB. Namun, karena keterbatasan layanan dan izin akses pada AWS Academy Sandbox, arsitektur disesuaikan dengan tetap mempertahankan pendekatan serverless.

## 2. Rencana Resource AWS

| Layanan / Komponen  | Nama Resource                   | Konfigurasi                                          |
| ------------------- | ------------------------------- | ---------------------------------------------------- |
| Amazon S3           | kantinft-orders-2785            | General purpose bucket, private, Block Public Access |
| AWS Lambda          | KantinOrderFunction             | Python 3.13, memory 128 MB                           |
| Lambda Function URL | URL yang dihasilkan oleh AWS    | Auth NONE, Buffered                                  |
| AWS IAM             | LabRole                         | Execution role bawaan AWS Academy Sandbox            |
| Amazon CloudWatch   | /aws/lambda/KantinOrderFunction | Log eksekusi Lambda                                  |

Seluruh resource regional menggunakan AWS Region us-east-1 tanpa konfigurasi custom VPC.

Nama S3 bucket tersebut merupakan nama yang digunakan pada sesi pengujian awal. Nama bucket dapat disesuaikan pada sesi deployment berikutnya karena nama bucket S3 harus unik secara global.

## 3. Prasyarat

- Sesi AWS Academy Sandbox aktif.
- Kredit AWS masih tersedia.
- Repository GitHub telah disiapkan.
- Source code Python tersedia.
- Postman atau curl tersedia untuk pengujian.
- Memiliki akses terhadap layanan dan izin AWS yang diperlukan.

## 4. Tahapan Deployment

### Phase 1: Persiapan Lingkungan

- Memulai sesi AWS Academy Sandbox.
- Memeriksa sisa kredit AWS.
- Membuka AWS Management Console.
- Memastikan AWS Region menggunakan us-east-1.
- Memeriksa layanan dan izin akses yang tersedia.

### Phase 2: Konfigurasi Amazon S3

- Membuka layanan Amazon S3.
- Membuat general purpose bucket.
- Menentukan nama bucket yang unik secara global.
- Memilih region us-east-1.
- Mengaktifkan Block Public Access.
- Menonaktifkan bucket versioning untuk kebutuhan prototipe.
- Menggunakan default encryption SSE-S3.
- Memastikan bucket berhasil dibuat dan tidak dapat diakses secara publik.

Data pesanan direncanakan disimpan sebagai objek JSON dengan format object key `orders/{order_id}.json`.

### Phase 3: Konfigurasi AWS Lambda

- Membuat Lambda function bernama KantinOrderFunction.
- Memilih runtime Python 3.13.
- Menggunakan IAM execution role yang tersedia, yaitu LabRole.
- Menggunakan konfigurasi memory 128 MB.
- Menambahkan environment variable BUCKET_NAME sesuai nama S3 bucket.
- Melakukan deployment kode pengujian konektivitas.
- Melakukan pengujian awal terhadap Lambda function.
- Memverifikasi izin akses penulisan dan pembacaan objek pada Amazon S3.

### Phase 4: Konfigurasi Lambda Function URL

- Membuka konfigurasi Lambda Function URL.
- Membuat Function URL untuk KantinOrderFunction.
- Menggunakan Auth NONE untuk pengujian prototipe.
- Menggunakan invoke mode Buffered.
- Tidak mengaktifkan CORS karena pengujian dilakukan melalui Postman atau curl.
- Memastikan resource-based policy mengizinkan pemanggilan melalui Function URL.
- Mendapatkan Function URL yang dihasilkan oleh AWS.
- Melakukan pengujian HTTP request melalui Function URL.

Routing untuk empat endpoint CRUD akan ditangani oleh kode Python pada Lambda berdasarkan HTTP method dan request path.

### Phase 5: Pengujian Konektivitas Awal

- Melakukan pengujian Lambda secara langsung.
- Menulis objek JSON pengujian ke Amazon S3.
- Membaca kembali objek JSON yang telah disimpan.
- Memeriksa status code dan JSON response.
- Memastikan objek `tests/connectivity-test.json` tersedia pada S3 bucket.
- Memeriksa log eksekusi melalui Amazon CloudWatch.

Tahapan ini bertujuan untuk memastikan infrastruktur dasar dapat berkomunikasi sebelum implementasi aplikasi CRUD secara menyeluruh.

### Phase 6: Deployment Aplikasi CRUD

- Menyiapkan source code aplikasi yang menggunakan Amazon S3.
- Melakukan pengujian kode secara lokal.
- Menyiapkan deployment package Lambda apabila diperlukan.
- Melakukan deployment source code aplikasi ke AWS Lambda.
- Memastikan handler dan environment variable telah dikonfigurasi dengan benar.
- Menguji empat endpoint CRUD melalui Postman atau curl.
- Memeriksa objek pesanan yang tersimpan pada Amazon S3.
- Memeriksa HTTP status code dan JSON response.
- Memeriksa log eksekusi dan kesalahan melalui CloudWatch.

Tahapan ini merupakan rencana pengembangan lanjutan setelah pengujian konektivitas awal.

### Phase 7: Dokumentasi dan Penyelesaian

- Mengambil screenshot konfigurasi resource AWS.
- Mendokumentasikan hasil pengujian konektivitas dan API.
- Menyimpan bukti pengujian pada folder evidence.
- Menyembunyikan informasi akun dan kredensial sebelum mempublikasikan dokumentasi.
- Memperbarui README dan dokumentasi deployment.
- Melakukan commit dan push ke GitHub.
- Mengakhiri sesi lab setelah seluruh kebutuhan pengujian terpenuhi.

## 5. Rencana Pengujian

### Pengujian Infrastruktur Awal

| Skenario Pengujian     | Hasil yang Diharapkan                      | Status   |
| ---------------------- | ------------------------------------------ | -------- |
| Lambda invocation      | Function berhasil dijalankan               | Berhasil |
| Lambda Function URL    | HTTP request berhasil diterima oleh Lambda | Berhasil |
| S3 PutObject           | Lambda berhasil menulis objek JSON         | Berhasil |
| S3 GetObject           | Lambda berhasil membaca objek JSON         | Berhasil |
| S3 object verification | Objek pengujian tersedia pada bucket       | Berhasil |
| CloudWatch logging     | Log eksekusi Lambda tersedia               | Berhasil |

### Pengujian Aplikasi CRUD

| Skenario Pengujian          | Hasil yang Diharapkan                           |
| --------------------------- | ----------------------------------------------- |
| POST /orders                | 201 Created                                     |
| GET /orders                 | 200 OK                                          |
| PUT /orders/{id}            | 200 OK                                          |
| DELETE /orders/{id}         | 200 OK                                          |
| Input tidak valid           | 400 Bad Request                                 |
| Pesanan tidak ditemukan     | 404 Not Found                                   |
| Endpoint tidak ditemukan    | 404 Not Found                                   |
| Kesalahan internal          | 500 Internal Server Error                       |
| Perubahan jumlah atau harga | Total harga dihitung kembali                    |
| Verifikasi penyimpanan      | Objek JSON sesuai dengan operasi yang dilakukan |

Pengujian aplikasi CRUD akan dilakukan setelah implementasi source code selesai.

## 6. Keamanan

- Menggunakan HTTPS untuk komunikasi antara pengguna dan Lambda Function URL.
- Menggunakan IAM execution role (LabRole) yang tersedia pada AWS Academy Sandbox.
- Menggunakan private S3 bucket dengan Block Public Access.
- Menggunakan default encryption SSE-S3 untuk penyimpanan objek.
- Tidak menyimpan AWS credentials pada source code maupun repository.
- Menggunakan environment variable untuk konfigurasi resource.
- Menggunakan data dummy selama pengujian.
- Menggunakan Auth NONE hanya untuk pengujian prototipe.
- Tidak mempublikasikan Function URL secara terbuka pada repository.

Konfigurasi Auth NONE memungkinkan endpoint diakses tanpa autentikasi. Oleh karena itu, konfigurasi ini tidak ditujukan untuk penggunaan produksi atau penyimpanan data pengguna sebenarnya.

## 7. Manajemen Biaya

AWS Academy memiliki keterbatasan kredit yang tidak dapat direset. Oleh karena itu, penggunaan resource perlu direncanakan secara efisien melalui beberapa langkah berikut:

- Menggunakan arsitektur serverless untuk pengujian dengan volume request rendah.
- Menghindari penggunaan EC2 dan resource jaringan yang tidak diperlukan.
- Menggunakan Amazon S3 untuk penyimpanan objek JSON berukuran kecil.
- Menyesuaikan memory dan waktu eksekusi Lambda dengan kebutuhan aplikasi.
- Membatasi request dan logging yang tidak diperlukan.
- Melakukan pengembangan dan pengujian kode secara lokal sebelum deployment.
- Memantau sisa kredit AWS secara berkala.
- Mengaktifkan sesi lab hanya ketika diperlukan.
- Mengakhiri sesi lab setelah pengujian dan dokumentasi selesai.

Resource AWS Academy Sandbox bersifat sementara dan dihapus ketika sesi lab berakhir. Oleh karena itu, konfigurasi resource, source code, dan bukti pengujian perlu disimpan agar deployment dapat dilakukan kembali pada sesi berikutnya.

## 8. Target Hasil Deployment

### Week 12: Design & AWS Setup

- Private S3 bucket berhasil dibuat.
- Lambda function berhasil dikonfigurasi.
- IAM LabRole berhasil digunakan oleh Lambda.
- Lambda Function URL berhasil dikonfigurasi.
- Konektivitas HTTP berhasil diuji.
- Lambda berhasil menulis dan membaca objek JSON pada Amazon S3.
- Log eksekusi tersedia pada CloudWatch.
- Screenshot konfigurasi dan hasil pengujian tersedia.
- Repository GitHub dan dokumentasi telah diperbarui.

### Pengembangan Lanjutan

- Seluruh operasi CRUD berhasil diimplementasikan.
- Seluruh endpoint API berhasil diuji.
- Data pesanan berhasil disimpan dan dikelola pada Amazon S3.
- Validasi input dan penanganan kesalahan berjalan sesuai rancangan.
- Aplikasi berhasil di-deploy secara menyeluruh.

## 9. Status Deployment

**Week 12: Initial Infrastructure Setup & Connectivity Testing Completed.**

Pengujian infrastruktur awal telah dilakukan pada 25 November 2026 menggunakan AWS Academy Sandbox pada region us-east-1.

| Komponen                 | Status                           |
| ------------------------ | -------------------------------- |
| Amazon S3                | Berhasil dikonfigurasi           |
| AWS Lambda               | Berhasil dikonfigurasi           |
| IAM LabRole              | Berhasil digunakan               |
| Lambda Function URL      | Berhasil dikonfigurasi dan diuji |
| Lambda-S3 Connectivity   | Berhasil diuji                   |
| Amazon CloudWatch        | Berhasil diverifikasi            |
| AWS Evidence             | Tersedia                         |
| Implementasi CRUD        | Direncanakan                     |
| Deployment aplikasi CRUD | Direncanakan                     |

Bukti konfigurasi dan hasil pengujian tersedia pada folder [evidence](../evidence/).

Sesi AWS Sandbox telah diakhiri setelah pengujian awal selesai. Resource perlu dibuat kembali pada sesi berikutnya sebelum deployment aplikasi CRUD dilakukan.
