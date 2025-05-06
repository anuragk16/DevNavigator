import mysql.connector
from mysql.connector import Error
from datetime import datetime
import json
# -----------------------------
# Database and Connection Setup
# -----------------------------

def create_database():
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='63789'
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS user_auth_db")
        print("Database 'user_auth_db' created or already exists.")
    except Error as e:
        print("Error:", e)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="63789",
        database="user_auth_db"
    )

# -----------------------------
# Table Creation
# -----------------------------

def create_users_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE,
            email VARCHAR(100) UNIQUE,
            password_hash VARCHAR(255),
            education VARCHAR(100),
            interests TEXT,
            profile_created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def create_user_progress_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_progress (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_email VARCHAR(100),
            roadmap_name VARCHAR(100),
            progress_percent INT DEFAULT 0,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def create_roadmap_progress_table():
    conn = create_connection()
    cursor = conn.cursor()

    # Create the table if not exists (without completed_topics)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS roadmap_progress (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_email VARCHAR(100),
            roadmap_title VARCHAR(255),
            roadmap_path TEXT,
            progress_percent INT DEFAULT 0,
            FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE
        )
    """)

    # Check if 'completed_topics' column already exists
    cursor.execute("SHOW COLUMNS FROM roadmap_progress LIKE 'completed_topics'")
    result = cursor.fetchone()
    
    # If not, add the column
    if not result:
        cursor.execute("ALTER TABLE roadmap_progress ADD COLUMN completed_topics TEXT")
        print("Added 'completed_topics' column to roadmap_progress table.")

    conn.commit()
    cursor.close()
    conn.close()


def initialize_database():
    create_database()
    create_users_table()
    create_user_progress_table()
    create_roadmap_progress_table()
    print("All tables initialized.")

# ----------------------------------
# User Management and Data Insertion
# ----------------------------------

def insert_user(username, email, password_hash, education, interests):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, education, interests)
            VALUES (%s, %s, %s, %s, %s)
        """, (username, email, password_hash, education, interests))
        conn.commit()
        print("User inserted:", username)
    except mysql.connector.Error as e:
        print("Error inserting user:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def fetch_user(email):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

# -------------------------------
# User Progress (Roadmap Level 1)
# -------------------------------


def update_user_progress(user_email, roadmap_name, progress_percent):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM user_progress WHERE user_email = %s AND roadmap_name = %s
    """, (user_email, roadmap_name))
    exists = cursor.fetchone()

    if exists:
        cursor.execute("""
            UPDATE user_progress 
            SET progress_percent = %s, last_updated = NOW()
            WHERE user_email = %s AND roadmap_name = %s
        """, (progress_percent, user_email, roadmap_name))
    else:
        cursor.execute("""
            INSERT INTO user_progress (user_email, roadmap_name, progress_percent)
            VALUES (%s, %s, %s)
        """, (user_email, roadmap_name, progress_percent))

    conn.commit()
    cursor.close()
    conn.close()


def update_roadmap_progress(user_email, roadmap_name, progress_percent, completed_topics=[]):
    conn = create_connection()
    cursor = conn.cursor()
    completed_json = json.dumps(completed_topics)

    cursor.execute("""
        SELECT id FROM roadmap_progress WHERE user_email = %s AND roadmap_title = %s
    """, (user_email, roadmap_name))
    exists = cursor.fetchone()
    
    # Ensure result set is cleared before next query
    while cursor.nextset():
        pass

    if exists:
        cursor.execute("""
            UPDATE roadmap_progress 
            SET progress_percent = %s, completed_topics = %s
            WHERE user_email = %s AND roadmap_title = %s
        """, (progress_percent, completed_json, user_email, roadmap_name))
    else:
        cursor.execute("""
            INSERT INTO roadmap_progress (user_email, roadmap_title, roadmap_path, progress_percent, completed_topics)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_email, roadmap_name, "", progress_percent, completed_json))

    conn.commit()
    cursor.close()
    conn.close()


def get_user_progress(user_email):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT roadmap_name, progress_percent, last_updated
        FROM user_progress
        WHERE user_email = %s
    """, (user_email,))
    progress_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return progress_data

# -----------------------------------
# Roadmap Progress (Path-Specific)
# -----------------------------------

def add_roadmap_to_user(email, title, path):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM roadmap_progress WHERE user_email = %s AND roadmap_path = %s
    """, (email, path))
    exists = cursor.fetchone()

    if not exists:
        cursor.execute("""
            INSERT INTO roadmap_progress (user_email, roadmap_title, roadmap_path, progress_percent)
            VALUES (%s, %s, %s, %s)
        """, (email, title, path, 0))
        conn.commit()

    cursor.close()
    conn.close()

def get_user_roadmaps(email):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT roadmap_title, roadmap_path, progress_percent, completed_topics 
        FROM roadmap_progress 
        WHERE user_email = %s
    """, (email,))
    roadmaps = cursor.fetchall()
    for roadmap in roadmaps:
        if "completed_topics" in roadmap and roadmap["completed_topics"]:
            try:
                roadmap["completed_topics"] = json.loads(roadmap["completed_topics"])
            except:
                roadmap["completed_topics"] = []
        else:
            roadmap["completed_topics"] = []
    cursor.close()
    conn.close()
    return roadmaps


# ------------------------------
# Profile Info Aggregator
# ------------------------------

def get_full_user_profile(email):
    user = fetch_user(email)
    progress = get_user_progress(email)
    return {
        "user_info": user,
        "roadmap_progress": progress
    }

# ------------------------------
# Run Initialization on Import
# ------------------------------

initialize_database()
