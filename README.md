# Aplikasi Perpustakaan (Desktop MVC Python)

## 📌 Deskripsi Singkat Aplikasi
Aplikasi Perpustakaan adalah perangkat lunak berbasis desktop yang dikembangkan menggunakan arsitektur **Model-View-Controller (MVC)** dengan Python dan antarmuka **CustomTkinter**. Aplikasi ini dirancang untuk memudahkan petugas perpustakaan dalam mengelola data buku, proses autentikasi pengguna, serta manajemen operasional peminjaman buku secara terintegrasi dengan database MySQL.

## 📂 Struktur Direktori MVC
Proyek ini disusun dengan struktur folder modular berikut:
```text
tugas6rpl/
│
├── config/
│   └── database.py        # Konfigurasi koneksi database MySQL
├── controllers/
│   ├── auth_controller.py # Logika kontroler autentikasi & login
│   └── buku_controller.py # Logika kontroler manajemen data buku
├── models/
│   ├── user_model.py      # Operasi database untuk tabel pengguna/auth
│   └── buku_model.py      # Operasi database untuk tabel buku (CRUD)
├── views/
│   ├── login_view.py      # Antarmuka GUI halaman login
│   └── buku_view.py       # Antarmuka GUI manajemen buku
├── tests/
│   ├── test_auth.py       # Unit testing untuk fitur autentikasi
│   └── test_model.py      # Unit testing untuk operasi model buku
├── .github/
│   └── workflows/
│       └── ci_pipeline.yml# Konfigurasi CI/CD GitHub Actions
├── main.py                # Titik masuk utama aplikasi (Entry Point)
├── requirements.txt       # Daftar dependensi proyek
└── README.md              # Dokumentasi teknis proyek

⚙️ Panduan Instalasi & Konfigurasi Database MySQL
1. Buka Proyek: Buka folder proyek Anda di Visual Studio Code.
2. Aktifkan Virtual Environment: Jalankan perintah berikut di terminal PowerShell:
./env/Scripts/activate
3. Instal Dependensi: Pasang seluruh pustaka yang diperlukan:
python -m pip install -r requirements.txt
4. Konfigurasi Database:
a. Nyalakan layanan MySQL melalui aplikasi Laragon.
b. Buat database baru (misalnya db_perpustakaan) dan pastikan pengaturan koneksi di config/database.py sudah sesuai.

🚀 Cara Menjalankan Aplikasi
1. Mode Development (Python): Pastikan virtual environment aktif dan MySQL Laragon menyala, lalu jalankan:
python main.py
2. Mode Standalone (.exe): Masuk ke dalam folder dist/, lalu klik dua kali pada file AplikasiPerpustakaan.exe.

🗃️ Simpan dan Push ke GitHub
Simpan file README.md, lalu simpan perubahan ke Git melalui terminal, dan jalankan perintah berikut satu-persatu:
git add README.md
git commit -m "docs: menambahkan dokumentasi teknis README.md"
git push origin main
