# Lab CTF: Sistem Lupa Siapa yang Login

Ini adalah sebuah lab _Capture The Flag_ (CTF) sederhana yang didesain untuk mempraktikkan celah keamanan **Insecure Direct Object Reference (IDOR)** pada fitur ganti password.

- **Nama Challenge**: sistem lupa siapa yang login
- **Kategori**: Web Security, Broken Access Control
- **Tingkat Kesulitan**: Easy - Medium
- **Tools yang Disarankan**: [Burp Suite](https://portswigger.net/burp)

---

## 🎯 Tujuan Challenge

Tujuan dari lab ini adalah:
1.  Login sebagai pengguna yang sudah ditentukan (`abiyan`).
2.  Menemukan cara untuk mengubah password pengguna lain (misalnya `joshua`).
3.  Login sebagai pengguna yang passwordnya telah diubah.
4.  Menemukan dan mendapatkan _flag_.

Challenge ini secara spesifik mengajarkan bahaya memercayai input dari sisi klien (browser) untuk melakukan aksi sensitif di backend tanpa validasi kepemilikan (authorization).

---

## 🚀 Cara Menjalankan Lab

Pastikan Anda sudah memiliki **Python** dan **pip** terinstal di sistem Anda.

1.  **Clone atau Download Repository**
    Jika ini adalah bagian dari git repo, Anda sudah memilikinya. Jika tidak, pastikan semua file berada dalam satu direktori.

2.  **Setup Virtual Environment (Sangat Direkomendasikan)**
    ```bash
    # Buat virtual environment
    python3 -m venv venv

    # Aktifkan virtual environment
    # Windows
    .\venv\Scripts\activate
    # macOS / Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    Jalankan perintah berikut untuk menginstal Flask:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan Aplikasi Web**
    ```bash
    python3 app.py
    ```

5.  **Akses Lab**
    Buka browser Anda dan kunjungi alamat:
    [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🕵️‍♂️ Panduan Eksploitasi

1.  **Login ke Aplikasi**
    Gunakan kredensial berikut untuk login:
    - **Username**: `admin`
    - **Password**: `admin`

2.  **Konfigurasi Burp Suite**
    - Jalankan Burp Suite.
    - Konfigurasikan browser Anda untuk menggunakan Burp Suite sebagai proxy (default di `127.0.0.1:8080`).
    - Pastikan "Intercept is ON" di tab "Proxy" > "Intercept".

3.  **Lakukan Aksi Ganti Password**
    - Di dalam aplikasi, navigasi ke halaman "Ganti Password".
    - Masukkan password baru (misalnya `passwordbaru123`).
    - Klik tombol "Ubah Password".

4.  **Intercept dan Modifikasi Request**
    - Request akan tertangkap di Burp Suite. Perhatikan body dari request `POST` ke `/change-password`. Anda akan melihat sesuatu seperti ini:
      ```http
      POST /change-password HTTP/1.1
      Host: 127.0.0.1:5000
      [...]

      new_password=passwordbaru123&user_id=0
      ```
    - **Ini adalah celah IDOR-nya.** Aplikasi mengirimkan `user_id` dari klien. Backend tidak memvalidasi apakah `user_id=0` ini benar-benar milik user yang sedang login (`admin`).
    - **Modifikasi `user_id`**. Ubah nilainya dari `0` ke ID user lain. Misalnya, `2` untuk menargetkan user `joshua`.
      ```http
      new_password=passwordbaru123&user_id=2
      ```
    - Klik "Forward" di Burp Suite untuk mengirim request yang sudah dimodifikasi ke server.

5.  **Verifikasi Eksploit dan Dapatkan Flag**
    - Jika berhasil, password user `joshua` (ID 2) kini telah berubah menjadi `passwordbaru123`.
    - Logout dari akun `admin`.
    - Login kembali menggunakan kredensial:
        - **Username**: `joshua`
        - **Password**: `passwordbaru123`
    - Setelah berhasil login sebagai `joshua`, flag akan muncul di halaman profil.
    
---
## 🏁 Flag

Flag akan muncul di halaman profil setelah Anda berhasil login sebagai pengguna lain yang telah Anda kompromikan (bukan user `admin`).

**Flag**: `ITCLUB{P4S5W0RD_NY4S4R_S4L4H_0R4NG}`
