# DAG Sederhana ETL dengan Apache Airflow 🌀

Repositori ini berisi implementasi DAG sederhana untuk proses **ETL (Extract, Transform, Load)** menggunakan **Apache Airflow** dan **PostgreSQL**.

## 📌 Deskripsi Singkat

ETL ini terdiri dari tiga tahapan:

1. **Extract**  
   Mengambil data dari tabel `retail_raw` di database PostgreSQL (`source_db`) dan menyimpannya sebagai file `retail_extract.csv`.

2. **Transform**  
   Melakukan transformasi sederhana pada data:
   - Menghitung `TotalPrice` (`Quantity * UnitPrice`)
   - Menghapus baris kosong

3. **Load**  
   Memasukkan data yang telah dibersihkan ke dalam tabel `retail_mart` sebagai _data mart_.

## 🛠️ Teknologi yang Digunakan

- Apache Airflow 2.8.1 (via Docker)
- PostgreSQL 13
- Python (pandas, psycopg2)
- Docker & Docker Compose

## 📁 Struktur Folder

```
airflow-docker/
│
├── dags/
│   └── etl_retail.py          # DAG utama untuk proses ETL
├── retail-data.csv            # Data mentah awal
├── .env                       # Konfigurasi lingkungan Airflow & PostgreSQL
├── docker-compose.yml         # Menjalankan Airflow & PostgreSQL via Docker
└── README.md                  # Dokumentasi proyek
```

## 🚀 Cara Menjalankan Proyek Ini

> 💡 Pastikan Docker dan Docker Compose sudah terinstal di laptop kamu.

### 1. Clone repository
```bash
git clone https://github.com/dwmhr12/dag_sederhana.git
cd dag_sederhana
```

### 2. Jalankan Docker Compose
```bash
sudo docker-compose up -d
```

### 3. Akses Airflow
Buka browser dan kunjungi:  
[http://localhost:8080](http://localhost:8080)  
Login:
- **Username:** `airflow`
- **Password:** `airflow`

### 4. Jalankan DAG
Masuk ke tab DAGs → Aktifkan `etl_retail_dag` → Klik **Trigger DAG** untuk menjalankan secara manual.

## 🧪 Verifikasi Hasil

Untuk cek isi tabel hasil (`retail_mart`), lakukan:

```bash
# Masuk ke container PostgreSQL
sudo docker exec -it postgres psql -U airflow

# Ganti ke database source_db
\c source_db

# Lihat isi tabel retail_mart
SELECT * FROM retail_mart LIMIT 5;

# Lihat daftar tabel di database
\dt
```

## 🙋‍♀️ Penulis

**Dewi Maharani**  
📍 [GitHub @dwmhr12](https://github.com/dwmhr12)

---

## 📌 Catatan Tambahan

- Dataset dummy `retail-data.csv` dimasukkan terlebih dahulu ke PostgreSQL sebagai tabel `retail_raw`.
- Proses ETL dilakukan seluruhnya menggunakan `PythonOperator`.
- Output akhir masuk ke `retail_mart` sebagai bentuk data mart hasil transformasi.

