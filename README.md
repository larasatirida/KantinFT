# KantinFT

**Serverless Campus Canteen Ordering System on AWS**

## Deskripsi Proyek

KantinFT merupakan sistem pemesanan makanan berbasis cloud yang dirancang untuk lingkungan Fakultas Teknik Universitas Gadjah Mada. Antrean pemesanan makanan pada jam istirahat dapat menyebabkan mahasiswa membutuhkan waktu lebih lama untuk mendapatkan makanan.

KantinFT memungkinkan pengguna melakukan pemesanan makanan sebelum waktu pengambilan serta membantu tenant mengelola data dan status pesanan. Pada tahap awal, sistem berfokus pada pengelolaan pesanan melalui operasi Create, Read, Update, dan Delete (CRUD).

Fitur autentikasi pengguna, pembayaran digital, katalog menu, dan antarmuka pengguna berada di luar ruang lingkup implementasi awal.

## Informasi Proyek

| Aspek                 | Keterangan          |
| --------------------- | ------------------- |
| Use Case              | Simple Orders       |
| Track                 | Track C: Serverless |
| Bahasa Pemrograman    | Python 3.13         |
| Storage               | Amazon S3           |
| HTTP Endpoint         | Lambda Function URL |
| Compute               | AWS Lambda          |
| Monitoring            | Amazon CloudWatch   |
| Access Management     | AWS IAM (LabRole)   |
| AWS Region            | us-east-1           |
| Lingkungan Deployment | AWS Academy Sandbox |
| Pengujian API         | Postman / curl      |

## Ruang Lingkup

- Membuat pesanan makanan.
- Menampilkan daftar pesanan.
- Memperbarui data dan status pesanan.
- Menghapus pesanan.
- Menghitung total harga secara otomatis.
- Menyimpan data pesanan sebagai objek JSON pada Amazon S3.
- Melakukan validasi input dan penanganan kesalahan API.

## Arsitektur Sistem

![Arsitektur KantinFT](docs/KantinFT.drawio.png)

KantinFT menggunakan arsitektur serverless yang memungkinkan pengembangan aplikasi tanpa melakukan provisioning dan pengelolaan server secara langsung.

Rancangan awal menggunakan Amazon API Gateway dan Amazon DynamoDB. Namun, karena keterbatasan layanan dan izin akses pada AWS Academy Sandbox, arsitektur disesuaikan menggunakan Lambda Function URL dan Amazon S3 dengan tetap mempertahankan pendekatan serverless.

### Komponen AWS

| Komponen AWS        | Fungsi                                                                                  |
| ------------------- | --------------------------------------------------------------------------------------- |
| Lambda Function URL | Menyediakan HTTPS endpoint untuk menerima request dan memanggil Lambda secara langsung. |
| AWS Lambda          | Menjalankan logika bisnis, routing, dan operasi CRUD menggunakan Python.                |
| Amazon S3           | Menyimpan data pesanan makanan dalam bentuk objek JSON.                                 |
| AWS IAM             | Mengatur izin akses layanan melalui execution role dan resource-based policy.           |
| Amazon CloudWatch   | Mencatat log eksekusi serta mendukung monitoring dan debugging.                         |

### Alur Sistem

1. Pengguna mengirimkan HTTPS request melalui Postman atau curl.
2. Lambda Function URL menerima request dan memanggil AWS Lambda.
3. Lambda mengidentifikasi HTTP method dan request path.
4. Lambda menjalankan validasi input dan logika bisnis sesuai operasi yang diminta.
5. Lambda berinteraksi dengan Amazon S3 menggunakan AWS SDK (boto3).
6. Hasil pemrosesan dikembalikan kepada pengguna dalam format JSON.
7. Log eksekusi Lambda dicatat pada Amazon CloudWatch.

Sistem menggunakan AWS-managed networking tanpa konfigurasi custom VPC. Akses Lambda terhadap Amazon S3 dan CloudWatch diatur melalui IAM execution role (LabRole).

## Model Data

- **Entitas:** Order
- **Storage:** Amazon S3
- **Bucket pengujian awal:** kantinft-orders-2785
- **Object key:** `orders/{order_id}.json`
- **Format penyimpanan:** JSON
- **Bucket access:** Private

Setiap pesanan direpresentasikan sebagai satu objek JSON. Amazon S3 digunakan sebagai object storage, bukan sebagai database relasional maupun NoSQL.

| Atribut       | Tipe Data | Keterangan                       |
| ------------- | --------- | -------------------------------- |
| order_id      | String    | ID unik pesanan                  |
| customer_name | String    | Nama pemesan                     |
| tenant_name   | String    | Nama tenant kantin               |
| food_name     | String    | Nama makanan yang dipesan        |
| quantity      | Integer   | Jumlah makanan                   |
| unit_price    | Integer   | Harga satuan dalam rupiah        |
| total_price   | Integer   | Total harga pesanan dalam rupiah |
| pickup_time   | String    | Jadwal pengambilan pesanan       |
| status        | String    | Status pesanan                   |
| created_at    | String    | Waktu pembuatan pesanan          |
| updated_at    | String    | Waktu pembaruan pesanan          |

### Contoh Data Pesanan

```json
{
  "order_id": "550e8400-e29b-41d4-a716-446655440000",
  "customer_name": "Mahasiswa A",
  "tenant_name": "Kantin FT",
  "food_name": "Nasi Ayam",
  "quantity": 2,
  "unit_price": 15000,
  "total_price": 30000,
  "pickup_time": "2026-11-25T12:00:00+07:00",
  "status": "PENDING",
  "created_at": "2026-11-25T03:00:00Z",
  "updated_at": "2026-11-25T03:00:00Z"
}
```

Data tersebut merupakan contoh data dummy untuk kebutuhan perancangan dan pengujian.

## API Endpoints

| Method | Endpoint     | Operasi         | Amazon S3 Operation      |
| ------ | ------------ | --------------- | ------------------------ |
| POST   | /orders      | Create order    | PutObject                |
| GET    | /orders      | Read all orders | ListObjectsV2, GetObject |
| PUT    | /orders/{id} | Update order    | GetObject, PutObject     |
| DELETE | /orders/{id} | Delete order    | GetObject, DeleteObject  |

Seluruh endpoint direncanakan ditangani oleh satu Lambda function berdasarkan HTTP method dan request path.

### HTTP Status Codes

| Status Code               | Keterangan                            |
| ------------------------- | ------------------------------------- |
| 200 OK                    | Operasi berhasil                      |
| 201 Created               | Pesanan berhasil dibuat               |
| 400 Bad Request           | Input tidak valid                     |
| 404 Not Found             | Pesanan atau endpoint tidak ditemukan |
| 500 Internal Server Error | Terjadi kesalahan pada server         |

## Aturan Bisnis

- ID pesanan dihasilkan secara otomatis menggunakan UUID.
- Setiap pesanan terdiri dari satu jenis makanan dari satu tenant.
- Jumlah makanan dan harga satuan harus berupa bilangan bulat positif.
- Total harga dihitung secara otomatis berdasarkan jumlah makanan dan harga satuan.
- Total harga dihitung kembali apabila jumlah makanan atau harga satuan diperbarui.
- Status awal pesanan adalah PENDING.
- Status pesanan dapat diperbarui menjadi PROCESSING, READY, atau COMPLETED.
- Waktu pengambilan menggunakan format ISO 8601 dengan informasi zona waktu.
- Waktu pembuatan dan pembaruan pesanan dicatat secara otomatis.
- Operasi pembaruan dan penghapusan hanya dapat dilakukan terhadap pesanan yang tersedia.

Pada prototipe ini, harga satuan masih dimasukkan melalui request karena pengelolaan katalog menu berada di luar ruang lingkup proyek.

## Struktur Repository

| Path             | Keterangan                                              |
| ---------------- | ------------------------------------------------------- |
| src/             | Source code AWS Lambda dan logika aplikasi              |
| docs/            | Diagram arsitektur, design brief, dan deployment plan   |
| tests/           | Unit testing dan pengujian fungsi aplikasi              |
| evidence/        | Dokumentasi konfigurasi dan hasil pengujian AWS         |
| requirements.txt | Daftar dependensi Python                                |
| .gitignore       | Konfigurasi file yang tidak disertakan dalam repository |
| README.md        | Dokumentasi utama proyek                                |

## Deployment

Deployment dilakukan menggunakan AWS Academy Sandbox pada region us-east-1.

Tahapan deployment meliputi:

1. Mengaktifkan sesi AWS Academy Sandbox.
2. Membuat private S3 bucket.
3. Membuat AWS Lambda function dengan runtime Python 3.13.
4. Menggunakan IAM execution role (LabRole).
5. Mengonfigurasi environment variable BUCKET_NAME.
6. Mengaktifkan Lambda Function URL.
7. Melakukan pengujian konektivitas Lambda dan Amazon S3.
8. Melakukan deployment kode aplikasi.
9. Melakukan pengujian endpoint CRUD.
10. Memeriksa log eksekusi melalui Amazon CloudWatch.

Panduan deployment secara lengkap tersedia pada [Deployment Plan](docs/deployment-plan.md).

Resource AWS Academy Sandbox bersifat sementara dan dihapus ketika sesi lab berakhir. Oleh karena itu, konfigurasi dan hasil pengujian didokumentasikan agar proses deployment dapat dilakukan kembali pada sesi berikutnya.

## AWS Evidence

Pengujian konektivitas awal telah berhasil dilakukan menggunakan AWS Lambda dan Amazon S3. Lambda berhasil menulis dan membaca objek JSON pada S3, mengembalikan HTTP status 200, serta mencatat hasil eksekusi pada CloudWatch.

| Evidence                                                                 | Keterangan                                 |
| ------------------------------------------------------------------------ | ------------------------------------------ |
| [DynamoDB Access Denied](evidence/01-dynamodb-access-denied.png)         | Bukti keterbatasan izin pada AWS Sandbox   |
| [Lambda Creation](evidence/02-lambda-creation.png)                       | Pembuatan Lambda function                  |
| [Function URL Configuration](evidence/03-function-url-configuration.png) | Konfigurasi HTTP endpoint                  |
| [Lambda Environment](evidence/04-lambda-environment.png)                 | Konfigurasi environment variable           |
| [Lambda Connectivity Test](evidence/05-lambda-connectivity-test.png)     | Hasil pengujian konektivitas Lambda dan S3 |
| [S3 Test Object](evidence/06-s3-test-object.png)                         | Bukti penyimpanan objek JSON pada S3       |
| [CloudWatch Log Group](evidence/07-cloudwatch-log-group.png)             | Dokumentasi log group Lambda               |
| [CloudWatch Log Events](evidence/08-cloudwatch-log-events.png)           | Detail log hasil eksekusi Lambda           |

## Dokumentasi

- [Architecture Diagram](docs/KantinFT.drawio.png)
- [Design Brief](docs/design-brief.pdf)
- [Deployment Plan](docs/deployment-plan.md)
- [AWS Evidence](evidence/)

## Keamanan dan Efisiensi Biaya

- Tidak menyimpan AWS credentials pada repository.
- Menggunakan data dummy selama pengujian.
- Mengaktifkan Block Public Access pada Amazon S3.
- Menggunakan IAM LabRole yang tersedia pada AWS Academy Sandbox.
- Menggunakan HTTPS untuk komunikasi antara client dan Lambda Function URL.
- Menggunakan Auth NONE hanya untuk pengujian prototipe.
- Tidak mempublikasikan Function URL secara terbuka pada repository.
- Memantau penggunaan kredit AWS secara berkala.
- Menghindari pembuatan resource cloud yang tidak diperlukan.
- Mengakhiri sesi lab setelah pengujian selesai.

Konfigurasi Auth NONE memungkinkan endpoint diakses tanpa autentikasi sehingga tidak ditujukan untuk penggunaan produksi atau penyimpanan data pengguna sebenarnya.
