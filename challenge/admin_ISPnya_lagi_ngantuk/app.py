from flask import Flask, render_template, request

app = Flask(__name__)

# Data pelanggan
customer_data = {
    1: {
        "nama": "Denatalle",
        "paket": "ITClubNet Basic",
        "total_tagihan": "Rp 150.000",
        "status_pembayaran": "Lunas",
        "deskripsi": "Internet lancar, cuma malam kadang agak turun.",
        "profil": {
            "alamat": "Jl. Anggrek No. 12, Bandung",
            "nomor_telepon": "0812-3456-7890",
            "tanggal_bergabung": "12 Januari 2023",
            "jumlah_perangkat": 3
        },
        "foto_profil": "https://picsum.photos/id/1/100/100"
    },
    2: {
        "nama": "Alfin",
        "paket": "ITClubNet Bronze",
        "total_tagihan": "Rp 180.000",
        "status_pembayaran": "Belum Lunas",
        "deskripsi": "Tagihan bulan ini kok agak mahal ya?",
        "profil": {
            "alamat": "Gg. Melati V No. 3, Cimahi",
            "nomor_telepon": "0878-1122-3344",
            "tanggal_bergabung": "23 Februari 2023",
            "jumlah_perangkat": 4
        },
        "foto_profil": "https://picsum.photos/id/2/100/100"
    },
    3: {
        "nama": "Alfi",
        "paket": "ITClubNet Bronze",
        "total_tagihan": "Rp 180.000",
        "status_pembayaran": "Lunas",
        "deskripsi": "Tidak ada kendala, terima kasih.",
        "profil": {
            "alamat": "Perumahan Indah Blok C7, Jatinangor",
            "nomor_telepon": "0896-5566-7788",
            "tanggal_bergabung": "05 Maret 2023",
            "jumlah_perangkat": 2
        },
        "foto_profil": "https://picsum.photos/id/3/100/100"
    },
    4: {
        "nama": "Iben",
        "paket": "ITClubNet Silver",
        "total_tagihan": "Rp 250.000",
        "status_pembayaran": "Lunas",
        "deskripsi": "Lumayan buat nge-game online, ping stabil.",
        "profil": {
            "alamat": "Apartemen Bahagia Lt. 10 No. 2, Jakarta",
            "nomor_telepon": "0811-9988-7766",
            "tanggal_bergabung": "18 April 2023",
            "jumlah_perangkat": 5
        },
        "foto_profil": "https://picsum.photos/id/4/100/100"
    },
    5: {
        "nama": "Haikal",
        "paket": "ITClubNet Gold",
        "total_tagihan": "Rp 350.000",
        "status_pembayaran": "Belum Lunas",
        "deskripsi": "Butuh upgrade kecepatan, sering buffering kalau streaming.",
        "profil": {
            "alamat": "Komplek Hijau Asri No. 45, Bekasi",
            "nomor_telepon": "0877-1234-5678",
            "tanggal_bergabung": "01 Mei 2023",
            "jumlah_perangkat": 6
        },
        "foto_profil": "https://picsum.photos/id/5/100/100"
    },
    6: {
        "nama": "Abu Bakar",
        "paket": "ITClubNet Basic",
        "total_tagihan": "Rp 150.000",
        "status_pembayaran": "Lunas",
        "deskripsi": "Pelayanan cepat, teknisi ramah.",
        "profil": {
            "alamat": "Dusun Jaya No. 7, Karawang",
            "nomor_telepon": "0821-0011-2233",
            "tanggal_bergabung": "20 Juni 2023",
            "jumlah_perangkat": 3
        },
        "foto_profil": "https://picsum.photos/id/6/100/100"
    },
    7: {
        "nama": "Kila",
        "paket": "ITClubNet Bronze",
        "total_tagihan": "Rp 180.000",
        "status_pembayaran": "Lunas",
        "deskripsi": "Koneksi stabil banget buat kelas online.",
        "profil": {
            "alamat": "Jl. Pendidikan III No. 1, Bogor",
            "nomor_telepon": "0857-4433-2211",
            "tanggal_bergabung": "09 Juli 2023",
            "jumlah_perangkat": 2
        },
        "foto_profil": "https://picsum.photos/id/7/100/100"
    },
    8: {
        "nama": "Tiara",
        "paket": "ITClubNet Silver",
        "total_tagihan": "Rp 250.000",
        "status_pembayaran": "Belum Lunas",
        "deskripsi": "Minggu lalu sempat putus nyambung, mohon dicek.",
        "profil": {
            "alamat": "Kampung Damai RT 01 RW 02, Depok",
            "nomor_telepon": "0813-8877-6655",
            "tanggal_bergabung": "15 Agustus 2023",
            "jumlah_perangkat": 4
        },
        "foto_profil": "https://picsum.photos/id/8/100/100"
    },
    9: {
        "nama": "Joshua",
        "paket": "ITClubNet Gold",
        "total_tagihan": "Rp 350.000",
        "status_pembayaran": "Lunas",
        "deskripsi": "Oh iya, yang dimaksud itu namanya leet. Biasanya dipakai buat username atau kode tertentu.",
        "profil": {
            "alamat": "Jl. Mawar Merah No. 19, Yogyakarta",
            "nomor_telepon": "0815-1234-9876",
            "tanggal_bergabung": "03 September 2023",
            "jumlah_perangkat": 5
        },
        "foto_profil": "https://picsum.photos/id/9/100/100"
    },
    10: {
        "nama": "Samuel",
        "paket": "ITClubNet Basic",
        "total_tagihan": "Rp 150.000",
        "status_pembayaran": "Lunas",
        "deskripsi": "Oke lah, sesuai harga.",
        "profil": {
            "alamat": "Kost Pelangi No. 8, Solo",
            "nomor_telepon": "0899-7654-3210",
            "tanggal_bergabung": "28 September 2023",
            "jumlah_perangkat": 1
        },
        "foto_profil": "https://picsum.photos/id/10/100/100"
    },
    11: {
        "nama": "Syahrul",
        "paket": "ITClubNet Bronze",
        "total_tagihan": "Rp 180.000",
        "status_pembayaran": "Belum Lunas",
        "deskripsi": "Pembayaran menunggu gaji turun.",
        "profil": {
            "alamat": "Kontrakan Kuning No. 2, Semarang",
            "nomor_telepon": "0856-1122-3344",
            "tanggal_bergabung": "10 Oktober 2023",
            "jumlah_perangkat": 3
        },
        "foto_profil": "https://picsum.photos/id/11/100/100"
    },
    12: {
        "nama": "Dimas",
        "paket": "ITClubNet Silver",
        "total_tagihan": "Rp 250.000",
        "status_pembayaran": "Lunas",
        "deskripsi": "Kemarin ngobrol sama temen soal angka yang sering dipakai anak IT. Katanya angka bisa gantiin huruf biar keliatan keren.",
        "profil": {
            "alamat": "Griya Sejahtera Blok A1, Surabaya",
            "nomor_telepon": "0817-0099-8877",
            "tanggal_bergabung": "25 Oktober 2023",
            "jumlah_perangkat": 4
        },
        "foto_profil": "https://picsum.photos/id/12/100/100"
    },
    13: {
        "nama": "Darwin",
        "paket": "ITClubNet Gold",
        "total_tagihan": "Rp 350.000",
        "status_pembayaran": "Lunas",
        "deskripsi": "Puasa nge-game dulu, fokus UNBK.",
        "profil": {
            "alamat": "Jl. Ilmuwan No. 7, Malang",
            "nomor_telepon": "0818-4455-6677",
            "tanggal_bergabung": "08 November 2023",
            "jumlah_perangkat": 2
        },
        "foto_profil": "https://picsum.photos/id/13/100/100"
    },
    14: {
        "nama": "Kenken",
        "paket": "ITClubNet Basic",
        "total_tagihan": "Rp 150.000",
        "status_pembayaran": "Belum Lunas",
        "deskripsi": "Mau bayar tapi lupa nomor tagihan.",
        "profil": {
            "alamat": "Jl. Pahlawan No. 34, Denpasar",
            "nomor_telepon": "0895-0011-2233",
            "tanggal_bergabung": "17 November 2023",
            "jumlah_perangkat": 1
        },
        "foto_profil": "https://picsum.photos/id/14/100/100"
    },
    15: {
        "nama": "Aril",
        "paket": "ITClubNet Bronze",
        "total_tagihan": "Rp 180.000",
        "status_pembayaran": "Lunas",
        "deskripsi": "Makasih ITClubNet!",
        "profil": {
            "alamat": "Gang Sempit No. 1, Makassar",
            "nomor_telepon": "0822-9988-7766",
            "tanggal_bergabung": "01 Desember 2023",
            "jumlah_perangkat": 3
        },
        "foto_profil": "https://picsum.photos/id/15/100/100"
    },
    16: {
        "nama": "Azril",
        "paket": "ITClubNet Silver",
        "total_tagihan": "Rp 250.000",
        "status_pembayaran": "Lunas",
        "deskripsi": "Sering dipakai buat streaming, lancar jaya.",
        "profil": {
            "alamat": "Komp. Cendrawasih No. 5, Balikpapan",
            "nomor_telepon": "0816-5544-3322",
            "tanggal_bergabung": "14 Desember 2023",
            "jumlah_perangkat": 5
        },
        "foto_profil": "https://picsum.photos/id/16/100/100"
    },
    17: {
        "nama": "Nazril",
        "paket": "ITClubNet Gold",
        "total_tagihan": "Rp 350.000",
        "status_pembayaran": "Belum Lunas",
        "deskripsi": "Tolong perpanjang masa aktif, belum bisa bayar.",
        "profil": {
            "alamat": "Desa Makmur RT 03 RW 01, Samarinda",
            "nomor_telepon": "0876-1234-5678",
            "tanggal_bergabung": "26 Desember 2023",
            "jumlah_perangkat": 4
        },
        "foto_profil": "https://picsum.photos/id/17/100/100"
    },
    18: {
        "nama": "Fahri",
        "paket": "ITClubNet Basic",
        "total_tagihan": "Rp 150.000",
        "status_pembayaran": "Lunas",
        "deskripsi": "Sudah saya transfer ya.",
        "profil": {
            "alamat": "Jl. Protokol Utama No. 8, Pontianak",
            "nomor_telepon": "0823-9900-1122",
            "tanggal_bergabung": "05 Januari 2024",
            "jumlah_perangkat": 2
        },
        "foto_profil": "https://picsum.photos/id/18/100/100"
    },
    19: {
        "nama": "Farhan",
        "paket": "ITClubNet Bronze",
        "total_tagihan": "Rp 180.000",
        "status_pembayaran": "Lunas",
        "deskripsi": "Untuk bulan depan otomatis debet aja.",
        "profil": {
            "alamat": "Taman Kota Indah No. 11, Padang",
            "nomor_telepon": "0852-7766-5544",
            "tanggal_bergabung": "18 Januari 2024",
            "jumlah_perangkat": 3
        },
        "foto_profil": "https://picsum.photos/id/19/100/100"
    },
    1337: {
        "nama": "Abiyan",
        "paket": "ITClubNet Core Access",
        "total_tagihan": "Rp 999.999",
        "status_pembayaran": "Lunas",
        "deskripsi": "Admin ISP lagi ngantuk. ID sensitif kebuka semua. Kalau kamu bisa baca ini, berarti kamu paham IDOR.",
        "flag": "ITCLUB{IDOR_4dm1n_L4g1_Ng4ntuk}",
        "profil": {
            "alamat": "Pusat Data Rahasia, Jakarta",
            "nomor_telepon": "0800-1337-1337", # Special number for admin
            "tanggal_bergabung": "01 Januari 2022",
            "jumlah_perangkat": 99 # Many devices for admin
        },
        "foto_profil": "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&s=100" # Generic admin avatar
    },
    20: {
        "nama": "Ilham",
        "paket": "ITClubNet Silver",
        "total_tagihan": "Rp 250.000",
        "status_pembayaran": "Belum Lunas",
        "deskripsi": "Lupa bayar, minggu depan saya urus.",
        "profil": {
            "alamat": "Jl. Harapan Bangsa No. 22, Medan",
            "nomor_telepon": "0811-2345-6789",
            "tanggal_bergabung": "03 Februari 2024",
            "jumlah_perangkat": 4
        },
        "foto_profil": "https://picsum.photos/id/20/100/100"
    },
    21: {
        "nama": "Phasa",
        "paket": "ITClubNet Gold",
        "total_tagihan": "Rp 350.000",
        "status_pembayaran": "Lunas",
        "deskripsi": "Internet cepat, mantap buat kerja remote.",
        "profil": {
            "alamat": "Komplek Elite Permai Blok B, Palembang",
            "nomor_telepon": "0877-9876-5432",
            "tanggal_bergabung": "10 Februari 2024",
            "jumlah_perangkat": 6
        },
        "foto_profil": "https://picsum.photos/id/21/100/100"
    },
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tagihan")
def tagihan():
    customer_id = request.args.get("id")
    
    if not customer_id:
        return render_template("tagihan.html", error_message="Parameter ID tidak ditemukan.")

    try:
        customer_id = int(customer_id)
    except ValueError:
        return render_template("tagihan.html", error_message="ID tagihan tidak valid.")

    customer = customer_data.get(customer_id)

    if not customer:
        return render_template("tagihan.html", error_message="Data tagihan tidak ditemukan.")

    # Pass the customer data and flag (if applicable) to the template
    return render_template("tagihan.html", customer=customer, customer_id=customer_id)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
