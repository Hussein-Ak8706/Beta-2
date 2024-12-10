import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('auct_datas_2.db')
    c = conn.cursor()
    
    # Drop existing table if it exists
    c.execute('DROP TABLE IF EXISTS auctionItems')
    
    # Create the auctionItems table with TTL
    c.execute('''CREATE TABLE IF NOT EXISTS auctionItems
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  item TEXT NOT NULL,
                  starting_price REAL NOT NULL,
                  current_bid REAL,
                  image BLOB,
                  description TEXT,
                  end_time INTEGER NOT NULL)''')
    
    print("Database initialized successfully!")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()