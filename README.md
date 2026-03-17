# 🚩 IT Club CTF Labs - SMK 1 TRIPLE "J"

![CTF Banner](https://img.shields.io/badge/CTF-Challenge--Labs-red?style=for-the-badge&logo=target)
![Category](https://img.shields.io/badge/Category-Web--Exploitation-blue?style=for-the-badge)
![Vulnerability](https://img.shields.io/badge/Focus-IDOR--%26--Logic--Flaw-orange?style=for-the-badge)
![School](https://img.shields.io/badge/SMK-1--TRIPLE--J-green?style=for-the-badge)

Selamat datang di **IT Club CTF Labs**! Repositori ini berisi kumpulan lab praktik *Capture The Flag* (CTF) yang dirancang khusus untuk anggota **IT Club SMK 1 TRIPLE "J"**.

---

## 🚧 Status Proyek & Roadmap

> [!IMPORTANT]
> Proyek ini **masih dalam tahap pengembangan**. Saat ini jumlah challenge masih terbatas dan berfokus pada kategori *Web Exploitation*.

Kami berencana untuk terus menambahkan challenge yang lebih bervariatif di masa mendatang, meliputi kategori:
- 🕵️ **Digital Forensics** (Analisis file, disk, dan network)
- ⚔️ **Pwn / Binary Exploitation** (Eksploitasi memory corruptions)
- 🔓 **Reverse Engineering** (Analisis mendalam terhadap binary)
- 🔐 **Cryptography** (Pemecahan sandi dan enkripsi)
- 🌐 **OSINT** (Open Source Intelligence)

---

## 🚀 Fitur Utama

- 🐳 **Dockerized**: Semua lab dan platform CTFd berjalan di dalam container Docker.
- 🎯 **Fokus Materi**: Terfokus pada kerentanan web modern (IDOR, Price Manipulation, dsb).
- 🏆 **Integrated Platform**: Menggunakan **CTFd** sebagai dashboard skor dan manajemen flag.

---

## 📂 Daftar Challenge (Lab)

Projek ini mencakup 5 Lab utama yang merepresentasikan berbagai skenario dunia nyata:

| Lab | Nama Challenge | Port | Deskripsi Singkat |
| :--- | :--- | :--- | :--- |
| **Lab 1** | `admin_ISPnya_lagi_ngantuk` | `5001` | Eksploitasi sistem invoice pada layanan ISP. |
| **Lab 2** | `BayarSeiklhasnya` | `5002` | Manipulasi harga tiket/barang pada sistem pembayaran. |
| **Lab 3** | `DompetTanpaPemilik` | `5003` | Kerentanan pada sistem transfer saldo dompet digital. |
| **Lab 4** | `orderan_gue_malah_alamat_orang` | `5004` | Manipulasi alamat pengiriman pada sistem e-commerce. |
| **Lab 5** | `sistem_lupa_siapa_yang_login` | `5005` | Kerentanan pada manajemen profile dan ganti password. |

> **Note:** Dashboard Utama (CTFd) berjalan pada port `:8000`.

---

## 🛠️ Cara Menjalankan Lab

Pastikan Anda sudah menginstal **Docker** dan **Docker Compose** di komputer Anda.

1. **Clone Repositori**
   ```bash
   git clone https://github.com/abyfromheaven/ITClubCTFLabs.git
   cd ITClubCTFLabs
   ```

2. **Build & Jalankan Container**
   ```bash
   docker-compose up -d --build
   ```

3. **Akses Lab**
   - **Dashboard Skor (CTFd):** `http://localhost:8000`
   - **Lab Challenges:** `http://localhost:5001` s/d `http://localhost:5005`

---

## 🧪 Tech Stack

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

---

## 📖 Konsep Pembelajaran

Lab ini dirancang untuk mengajarkan bagaimana seorang penyerang dapat memanipulasi parameter (seperti `id`, `user_id`, `price`, dll) untuk mengakses data milik pengguna lain atau mengubah logika bisnis aplikasi.

**Materi yang dicakup:**
- URL ID Parameter Manipulation
- Price & Amount Manipulation
- Insecure Password Change Flow
- Unauthorized Money Transfer
- Address Entry/Profile IDOR

---

## 👨‍💻 Kontributor

Dibuat dengan ❤️ untuk **IT Club SMK 1 TRIPLE "J"**.

---
*Keep Hacking, Stay Legal!* 🛡️
