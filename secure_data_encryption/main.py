import streamlit as st # type: ignore
import sqlite3
import hashlib
import os
from cryptography.fernet import Fernet # type: ignore
import time

# Constants
KEY_FILE = "simple_secret_key"
DB_NAME = "simple_data.db"
MAX_ATTEMPTS = 3
LOCKOUT_TIME = 10  # 5 minutes in seconds

# Initialize session state for authentication and attempts
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'lockout_until' not in st.session_state:
    st.session_state.lockout_until = 0

def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE,"wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE,"rb") as f:
            key = f.read()
    return key

cipher = Fernet(load_key())

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Create vault table
    c.execute("""
            CREATE TABLE IF NOT EXISTS vault (
            label TEXT PRIMARY KEY,
            encrypted_text TEXT,
            passkey TEXT)""")
    
    # Create users table
    c.execute("""
            CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT)""")
    
    # Add default admin user if not exists
    admin_hash = hashlib.sha256("admin123".encode()).hexdigest()
    try:
        c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                 ("admin", admin_hash))
    except sqlite3.IntegrityError:
        pass  # Admin user already exists
    
    conn.commit()
    conn.close()

init_db()

def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

def encrypt(text):
    return cipher.encrypt(text.encode()).decode()

def decrypt(encrypted_text):
    return cipher.decrypt(encrypted_text.encode()).decode()

def login_page():
    st.title("Login")
    
    # Check if user is locked out
    if st.session_state.lockout_until > time.time():
        remaining_time = int(st.session_state.lockout_until - time.time())
        st.error(f"Account is locked. Please try again in {remaining_time} seconds.")
        return False
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        result = c.fetchone()
        conn.close()
        
        if result and result[0] == hashlib.sha256(password.encode()).hexdigest():
            st.session_state.authenticated = True
            st.session_state.attempts = 0
            st.success("Login successful!")
            st.rerun()
        else:
            st.session_state.attempts += 1
            if st.session_state.attempts >= MAX_ATTEMPTS:
                st.session_state.lockout_until = time.time() + LOCKOUT_TIME
                st.error(f"Too many failed attempts. Account locked for {LOCKOUT_TIME//60} minutes.")
            else:
                st.error(f"Invalid credentials. {MAX_ATTEMPTS - st.session_state.attempts} attempts remaining.")
    
    return False

def main_app():
    st.title("Secure Data Encryption WebApp")
    
    # Sidebar for navigation
    menu = ["Home", "Store Secret", "Retrieve Secret"]
    choice = st.sidebar.selectbox("Choose Option", menu)
    
    if choice == "Home":
        st.header("Welcome to Secure Data Encryption System")
        st.write("""
        This application allows you to:
        - Store sensitive data securely
        - Retrieve your data using a passkey
        - All data is encrypted using Fernet encryption
        """)
        
    elif choice == "Store Secret":
        st.header("Store a new secret")
        
        label = st.text_input("Label(Unique ID): ")
        secret = st.text_area("Your Secret")
        passkey = st.text_input("passkey (to protect it): ", type="password")
        
        if st.button("Encrypt and Save"):
            if label and secret and passkey:
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                encrypted = encrypt(secret)
                hashed_key = hash_passkey(passkey)
                
                try:
                    c.execute("INSERT INTO vault (label, encrypted_text, passkey) VALUES (?, ?, ?)", 
                             (label, encrypted, hashed_key))
                    conn.commit()
                    st.success("Secret saved Successfully")
                except sqlite3.IntegrityError:
                    st.error("Label already exists!")
                finally:
                    conn.close()
            else:
                st.warning("Please fill all fields")
    
    elif choice == "Retrieve Secret":
        st.header("Retrieve Your Secret")
        label = st.text_input("Enter Label: ")
        passkey = st.text_input("Enter passkey: ", type="password")
        
        if st.button("Decrypt"):
            if not label or not passkey:
                st.warning("Please fill all fields")
                return
                
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT encrypted_text, passkey FROM vault WHERE label = ?", (label,))
            result = c.fetchone()
            conn.close()
            
            if result:
                encrypted_text, stored_hash = result
                if hash_passkey(passkey) == stored_hash:
                    decrypted = decrypt(encrypted_text)
                    st.success("Here is your secret..")
                    st.code(decrypted)
                else:
                    st.error("Incorrect Passkey")
            else:
                st.warning("No such label found")

# Main app flow
if not st.session_state.authenticated:
    login_page()
else:
    # Add logout button in sidebar
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.attempts = 0
        st.rerun()
    
    main_app() 



