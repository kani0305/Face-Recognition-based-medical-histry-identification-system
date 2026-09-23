import sqlite3
import os

DB_FILE = "data/patients.db"


def init_db():
    """Initialize the database and create the table if not exists"""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            doctor TEXT,
            bp TEXT,
            history TEXT,
            face_path TEXT
        )
    """)
    conn.commit()
    conn.close()


def insert_patient(name, age, gender, doctor, bp, history, face_path):
    """Insert new patient record"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO patients (name, age, gender, doctor, bp, history, face_path)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, age, gender, doctor, bp, history, face_path))
    conn.commit()
    conn.close()


def get_patient_by_name(name):
    """Fetch patient by name or file path (case-insensitive)"""
    name = os.path.splitext(os.path.basename(name.strip().lower()))[0]
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE LOWER(TRIM(name)) = ?", (name,))
    patient = cursor.fetchone()
    conn.close()
    return patient
