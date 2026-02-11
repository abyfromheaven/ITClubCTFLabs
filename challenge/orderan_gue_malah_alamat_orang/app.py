from flask import Flask, render_template, request, session, flash, g, jsonify
import os
import datetime

app = Flask(__name__)
# Gunakan secret key tetap untuk CTF
app.secret_key = 'super_secret_ctf_key'

# 1. DATA IN-MEMORY
# Data user (hardcoded)
users = {
  1: {"username": "abiyan", "password": "password"},
  2: {"username": "joshua", "password": "password"},
  3: {"username": "phasa", "password": "password"},
  4: {"username": "tiara", "password": "password"},
  5: {"username": "kila", "password": "password"},
  6: {"username": "haykal", "password": "password"}
}

# Data alamat (disimpan per user ID)
# Akan diisi via UI oleh user, atau pre-populated untuk dummy users
addresses = {
    1: {"full_name": "Manis Abiyan", "street": "Jl. Merdeka No. 10", "city": "Jakarta", "postal_code": "10110", "phone": "081234567890"},
    2: {"full_name": "Joshua Susilo", "street": "Jl. Pahlawan No. 5", "city": "Surabaya", "postal_code": "60271", "phone": "081298765432"},
    3: {"full_name": "Phasa Turink", "street": "Jl. Diponegoro No. 20", "city": "Bandung", "postal_code": "40115", "phone": "085712345678"},
    4: {"full_name": "Tiara Sari", "street": "Jl. Gajah Mada No. 12", "city": "Semarang", "postal_code": "50134", "phone": "087811223344"},
    5: {"full_name": "Kila Putri", "street": "Jl. Sudirman No. 7", "city": "Yogyakarta", "postal_code": "55281", "phone": "089655667788"},
    6: {"full_name": "Haykal Setiaone", "street": "Jl. Kebon Jeruk No. 3", "city": "Jakarta Barat", "postal_code": "11530", "phone": "081112223333"} # Haykal's pre-populated address
}

# Data produk
products = [
  {
    "id": 1,
    "name": "IoT Starter Kit",
    "price": "Rp 850.000",
    "description": "Paket dasar untuk mempelajari Internet of Things, termasuk ESP32, sensor suhu, sensor kelembaban, breadboard, dan kabel jumper. Ideal untuk pemula.",
    "image": "https://images.unsplash.com/photo-1614064641938-3bbee52942c7?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "iot"
  },
  {
    "id": 2,
    "name": "Network Lab Kit",
    "price": "Rp 1.200.000",
    "description": "Peralatan lengkap untuk membangun dan mengkonfigurasi jaringan kecil, berisi router mikrotik, kabel UTP, konektor RJ45, crimping tools, dan LAN tester.",
    "image": "https://images.unsplash.com/photo-1593640408182-31c70c8268f5?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "networking"
  },
  {
    "id": 3,
    "name": "Server Rack Cabinet",
    "price": "Rp 3.500.000",
    "description": "Rak kabinet server standar 19 inci, tinggi 42U, dilengkapi dengan pendingin aktif dan pintu tempered glass. Cocok untuk data center skala kecil hingga menengah.",
    "image": "https://images.unsplash.com/photo-1629654291660-3c98113a0438?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "pc-build"
  },
  {
    "id": 4,
    "name": "Fiber Optic Splicer",
    "price": "Rp 15.000.000",
    "description": "Alat penyambung kabel fiber optik otomatis berpresisi tinggi, lengkap dengan cleaver, striper, dan power meter. Essential untuk instalasi jaringan FTTx.",
    "image": "https://images.unsplash.com/photo-1591696205602-2f950c417cb1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "networking"
  },
  {
    "id": 5,
    "name": "Security Camera System",
    "price": "Rp 4.800.000",
    "description": "Sistem kamera pengawas CCTV IP resolusi 4K, dilengkapi dengan 4 kamera outdoor, NVR 8 channel, hard drive 2TB, dan PoE switch. Instalasi mudah.",
    "image": "https://images.unsplash.com/photo-1541140532154-b024d705b90a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "security"
  },
    {
    "id": 6,
    "name": "WiFi Pentesting Kit",
    "price": "Rp 2.500.000",
    "description": "Kit lengkap untuk testing keamanan jaringan WiFi, termasuk adapter monitor mode, antena directional, dan software khusus.",
    "image": "https://images.unsplash.com/photo-1614064641938-3bbee52942c7?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "pentesting"
  },
  {
    "id": 7,
    "name": "Raspberry Pi Pentesting Bundle",
    "price": "Rp 1.800.000",
    "description": "Raspberry Pi 4 dengan Kali Linux pre-installed, case khusus, power bank, dan berbagai alat pentesting portabel.",
    "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "pentesting"
  },
  {
    "id": 8,
    "name": "USB Rubber Ducky Professional",
    "price": "Rp 950.000",
    "description": "Alat pentesting berbasis USB yang dapat menjalankan script keystroke injection untuk testing keamanan fisik.",
    "image": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "pentesting"
  },
  {
    "id": 9,
    "name": "HackRF One SDR",
    "price": "Rp 4.200.000",
    "description": "Software Defined Radio untuk analisis dan testing keamanan sinyal radio, komunikasi wireless, dan RF security.",
    "image": "https://images.unsplash.com/photo-1591696205602-2f950c417cb1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "pentesting"
  },
  {
    "id": 10,
    "name": "LAN Turtle Covert",
    "price": "Rp 1.250.000",
    "description": "Alat pentesting jaringan yang menyamar sebagai adapter Ethernet, untuk testing keamanan jaringan internal.",
    "image": "https://images.unsplash.com/photo-1551650975-87deedd944c3?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "pentesting"
  },
  {
    "id": 11,
    "name": "Proxmark3 RFID Tool",
    "price": "Rp 2.800.000",
    "description": "Alat untuk testing keamanan kartu RFID/NFC, cloning, dan analisis sistem keamanan berbasis frekuensi radio.",
    "image": "https://images.unsplash.com/photo-1629654291660-3c98113a0438?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "pentesting"
  },
  {
    "id": 12,
    "name": "Bad USB Attack Tool",
    "price": "Rp 850.000",
    "description": "Alat pentesting USB yang dapat menyamar sebagai berbagai perangkat USB untuk testing keamanan fisik.",
    "image": "https://images.unsplash.com/photo-1581094794329-c8112a89af12?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "pentesting"
  },
  {
    "id": 13,
    "name": "WiFi Pineapple Nano",
    "price": "Rp 3.500.000",
    "description": "Alat pentesting WiFi profesional untuk melakukan berbagai serangkaian testing keamanan jaringan wireless.",
    "image": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "pentesting"
  },
  {
    "id": 14,
    "name": "Gaming PC RTX 4070",
    "price": "Rp 25.000.000",
    "description": "PC gaming lengkap dengan RTX 4070, Intel i7-13700K, 32GB RAM DDR5, 1TB NVMe SSD, dan casing RGB premium.",
    "image": "https://images.unsplash.com/photo-1593640408182-31c70c8268f5?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "pc-build"
  },
  {
    "id": 15,
    "name": "Workstation PC untuk Developer",
    "price": "Rp 18.500.000",
    "description": "PC workstation dengan AMD Ryzen 9, 64GB RAM, 2TB NVMe SSD, dan GPU workstation untuk development dan rendering.",
    "image": "https://images.unsplash.com/photo-1569779213435-ba3167dde7cc?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "pc-build"
  },
  {
    "id": 16,
    "name": "Mini ITX Compact Build",
    "price": "Rp 12.750.000",
    "description": "PC kecil bertenaga dengan casing Mini ITX, AMD Ryzen 5, GTX 3060, 16GB RAM, dan 512GB SSD untuk space terbatas.",
    "image": "https://images.unsplash.com/photo-1593341646782-e0b495cff86d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "pc-build"
  },
  {
    "id": 17,
    "name": "Budget Gaming PC RX 6600",
    "price": "Rp 9.500.000",
    "description": "PC gaming harga terjangkau dengan AMD Ryzen 5, RX 6600, 16GB RAM, 512GB SSD untuk gaming 1080p dengan harga terbaik.",
    "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "pc-build"
  },
  {
    "id": 18,
    "name": "Streaming PC Dual PC Setup",
    "price": "Rp 32.000.000",
    "description": "Setup streaming lengkap dengan dua PC, capture card Elgato, microphone profesional, dan lighting kit.",
    "image": "https://images.unsplash.com/photo-1542744094-3a31f272c490?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "pc-build"
  },
  {
    "id": 19,
    "name": "Custom Water Cooling Kit",
    "price": "Rp 5.500.000",
    "description": "Kit lengkap untuk rakitan custom water cooling termasuk radiator, pump, reservoir, tubing, fittings, dan coolant.",
    "image": "https://images.unsplash.com/photo-1587202372634-32705e3bf49c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "pc-build"
  },
  {
    "id": 20,
    "name": "Mechanical Keyboard Custom",
    "price": "Rp 1.200.000",
    "description": "Keyboard mechanical custom dengan switch Gateron, keycaps PBT, RGB lighting, dan PCB hot-swappable.",
    "image": "https://images.unsplash.com/photo-1591488320449-011701bb6704?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "pc-build"
  },
  {
    "id": 21,
    "name": "Monitor Gaming 27\" 144Hz",
    "price": "Rp 4.800.000",
    "description": "Monitor gaming 27 inch dengan refresh rate 144Hz, 1ms response time, FreeSync, dan resolusi QHD untuk pengalaman gaming terbaik.",
    "image": "https://images.unsplash.com/photo-1541140532154-b024d705b90a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "pc-build"
  },
  {
    "id": 22,
    "name": "Kit Sensor IoT Lengkap",
    "price": "Rp 500.000",
    "description": "Kit lengkap untuk proyek Internet of Things, termasuk berbagai sensor, microcontroller, dan modul komunikasi.",
    "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "iot"
  },
  {
    "id": 23,
    "name": "Smart Home Hub Pro",
    "price": "Rp 750.000",
    "description": "Perangkat kontrol rumah pintar dengan integrasi voice assistant, aplikasi mobile, dan kompatibilitas luas.",
    "image": "https://images.unsplash.com/photo-1581094794329-c8112a89af12?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "iot"
  },
  {
    "id": 24,
    "name": "Raspberry Pi 4 Kit",
    "price": "Rp 1.200.000",
    "description": "Kit starter Raspberry Pi 4 dengan case, power supply, microSD card, dan aksesori untuk proyek IoT.",
    "image": "https://images.unsplash.com/photo-1620288627223-53302f4e8c74?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "iot"
  },
  {
    "id": 25,
    "name": "Smart Lighting System",
    "price": "Rp 1.500.000",
    "description": "Sistem pencahayaan pintar dengan kontrol via smartphone, voice command, dan otomatisasi jadwal.",
    "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "iot"
  },
  {
    "id": 26,
    "name": "USB Drive Terenkripsi 256GB",
    "price": "Rp 400.000",
    "description": "USB drive dengan enkripsi AES-256 dan keypad untuk keamanan data tingkat tinggi.",
    "image": "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "security"
  },
  {
    "id": 27,
    "name": "Hardware Security Key FIDO2",
    "price": "Rp 300.000",
    "description": "Kunci keamanan fisik dengan standar FIDO2 untuk autentikasi tanpa password yang aman.",
    "image": "https://images.unsplash.com/photo-1527814050087-3793815479db?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "security"
  },
  {
    "id": 28,
    "name": "VPN Router Enterprise",
    "price": "Rp 900.000",
    "description": "Router dengan dukungan VPN built-in, firewall, dan manajemen jaringan yang aman.",
    "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "security"
  },
  {
    "id": 29,
    "name": "SSD Terenkripsi 1TB",
    "price": "Rp 1.800.000",
    "description": "SSD internal dengan enkripsi hardware AES-256 untuk keamanan data maksimal pada PC/laptop.",
    "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "security"
  },
  {
    "id": 30,
    "name": "Arduino Ultimate Starter Kit",
    "price": "Rp 600.000",
    "description": "Kit lengkap untuk belajar pemrograman embedded dengan Arduino, termasuk board, sensor, dan komponen.",
    "image": "https://images.unsplash.com/photo-1516116216624-53e697fedbea?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "programming"
  },
  {
    "id": 31,
    "name": "ESP32 Development Board",
    "price": "Rp 450.000",
    "description": "Papan pengembangan ESP32 dengan WiFi dan Bluetooth untuk proyek IoT dan pemrograman embedded.",
    "image": "https://images.unsplash.com/photo-1633356122102-3fe601e05bd2?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "programming"
  },
  {
    "id": 32,
    "name": "Buku Pemrograman Python Expert",
    "price": "Rp 150.000",
    "description": "Buku fisik dan digital untuk belajar Python dari dasar hingga tingkat lanjut dengan studi kasus nyata.",
    "image": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "programming"
  },
  {
    "id": 33,
    "name": "Raspberry Pi Pico Kit",
    "price": "Rp 350.000",
    "description": "Kit untuk belajar pemrograman microcontroller dengan Raspberry Pi Pico dan MicroPython/C++.",
    "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "programming"
  },
  {
    "id": 34,
    "name": "Router WiFi 6 Gaming",
    "price": "Rp 800.000",
    "description": "Router WiFi 6 dengan kecepatan tinggi, optimasi gaming, dan cakupan luas untuk rumah dan kantor.",
    "image": "https://images.unsplash.com/photo-1601643157091-ce5c0bb8c7b8?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "networking"
  },
  {
    "id": 35,
    "name": "Kabel Ethernet Cat6a (15m)",
    "price": "Rp 100.000",
    "description": "Kabel jaringan berkualitas tinggi dengan shielding untuk performa maksimal dan bebas gangguan.",
    "image": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "networking"
  },
  {
    "id": 36,
    "name": "WiFi Extender Mesh",
    "price": "Rp 250.000",
    "description": "Perluas jangkauan WiFi Anda dengan sistem mesh yang mudah diatur dan kompatibel dengan semua router.",
    "image": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "networking"
  },
  {
    "id": 37,
    "name": "Switch Jaringan 8 Port Gigabit",
    "price": "Rp 350.000",
    "description": "Switch jaringan gigabit dengan 8 port untuk ekspansi jaringan rumah atau kantor kecil.",
    "image": "https://images.unsplash.com/photo-1601643157091-ce5c0bb8c7b8?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "category": "networking"
  }
]
# Daftar order yang telah dibuat
orders = []
order_counter = 1000 # Untuk order ID

# Middleware untuk mengecek status login dan menambahkan user ke g
@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = users.get(user_id)
        g.user_id = user_id

# Decorator untuk halaman yang membutuhkan login API
def api_login_required(f):
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return jsonify({"status": "error", "message": "Unauthorized. Please log in."}), 401
        return f(*args, **kwargs)
    wrapped_view.__name__ = f.__name__ # Preserve original name for Flask routing
    return wrapped_view

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user_found_id = None
    for user_id, user_data in users.items():
        if user_data['username'] == username and user_data['password'] == password:
            user_found_id = user_id
            break
    
    if user_found_id:
        # Restriction for CTF player: Only Haykal (ID 6) can log in
        if user_found_id != 6:
            return jsonify({"status": "error", "message": "Only Haykal is allowed to log in for this CTF challenge."}), 403 # Forbidden
        
        session['user_id'] = user_found_id
        session['username'] = username
        return jsonify({"status": "success", "message": "Login successful!", "user": {"id": user_found_id, "username": username}})
    
    return jsonify({"status": "error", "message": "Invalid username or password."}), 401
    
@app.route('/logout', methods=['POST'])
@api_login_required
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return jsonify({"status": "success", "message": "Logged out successfully."})

@app.route('/api/user_info', methods=['GET'])
@api_login_required
def user_info():
    return jsonify({
        "status": "success",
        "user": {
            "id": g.user_id,
            "username": g.user['username'],
            # Phone number is no longer directly from addresses[g.user_id] because address management is removed
            "phone": addresses.get(g.user_id, {}).get("phone", "") 
        }
    })

@app.route('/api/products', methods=['GET'])
@api_login_required
def get_products():
    # No longer checking for user_has_address here, as it's not a prerequisite for browsing
    return jsonify({"status": "success", "products": products})

# The /api/manage_address route is kept for backend IDOR retrieval, but not exposed via frontend UI
@app.route('/api/manage_address', methods=['GET', 'POST'])
@api_login_required
def api_manage_address():
    # Only allow GET for existing dummy addresses or Haykal's if he added one
    # POST is still needed to allow Haykal to add his address
    if request.method == 'GET':
        current_address = addresses.get(g.user_id)
        if current_address:
            return jsonify({"status": "success", "address": current_address})
        else:
            # Return a specific error code for frontend to know it's missing, not a general error
            return jsonify({"status": "error", "message": "Address not found for this user.", "code": "NO_ADDRESS"}), 404
    elif request.method == 'POST':
        data = request.json
        full_name = data.get('full_name')
        street = data.get('street')
        city = data.get('city')
        postal_code = data.get('postal_code')
        phone = data.get('phone') # Added phone number field

        if not all([full_name, street, city, postal_code, phone]):
            return jsonify({"status": "error", "message": "All address fields including phone must be filled."}), 400
        else:
            addresses[g.user_id] = {
                "full_name": full_name,
                "street": street,
                "city": city,
                "postal_code": postal_code,
                "phone": phone
            }
            return jsonify({"status": "success", "message": "Address updated successfully!", "address": addresses[g.user_id]})

@app.route('/api/order', methods=['POST'])
@api_login_required
def api_order():
    data = request.json
    product_id = data.get('product_id')
    selected_product = next((p for p in products if p['id'] == product_id), None)

    if not selected_product:
        return jsonify({"status": "error", "message": "Product not found."}), 404
    
    # *** VULNERABILITY HERE (IDOR) ***
    # Backend mengambil user_id dari request JSON, BUKAN dari session user yang login.
    # Tidak ada pengecekan apakah user_id ini sesuai dengan user_id di session.
    target_user_id_from_form = data.get('user_id') 
    if target_user_id_from_form is None:
        return jsonify({"status": "error", "message": "user_id is required."}), 400

    try:
        target_user_id_from_form = int(target_user_id_from_form)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid user_id format."}), 400
    # *********************************

    flag_message = None
    # 10. FLAG LOGIC
    # Jika user login adalah haykal (id 6) DAN user_id di request BUKAN 6, tampilkan flag.
    if g.user_id == 6 and target_user_id_from_form != 6:
        flag_message = "ITCLUB{1D0R_P4D4_0RD3R_4DDR3S5}"
        # Jika flag terpicu, kita akan langsung mengembalikan respons sukses dengan flag
        # Ini agar flag selalu muncul tanpa terhalang oleh pengecekan alamat
        return jsonify({
            "status": "success",
            "product": selected_product, # selected_product sudah terdefinisi di sini
            "shipping_address": addresses.get(target_user_id_from_form), # Tetap coba ambil alamat jika ada
            "target_user_id": target_user_id_from_form,
            "flag": flag_message
        })
    
    # Ambil alamat menggunakan user_id yang didapat dari form (VULNERABLE)
    shipping_address = addresses.get(target_user_id_from_form)

    if not shipping_address:
        # Changed error message and code to reflect that address is missing for a target user
        return jsonify({
            "status": "error", 
            "message": f"User ID {target_user_id_from_form} does not have a registered address.",
            "code": "TARGET_USER_NO_ADDRESS" 
        }), 400

    return jsonify({
        "status": "success",
        "product": selected_product,
        "shipping_address": shipping_address,
        "target_user_id": target_user_id_from_form,
        "flag": flag_message
    })

@app.route('/api/confirm_order', methods=['POST'])
@api_login_required
def api_confirm_order():
    global order_counter
    data = request.json
    product_id = data.get('product_id')
    target_user_id_for_shipping = data.get('target_user_id')
    address_details_str = data.get('address_details') # Stringified address from frontend for record
    phone_number = data.get('phone_number') # Phone number from frontend for record

    selected_product = next((p for p in products if p['id'] == product_id), None)
    
    if not selected_product or not address_details_str or not phone_number:
        return jsonify({"status": "error", "message": "Invalid order data."}), 400

    order_counter += 1
    order_id = f"ORD-{order_counter}"
    
    orders.append({
        "id": order_id,
        "date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
        "product": selected_product['name'],
        "price": selected_product['price'],
        "buyer_user_id": g.user_id, # User yang benar-benar login
        "shipping_to_user_id": target_user_id_for_shipping, # User yang alamatnya dipakai (VULNERABLE)
        "shipping_address": address_details_str, # Store as string
        "phone_number": phone_number,
        "status": "pending"
    })
    
    return jsonify({"status": "success", "message": "Order placed successfully!", "order_id": order_id})

@app.route('/api/order_history', methods=['GET'])
@api_login_required
def api_order_history():
    user_orders = [order for order in orders if order['buyer_user_id'] == g.user_id]
    
    # Enrich orders with username of the actual recipient for display
    enriched_orders = []
    for order in user_orders:
        recipient_username = users.get(order['shipping_to_user_id'], {}).get('username', 'Unknown User')
        enriched_order = order.copy()
        enriched_order['recipient_username'] = recipient_username
        enriched_orders.append(enriched_order)

    return jsonify({"status": "success", "orders": enriched_orders})

if __name__ == '__main__':
    app.run(debug=True)
