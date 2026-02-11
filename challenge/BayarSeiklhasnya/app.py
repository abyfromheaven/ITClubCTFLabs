import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) # Used for session management

# Database configuration
DATABASE = 'database.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                balance INTEGER NOT NULL
            )
        ''')
        
        # Create events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price INTEGER NOT NULL,
                description TEXT
            )
        ''')
        
        # Create transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                event_id INTEGER NOT NULL,
                paid_amount INTEGER NOT NULL,
                status TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (event_id) REFERENCES events(id)
            )
        ''')

        # Insert dummy user if not exists
        cursor.execute("SELECT * FROM users WHERE username = 'user'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO users (username, password, balance) VALUES (?, ?, ?)", 
                           ('user', 'user123', 1000))

        # Insert hardcoded events if not exists
        cursor.execute("SELECT * FROM events WHERE name = 'CTF Internal IT Club'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO events (name, price, description) VALUES (?, ?, ?)",
                           ('CTF Internal IT Club', 150, 'lomba hacking legal internal, no drama'))
        
        cursor.execute("SELECT * FROM events WHERE name = 'Workshop Linux Buat Yang Masih Takut Terminal'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO events (name, price, description) VALUES (?, ?, ?)",
                           ('Workshop Linux Buat Yang Masih Takut Terminal', 200, 'dari ls sampe sudo tanpa nangis'))
        
        cursor.execute("SELECT * FROM events WHERE name = 'Web Exploitation 101'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO events (name, price, description) VALUES (?, ?, ?)",
                           ('Web Exploitation 101', 300, 'SQLi, IDOR, dan dosa masa lalu backend'))

        db.commit()
        db.close()

# Initialize the database on startup
if not os.path.exists(DATABASE):
    init_db()

# --- Routes ---

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    user_id = 1 # Hardcode user_id for direct access
    db = get_db()
    
    # Get user balance
    user_data = db.execute("SELECT balance, username FROM users WHERE id = ?", (user_id,)).fetchone()
    balance = user_data['balance'] if user_data else 0
    username = user_data['username'] if user_data else 'Guest'

    # Get all events
    events = db.execute("SELECT * FROM events").fetchall()

    # Get user's transactions
    transactions = db.execute('''
        SELECT t.id, e.name AS event_name, t.paid_amount, t.status, t.timestamp
        FROM transactions t
        JOIN events e ON t.event_id = e.id
        WHERE t.user_id = ?
        ORDER BY t.timestamp DESC
    ''', (user_id,)).fetchall()
    
    db.close()
    return render_template('dashboard.html', balance=balance, events=events, transactions=transactions, username=username)

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    user_id = 1 # Hardcode user_id for direct access
    db = get_db()
    event = db.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
    db.close()
    
    if event:
        return render_template('event_detail.html', event=event)
    else:
        flash('Event not found.', 'danger')
        return redirect(url_for('dashboard'))

@app.route('/pay', methods=['POST'])
def pay():
    user_id = 1 # Hardcode user_id for direct access
    event_id = request.form.get('event_id', type=int)
    
    # --- VULNERABLE LOGIC START ---
    # The 'amount' is taken directly from the client request without validation.
    paid_amount = request.form.get('amount', type=int)
    # --- VULNERABLE LOGIC END ---

    if not event_id or paid_amount is None:
        flash('Invalid payment request.', 'danger')
        return redirect(url_for('dashboard'))

    db = get_db()
    cursor = db.cursor()

    try:
        # Get event actual price for flag logic
        event_data = cursor.execute("SELECT price, name FROM events WHERE id = ?", (event_id,)).fetchone()
        if not event_data:
            flash('Event not found.', 'danger')
            return redirect(url_for('dashboard'))
        
        actual_event_price = event_data['price']
        event_name = event_data['name']

        # Get user balance
        user_data = cursor.execute("SELECT balance FROM users WHERE id = ?", (user_id,)).fetchone()
        current_balance = user_data['balance']

        # Check if user has enough balance (based on the *paid_amount* from client)
        if current_balance >= paid_amount:
            # Deduct balance
            new_balance = current_balance - paid_amount
            cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (new_balance, user_id))
            
            # Record transaction
            transaction_status = 'success'
            cursor.execute("INSERT INTO transactions (user_id, event_id, paid_amount, status) VALUES (?, ?, ?, ?)",
                           (user_id, event_id, paid_amount, transaction_status))
            
            db.commit()

            # Flag logic: If paid_amount is less than actual price, display flag
            flag = None
            if paid_amount < actual_event_price:
                flag = "ITCLUB{fr0nt3nd_s0k_g4g4h_b4ck3nd_t3t3p_b3g0}"
            
            return render_template('payment_status.html', 
                                   status='success', 
                                   event_name=event_name,
                                   paid_amount=paid_amount,
                                   actual_price=actual_event_price,
                                   new_balance=new_balance,
                                   flag=flag)
        else:
            # Insufficient balance
            transaction_status = 'failed'
            cursor.execute("INSERT INTO transactions (user_id, event_id, paid_amount, status) VALUES (?, ?, ?, ?)",
                           (user_id, event_id, paid_amount, transaction_status))
            db.commit()
            flash('Insufficient balance.', 'danger')
            return render_template('payment_status.html', status='failed', message='Insufficient balance.')
            
    except Exception as e:
        db.rollback()
        flash(f'An error occurred during payment: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))
    finally:
        db.close()

@app.route('/reset_data')
def reset_data():
    user_id = 1 # Target dummy user
    default_balance = 1000
    
    db = get_db()
    cursor = db.cursor()
    
    try:
        # Reset user balance
        cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (default_balance, user_id))
        
        # Clear user transactions
        cursor.execute("DELETE FROM transactions WHERE user_id = ?", (user_id,))
        
        db.commit()
        flash('User data (balance and transactions) has been reset!', 'info')
    except Exception as e:
        db.rollback()
        flash(f'An error occurred during data reset: {str(e)}', 'danger')
    finally:
        db.close()
        
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    # Initialize the database on every run if it doesn't exist
    # This ensures that if the database file is deleted, it's recreated.
    # For production, you might want a more robust migration system.
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True)