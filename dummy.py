import sqlite3

def init_db():
    # Connect to SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect('auct_datas_2.db')
    c = conn.cursor()
    
    # Create the auctionItems table
    c.execute('''CREATE TABLE IF NOT EXISTS auctionItems
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  item TEXT NOT NULL,
                  starting_price REAL NOT NULL,
                  current_bid REAL,
                  image BLOB,
                  description TEXT)''')
    
    print("Database initialized successfully!")
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()