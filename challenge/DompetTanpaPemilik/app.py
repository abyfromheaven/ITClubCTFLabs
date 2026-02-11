import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import copy

# Inisialisasi Aplikasi Flask
app = Flask(__name__)
app.secret_key = os.urandom(24)

# --- KONFIGURASI LAB & DATABASE SIMULATION ---

# Flag yang akan didapatkan peserta
FLAG = "ITCLUB{S4Ld0_BuK4n_M1L1kMu}"
# Kondisi saldo penyerang untuk memunculkan flag
# Sekarang flag akan muncul jika saldo target (Tiara) = 0

# Data user IT Club
USERS = {
    "1001": {"username": "Abiyan", "password": "Abiyan", "role": "Kembaran Justin Bieber"}, # Abiyan role baru
    "1002": {"username": "Joshua", "password": "Joshua", "role": "member"},
    "1003": {"username": "Denatalle", "password": "Denatalle", "role": "member"},
    "1004": {"username": "Samuel", "password": "Samuel", "role": "member"},
    "1005": {"username": "Ilham", "password": "Ilham", "role": "member"},
    "1006": {"username": "Phasa Turing", "password": "kolot123", "role": "member"}, # Phasa Turing dengan password baru
    "1007": {"username": "Dimas", "password": "Dimas", "role": "member"},
    "1008": {"username": "Darwin", "password": "Darwin", "role": "member"},
    "1009": {"username": "Alfin", "password": "Alfin", "role": "member"},
    "1010": {"username": "Alfi", "password": "Alfi", "role": "member"},
    "1011": {"username": "Abu", "password": "Abu", "role": "member"},
    "1012": {"username": "Aril", "password": "Aril", "role": "member"},
    "1013": {"username": "Syahrul", "password": "Syahrul", "role": "member"},
    "1014": {"username": "Azril", "password": "Azril", "role": "member"},
    "1015": {"username": "Fahri", "password": "Fahri", "role": "member"},
    "1016": {"username": "Farhan", "password": "Farhan", "role": "member"},
    "1017": {"username": "Haikal", "password": "Haikal", "role": "member"},
    "1018": {"username": "Iben", "password": "Iben", "role": "member"},
    "1019": {"username": "Kenken", "password": "Kenken", "role": "member"},
    "1020": {"username": "Kila", "password": "Kila", "role": "member"},
    "1021": {"username": "Nazril", "password": "Nazril", "role": "member"},
    "1022": {"username": "Tiara", "password": "Tiara", "role": "treasurer"}, # Tiara tetap treasurer di backend
}

TARGET_USER_ID = "1022" # User ID Tiara (Bendahara)

# Saldo awal untuk setiap user. Disimpan sebagai template untuk fitur reset.
INITIAL_BALANCES = {
    "1001": 1_500_000,
    "1002": 1_200_000,
    "1003": 850_000,
    "1004": 2_500_000,
    "1005": 500_000,
    "1006": 50_000,  # Saldo Phasa Turing (penyerang) sangat kecil
    "1007": 1_100_000,
    "1008": 3_000_000,
    "1009": 450_000,
    "1010": 900_000,
    "1011": 650_000,
    "1012": 1_800_000,
    "1013": 2_100_000,
    "1014": 400_000,
    "1015": 500_000,
    "1016": 950_000,
    "1017": 2_700_000,
    "1018": 600_000,
    "1019": 1_400_000,
    "1020": 1_600_000,
    "1021": 800_000,
    "1022": 1_500_000, # Saldo Tiara (target) diubah agar tidak terlalu menonjol
}

# Variabel state aplikasi yang akan dimodifikasi
BALANCES = copy.deepcopy(INITIAL_BALANCES)
TRANSACTION_HISTORY = []

# --- DECORATORS & HELPERS ---
def login_required(f):
    """Decorator untuk memastikan user sudah login."""
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Anda harus login untuk mengakses halaman ini.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def get_total_balance():
    """Menghitung total saldo dari semua user."""
    return sum(BALANCES.values())

# --- ROUTES ---

@app.route("/")
@login_required
def index():
    return redirect(url_for('dashboard'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user_id_found = None
        for uid, udata in USERS.items():
            if udata['username'] == username and udata['password'] == password:
                user_id_found = uid
                break
        
        if user_id_found:
            session['user_id'] = user_id_found
            return redirect(url_for('dashboard'))
        else:
            flash("Username atau password salah.", "danger")
            return redirect(url_for('login'))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route("/dashboard")
@login_required
def dashboard():
    user_id = session['user_id']
    user_info = USERS[user_id]
    user_balance = BALANCES.get(user_id, 0)
    target_balance = BALANCES.get(TARGET_USER_ID, 0)

    # KONDISI FLAG BARU: Saldo target (Tiara) harus 0.
    show_flag = (target_balance == 0)

    user_transactions = [t for t in TRANSACTION_HISTORY if t['from_id'] == user_id or t['to_id'] == user_id]
    
    return render_template(
        "dashboard.html", 
        user=user_info, 
        user_id=user_id,
        balance=user_balance, 
        show_flag=show_flag, 
        flag=FLAG,
        transactions=reversed(user_transactions[-5:]),
        target_user_id=TARGET_USER_ID, # TERUSKAN TARGET_USER_ID KE DASHBOARD
        USERS=USERS # Teruskan variabel USERS agar bisa diakses di template untuk nama user
    )

@app.route("/members")
@login_required
def members():
    all_users = []
    for uid, udata in USERS.items():
        user_balance = BALANCES.get(uid, 0) # Get balance for each user
        all_users.append({"user_id": uid, "balance": user_balance, **udata})
    return render_template("members.html", users=all_users, target_user_id=TARGET_USER_ID)

@app.route("/api/balances")
def api_get_balances():
    return jsonify(BALANCES)

@app.route("/transfer", methods=["GET", "POST"])
@login_required
def transfer():
    current_user_id = session['user_id']

    if request.method == "POST":
        from_id = request.form.get("from_user_id") 
        to_id = request.form.get("to_user_id")
        
        try:
            amount = int(request.form.get("amount"))
        except (ValueError, TypeError):
            flash("Jumlah transfer tidak valid.", "danger")
            return redirect(url_for('transfer'))

        if from_id not in USERS or to_id not in USERS:
            flash("User pengirim atau penerima tidak valid.", "danger")
            return redirect(url_for('transfer'))
        if amount <= 0:
            flash("Jumlah transfer harus lebih dari nol.", "danger")
            return redirect(url_for('transfer'))
        if from_id == to_id:
            flash("Anda tidak bisa transfer ke diri sendiri.", "danger")
            return redirect(url_for('transfer'))
        
        sender_balance = BALANCES.get(from_id, 0)

        if sender_balance >= amount:
            BALANCES[from_id] -= amount
            BALANCES[to_id] += amount
            TRANSACTION_HISTORY.append({
                "from_id": from_id, "from_name": USERS[from_id]['username'],
                "to_id": to_id, "to_name": USERS[to_id]['username'],
                "amount": amount,
            })
            flash(f"Transfer sebesar {amount:,} ke {USERS[to_id]['username']} berhasil diproses.", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Saldo pengirim tidak mencukupi.", "danger")
            return redirect(url_for('transfer'))

    current_user_info = USERS[current_user_id]
    other_users = [{"user_id": uid, **udata} for uid, udata in USERS.items() if uid != current_user_id]
    return render_template("transfer.html", current_user=current_user_info, current_user_id=current_user_id, users=other_users)

@app.route("/reset", methods=["POST"]) # Diubah menjadi hanya menerima POST
def reset_lab():
    """Endpoint untuk mereset seluruh state lab ke kondisi awal."""
    global BALANCES, TRANSACTION_HISTORY
    BALANCES = copy.deepcopy(INITIAL_BALANCES)
    TRANSACTION_HISTORY = []
    
    # Logout user yang mungkin sedang login agar kembali ke halaman login
    session.pop('user_id', None)
    
    flash("Lingkungan lab telah direset ke kondisi awal.", "info")
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True, port=5001)