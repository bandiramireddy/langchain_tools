#create sqlite db in the db folder with the name helpdesk.db , and create one tickets
#table with columns id (integer primary key), title (text), description (text), status (text), created_at (timestamp)

# insert 2 Error tickets in the tickets table with title "Cannot connect to VPN" and "Email not syncing", description "User cannot connect to the company VPN from home." and "User's email is not syncing on mobile device.", status "open", created_at as current timestamp
# insert 2 error tickes with created_dt as 2025-01-10 
# insert 2 info tickets in the tickets table with title "Request for new laptop" and "Password reset", description "User requests a new laptop for work." and "User needs to reset their password.", status "closed", created_at as current timestamp
# insert 2 info tickets with created_dt as 2025-01-09
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
DB_PATH = 'db/helpdesk.db'
def create_db_and_table():
    """Create the SQLite database and tickets table if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_sample_tickets():
    """Insert sample tickets into the tickets table."""
    sample_tickets = [
        ("Cannot connect to VPN", "User cannot connect to the company VPN from home.", "open", "2025-01-10 10:00:00"),
        ("Email not syncing", "User's email is not syncing on mobile device.", "open", "2025-01-10 11:00:00"),
        ("Request for new laptop", "User requests a new laptop for work.", "closed", "2025-01-09 09:30:00"),
        ("Password reset", "User needs to reset their password.", "closed", "2025-01-09 10:15:00")
    ]
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO tickets (title, description, status, created_at)
        VALUES (?, ?, ?, ?)
    ''', sample_tickets)
    conn.commit()
    conn.close()
#display all tickets
def display_all_tickets():
    """Display all tickets in the tickets table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tickets')
    tickets = cursor.fetchall()
    for ticket in tickets:
        print(ticket)
    conn.close()
if __name__ == "__main__":
    # create_db_and_table()
    # insert_sample_tickets()
    # print("Database and sample tickets created successfully.")
    display_all_tickets()
