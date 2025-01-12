# Patani Backend

Backend **Patani** adalah inti dari aplikasi yang mengelola proses autentikasi, manajemen data, dan integrasi API untuk menghubungkan investor dengan petani. Proyek ini dikembangkan menggunakan **Django** dan **Django REST Framework** untuk membangun RESTful API yang skalabel.

---

## 🚀 Fitur Utama

- **Autentikasi JWT**: Menggunakan `djangorestframework-simplejwt` untuk autentikasi berbasis token yang aman.
- **Manajemen API**: Endpoint untuk mengelola data pengguna, proyek, dan investasi.
- **Cross-Origin Resource Sharing (CORS)**: Dukungan CORS untuk frontend dan backend komunikasi.
- **Media Handling**: Mengelola file media (gambar atau dokumen) dengan bantuan `Pillow`.
- **Statis dan Media**: `Whitenoise` digunakan untuk pengelolaan file statis dan media.
- **Asynchronous Support**: Menggunakan `asgiref` untuk menangani operasi asynchronous.

---

## 🛠️ Teknologi yang Digunakan

- **Framework**: [Django](https://www.djangoproject.com/) (v5.1.3)
- **REST API**: [Django REST Framework](https://www.django-rest-framework.org/) (v3.15.2)
- **Autentikasi**: [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/) (v5.3.1)
- **File Management**: [Pillow](https://python-pillow.org/) (v11.0.0)
- **Server**: [Gunicorn](https://gunicorn.org/) (v23.0.0)
- **CORS Handling**: [django-cors-headers](https://pypi.org/project/django-cors-headers/) (v4.6.0)
- **Static Files**: [Whitenoise](http://whitenoise.evans.io/) (v6.8.2)

---

## 📦 Instalasi dan Setup

### 1. Clone Repository
```bash
git clone https://github.com/faiqmubarok/backend-capstone-project-msib.git
cd backend-capstone-project-msib
```

### 2. Buat Virtual Environment
```bash
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Environment
Buat file `.env` di root proyek dan tambahkan konfigurasi berikut:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3  # Sesuaikan jika menggunakan database lain
```

### 5. Jalankan Migrasi Database
```bash
python manage.py migrate
```

### 6. Jalankan Server
```bash
python manage.py runserver
```

Buka aplikasi di browser di `http://127.0.0.1:8000`.

---

## 📋 Endpoints API

### Contoh Endpoints
| Method | Endpoint                      | Deskripsi                           |
|--------|-------------------------------|-------------------------------------|
| POST   | /users/register/              | Mendaftarkan akun                   |
| POST   | /users/login/                 | Masuk ke akun                       |
| GET    | /projects/allProject/         | Mendapatkan seluruh proyek          |
| POST   | /transactions/topup/          | Membuat transaksi baru              |
| GET    | /getTransaction/<int:userId>/ | Mendapatkan data transaksi user     |

Detail lebih lanjut tersedia di dokumentasi API (maintenance).

---

## 📁 Struktur Direktori

```plaintext
backend-capstone-project-msib/
├── patani/           # Direktori utama proyek Django
│   ├── settings.py   # Konfigurasi aplikasi
│   ├── urls.py       # Routing aplikasi
│   └── wsgi.py       # File WSGI untuk deploy
├── api/              # Aplikasi Django untuk API
│   ├── models.py     # Model database
│   ├── views.py      # Logika endpoint
│   ├── serializers.py # Serialisasi data
│   └── urls.py       # Routing endpoint API
├── manage.py         # File manajemen proyek Django
├── requirements.txt  # File dependencies Python
└── .env              # File konfigurasi environment
```

---

## 🌐 Deployment

### Gunicorn
Gunakan Gunicorn untuk menjalankan aplikasi:
```bash
gunicorn patani.wsgi
```

### Static Files
Pastikan file statis di-collect sebelum deploy:
```bash
python manage.py collectstatic
```

### Whitenoise
Tambahkan middleware berikut di `settings.py` untuk mendukung file statis:
```python
MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # Middleware lainnya...
]
```

---

## 🤝 Kontribusi

1. Fork repository ini.
2. Buat branch fitur baru:
   ```bash
   git checkout -b fitur-anda
   ```
3. Commit perubahan Anda:
   ```bash
   git commit -m "Menambahkan fitur baru"
   ```
4. Push branch Anda:
   ```bash
   git push origin fitur-anda
   ```
5. Buat Pull Request.

---

## 📧 Kontak

Jika ada pertanyaan, hubungi kami di [faiqmubarok@gmail.com](mailto:faiqmubarok@gmail.com).

---

Selamat Berkarya! 🌱
