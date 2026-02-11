# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash

# --- KONFIGURASI APLIKASI ---
app = Flask(__name__)
# Kunci rahasia untuk session, penting untuk keamanan sesi
app.secret_key = os.urandom(24)

# --- KONFIGURASI CHALLENGE ---
FLAG = "ITCLUB{P4S5W0RD_NY4S4R_S4L4H_0R4NG}"

# --- DATABASE PENGGUNA (Sederhana dalam bentuk list of dictionary) ---
# Struktur: {'user_id': int, 'username': str, 'password': str}
USERS_DATA = [
    {"user_id": 0, "username": "admin", "password": "admin"},
    {"user_id": 1, "username": "abiyan", "password": "abiyan123"},
    {"user_id": 2, "username": "joshua", "password": "joshua123"},
    {"user_id": 3, "username": "phasa", "password": "phasa123"},
    {"user_id": 4, "username": "abu bakar", "password": "abu123"},
    {"user_id": 5, "username": "tiara", "password": "tiara123"},
    {"user_id": 6, "username": "kila", "password": "kila123"},
    {"user_id": 7, "username": "iben", "password": "iben123"},
    {"user_id": 8, "username": "haykal", "password": "haykal123"},
    {"user_id": 9, "username": "alfi", "password": "alfi123"},
    {"user_id": 10, "username": "alfin", "password": "alfin123"},
    {"user_id": 11, "username": "denatalle", "password": "denatalle123"},
    {"user_id": 12, "username": "samuel", "password": "samuel123"},
    {"user_id": 13, "username": "ilham", "password": "ilham123"},
    {"user_id": 14, "username": "dimas", "password": "dimas123"},
    {"user_id": 15, "username": "darwin", "password": "darwin123"},
    {"user_id": 16, "username": "syahrul", "password": "syahrul123"},
    {"user_id": 17, "username": "kenken", "password": "kenken123"},
    {"user_id": 18, "username": "azril", "password": "azril123"},
    {"user_id": 19, "username": "nazril", "password": "nazril123"},
    {"user_id": 20, "username": "fahri", "password": "fahri123"},
    {"user_id": 21, "username": "aril", "password": "aril123"},
    {"user_id": 22, "username": "farhan", "password": "farhan123"},
]

# --- HELPER FUNCTIONS untuk mempermudah pencarian user ---
def find_user_by_username(username):
    """Mencari user berdasarkan username."""
    for user in USERS_DATA:
        if user['username'] == username:
            return user
    return None

def find_user_by_id(user_id):
    """Mencari user berdasarkan user_id."""
    try:
        user_id = int(user_id)
        for user in USERS_DATA:
            if user['user_id'] == user_id:
                return user
    except (ValueError, TypeError):
        pass
    return None

# --- ROUTE APLIKASI ---

@app.route('/')
def index():
    """Halaman utama, langsung arahkan ke login jika belum ada sesi."""
    if 'user_id' in session:
        return redirect(url_for('profile'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Halaman login."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = find_user_by_username(username)

        if user and user['password'] == password:
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            flash('Login berhasil!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Username atau password salah.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/profile')
def profile():
    """Halaman profil pengguna. Memerlukan login."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = find_user_by_id(session['user_id'])
    if not user:
        # Jika user di sesi tidak valid, hapus sesi
        session.clear()
        return redirect(url_for('login'))

    # KONDISI FLAG: Tampilkan flag jika user yang login BUKAN 'admin'
    show_flag = user['username'] != 'admin'

    return render_template('profile.html', user=user, show_flag=show_flag, flag=FLAG)

@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    """Halaman untuk mengubah password. Di sinilah letak kerentanannya."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # --- !!! VULNERABILITY: INSECURE DIRECT OBJECT REFERENCE (IDOR) !!! ---
        # Backend mengambil 'user_id' dari form yang dikirim oleh client,
        # bukan dari session yang terverifikasi.
        # Ini memungkinkan penyerang mengubah parameter 'user_id' untuk
        # menargetkan akun lain.
        target_user_id = request.form.get('user_id')
        new_password = request.form.get('new_password')

        # Tidak ada validasi untuk memeriksa apakah target_user_id sama dengan
        # user_id yang ada di session.
        
        target_user = find_user_by_id(target_user_id)

        if target_user and new_password:
            # Langsung ubah password berdasarkan user_id dari input
            target_user['password'] = new_password
            flash(f"Password untuk user {target_user['username']} berhasil diubah.", 'success')
        else:
            flash('User tidak ditemukan atau password baru kosong.', 'danger')
        
        return redirect(url_for('profile'))

    # Untuk method GET, tampilkan form
    current_user_id = session.get('user_id')
    return render_template('change_password.html', user_id=current_user_id)

@app.route('/logout')
def logout():
    """Menghapus sesi dan keluar."""
    session.clear()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('login'))

# --- MAIN EXECUTION ---
if __name__ == '__main__':
    # Menjalankan aplikasi di 127.0.0.1 (localhost) pada port 5000
    # debug=True agar perubahan kode langsung aktif dan menampilkan error
    app.run(host='127.0.0.1', port=5000, debug=True)
