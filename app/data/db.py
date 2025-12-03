"""
Week 8: Database Functions
"""
import sqlite3
from pathlib import Path

DB_PATH = Path("DATA") / "intelligence_platform.db"

def connect_database():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Create all required tables if they don't exist."""
    conn = connect_database()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Cyber incidents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            incident_id INTEGER PRIMARY KEY,
            timestamp TEXT,
            severity TEXT,
            category TEXT,
            status TEXT,
            description TEXT
        )
    """)
    
    # Datasets metadata table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            dataset_id INTEGER PRIMARY KEY,
            name TEXT,
            rows INTEGER,
            columns INTEGER,
            uploaded_by TEXT,
            upload_date TEXT
        )
    """)
    
    # IT tickets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            ticket_id INTEGER PRIMARY KEY,
            priority TEXT,
            description TEXT,
            status TEXT,
            assigned_to TEXT,
            created_at TEXT,
            resolution_time_hours INTEGER
        )
    """)
    
    conn.commit()
    conn.close()

def get_all_users():
    """Get all users from database."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def get_all_incidents():
    """Get all cyber incidents."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cyber_incidents ORDER BY timestamp DESC")
    incidents = cursor.fetchall()
    conn.close()
    return incidents

def get_all_datasets():
    """Get all datasets metadata."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM datasets_metadata ORDER BY dataset_id DESC")
    datasets = cursor.fetchall()
    conn.close()
    return datasets

def get_all_tickets():
    """Get all IT tickets."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM it_tickets ORDER BY ticket_id DESC")
    tickets = cursor.fetchall()
    conn.close()
    return tickets
