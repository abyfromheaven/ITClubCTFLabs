# CTF Lab: Dompet Tanpa Pemilik

## Story Challenge

IT Club sedang dalam persiapan untuk menyelenggarakan sebuah event besar, dan dana operasionalnya disimpan di sistem wallet internal yang baru.

Sistem ini dirancang untuk terlihat sangat aman. Role pengguna didefinisikan dengan jelas, dan akses tampaknya dibatasi dengan ketat sesuai dengan peran masing-masing anggota. Sepintas, semuanya terlihat solid dan terpercaya.

Namun, Anda, sebagai anggota biasa, menemukan sebuah celah logika yang mendasar. Sistem ini ternyata lebih mempercayai data yang dikirimkan dari sisi pengguna daripada memverifikasi identitas asli user yang sedang login.

Jika celah ini benar-benar ada dan bisa dieksploitasi, seluruh rencana event besar IT Club bisa gagal total karena penyalahgunaan dana.

**Buktikan celah itu.** Kuras saldo bendahara sampai habis dan temukan flag-nya.

## Goal

Tugas Anda adalah mengekspos kelemahan fundamental sistem ini.

**Goal utama: Kuras saldo dari akun bendahara (**Tiara**) hingga mencapai nol.**

Anda harus melakukannya sebagai anggota biasa, tanpa memerlukan akses admin, dan tanpa bypass mekanisme login. Eksploitasi harus terjadi murni karena kelemahan logika pada sistem.

## Kondisi Sukses

Flag akan muncul di dashboard **akun Anda** hanya jika **kedua kondisi** berikut terpenuhi secara bersamaan:

1.  Saldo pada akun bendahara (`Tiara`) telah mencapai **Rp 0**.
2.  Saldo pada akun Anda sendiri telah meningkat secara signifikan sebagai hasilnya.

Ini untuk memastikan bahwa Anda benar-benar memahami dan berhasil mengeksploitasi alur serangan secara penuh.

## Lingkungan Lab

### Prasyarat
- Python 3
- `pip` (package installer for Python)

### 1. Instalasi Dependensi
Buka terminal di direktori proyek ini dan jalankan perintah berikut:

```bash
pip install -r requirements.txt
```

### 2. Menjalankan Server
Setelah instalasi selesai, jalankan server Flask dengan perintah:

```bash
flask run --port 5001
```
Atau bisa juga dengan:
```bash
python3 app.py
```

### 3. Akses Aplikasi
Buka browser Anda dan kunjungi alamat:

[http://127.0.0.1:5001](http://127.0.0.1:5001)

Untuk memulai, login sebagai **Phasa Turing**. Username dan password adalah `Phasa Turing` dan `kolot123`.

### 4. Reset Lingkungan
Jika Anda ingin mengulang lab dari awal (mengembalikan semua saldo dan riwayat transaksi ke kondisi semula), Anda bisa mengunjungi endpoint `/reset`:

[http://127.0.0.1:5001/reset](http://127.0.0.1:5001/reset)

Endpoint ini akan mengembalikan semua state lab dan mengarahkan Anda kembali ke halaman login.