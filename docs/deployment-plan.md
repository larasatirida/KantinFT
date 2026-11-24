# KantinFT: Deployment Plan

## 1. Tujuan

Deployment bertujuan untuk menyiapkan dan memverifikasi infrastruktur awal KantinFT menggunakan AWS Learner Lab.

Proses deployment berfokus pada integrasi Amazon API Gateway, AWS Lambda, dan Amazon DynamoDB untuk memastikan setiap komponen dapat berkomunikasi dan menjalankan fungsinya dengan penggunaan kredit AWS yang efisien.

## 2. Rencana Resource AWS

| Layanan     | Nama Resource                   | Konfigurasi                                          |
| ----------- | ------------------------------- | ---------------------------------------------------- |
| DynamoDB    | KantinOrders                    | On-demand, partition key bertipe String              |
| Lambda      | KantinOrderFunction             | Python 3.12, memory 128 MB                           |
| API Gateway | KantinFT-API                    | HTTP API                                             |
| IAM         | LabRole                         | Execution role bawaan, menyesuaikan izin Learner Lab |
| CloudWatch  | /aws/lambda/KantinOrderFunction | Log eksekusi Lambda                                  |

Seluruh resource regional akan dibuat pada AWS Region yang sama dan didukung oleh AWS Learner Lab.

## 3. Prasyarat

- Sesi AWS Learner Lab aktif.
- Kredit AWS masih tersedia.
- Repository GitHub telah disiapkan.
- Source code Python tersedia.
- Postman atau curl tersedia untuk pengujian.
- Memiliki akses terhadap layanan dan izin AWS yang diperlukan.

## 4. Tahapan Deployment

### Phase 1: Persiapan Lingkungan

- Memulai sesi AWS Learner Lab.
- Memeriksa sisa kredit AWS.
- Membuka AWS Management Console.
- Memastikan AWS Region dan izin layanan yang tersedia.

### Phase 2: Konfigurasi DynamoDB

- Membuat tabel bernama KantinOrders.
- Menentukan order_id sebagai partition key bertipe String.
- Menggunakan capacity mode on-demand.
- Memastikan status tabel telah Active.

### Phase 3: Konfigurasi Lambda

- Membuat Lambda function bernama KantinOrderFunction.
- Memilih runtime Python.
- Menggunakan IAM execution role yang tersedia dan diizinkan.
- Menambahkan environment variable TABLE_NAME dengan nilai KantinOrders.
- Melakukan deployment source code Lambda.
- Melakukan pengujian awal terhadap Lambda function.
- Memverifikasi izin akses baca dan tulis terhadap DynamoDB.

### Phase 4: Konfigurasi API Gateway

- Membuat HTTP API bernama KantinFT-API.
- Mengintegrasikan API dengan KantinOrderFunction.
- Mengonfigurasi empat CRUD routes.
- Memastikan API Gateway memiliki izin untuk memanggil Lambda.
- Mengonfigurasi deployment stage.
- Mendapatkan API invoke URL.

### Phase 5: Pengujian Konektivitas dan API

- Melakukan pengujian Lambda secara langsung.
- Memastikan Lambda dapat mengakses DynamoDB.
- Mengirim HTTP request melalui API Gateway.
- Memeriksa HTTP status code dan JSON response.
- Memeriksa data pesanan yang tersimpan pada DynamoDB.
- Memeriksa log eksekusi melalui CloudWatch.

### Phase 6: Dokumentasi

- Mengambil screenshot konfigurasi resource AWS.
- Mendokumentasikan hasil pengujian konektivitas.
- Menyimpan bukti pengujian pada folder evidence.
- Memperbarui README dan dokumentasi deployment.
- Melakukan commit dan push ke GitHub.

## 5. Rencana Pengujian

| Skenario Pengujian      | Hasil yang Diharapkan                      |
| ----------------------- | ------------------------------------------ |
| Lambda invocation       | Function berhasil dijalankan               |
| Konektivitas DynamoDB   | Lambda dapat mengakses tabel               |
| Integrasi API Gateway   | HTTP request berhasil diteruskan ke Lambda |
| POST /orders            | 201 Created                                |
| GET /orders             | 200 OK                                     |
| PUT /orders/{id}        | 200 OK                                     |
| DELETE /orders/{id}     | 200 OK                                     |
| Input tidak valid       | 400 Bad Request                            |
| Pesanan tidak ditemukan | 404 Not Found                              |

## 6. Keamanan

- Menggunakan HTTPS untuk komunikasi antara pengguna dan API Gateway.
- Menggunakan IAM execution role yang diizinkan oleh AWS Learner Lab.
- Memverifikasi izin API Gateway untuk memanggil Lambda.
- Tidak menyimpan AWS credentials pada source code maupun repository.
- Menggunakan environment variable untuk konfigurasi resource.
- Menggunakan data dummy selama pengujian.
- Menggunakan API tanpa autentikasi hanya untuk keperluan pengujian sementara.

## 7. Manajemen Biaya

AWS Learner Lab memiliki keterbatasan kredit yang tidak dapat direset. Oleh karena itu, penggunaan resource perlu direncanakan secara efisien melalui beberapa langkah berikut:

- Menggunakan arsitektur serverless untuk kebutuhan pengujian dengan volume request rendah.
- Menghindari penggunaan EC2 dan resource jaringan yang tidak diperlukan.
- Menggunakan capacity mode on-demand pada DynamoDB.
- Menyesuaikan memory dan waktu eksekusi Lambda dengan kebutuhan aplikasi.
- Membatasi request dan logging yang tidak diperlukan.
- Memantau sisa kredit AWS secara berkala.
- Menghapus resource yang tidak lagi diperlukan setelah memastikan kebutuhan pengujian dan penilaian telah terpenuhi.

## 8. Target Hasil Deployment

- Tabel DynamoDB berhasil dibuat dan berstatus Active.
- Lambda function berhasil dikonfigurasi.
- Izin akses IAM berhasil diverifikasi.
- API Gateway berhasil terintegrasi dengan Lambda.
- Konektivitas antarservice berhasil diuji.
- Screenshot konfigurasi dan hasil pengujian tersedia.
- Repository GitHub telah diperbarui.

## 9. Status Deployment

**Planned: Menunggu konfigurasi AWS Learner Lab.**

Konfigurasi, hasil deployment, dan bukti pengujian akan didokumentasikan setelah proses implementasi dilakukan.
