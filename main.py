from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import base64
from datetime import datetime, timedelta
import time

app = Flask(__name__)

def remove_expired_items():
    """Remove items that have expired based on their TTL"""
    current_time = int(time.time())
    con = sqlite3.connect('auct_datas_2.db')
    cur = con.cursor()
    cur.execute("DELETE FROM auctionItems WHERE end_time < ?", (current_time,))
    con.commit()
    con.close()

def format_time_remaining(end_time):
    """Format the remaining time in a human-readable format"""
    now = datetime.now()
    end_datetime = datetime.fromtimestamp(end_time)
    
    if end_datetime < now:
        return "Expired"
    
    time_remaining = end_datetime - now
    days = time_remaining.days
    hours = time_remaining.seconds // 3600
    minutes = (time_remaining.seconds % 3600) // 60
    
    if days > 0:
        return f"{days}d {hours}h remaining"
    elif hours > 0:
        return f"{hours}h {minutes}m remaining"
    else:
        return f"{minutes}m remaining"

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/homepage")
def homepage():
    remove_expired_items()  # Clean up expired items
    
    con = sqlite3.connect('auct_datas_2.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM auctionItems")
    auctions = []
    for row in cur.fetchall():
        auction = {
            'id': row[0],
            'item': row[1],
            'starting_price': row[2],
            'current_bid': row[3],
            'image': base64.b64encode(row[4]).decode('utf-8') if row[4] else None,
            'description': row[5],
            'end_time': row[6],
            'time_remaining': format_time_remaining(row[6]),
            'end_datetime': datetime.fromtimestamp(row[6]).strftime('%Y-%m-%d %H:%M:%S')
        }
        auctions.append(auction)
    con.close()
    return render_template("homepage.html", auctions=auctions)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        item = request.form['item']
        starting_price = float(request.form['starting_price'])
        description = request.form['description']
        image = request.files['image'].read() if 'image' in request.files else None
        
        # Calculate end time based on duration
        duration_hours = int(request.form['duration'])
        end_time = int(time.time() + (duration_hours * 3600))

        con = sqlite3.connect('auct_datas_2.db')
        cur = con.cursor()
        cur.execute("""
            INSERT INTO auctionItems 
            (item, starting_price, current_bid, image, description, end_time) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            (item, starting_price, starting_price, image, description, end_time))
        con.commit()
        con.close()

        return redirect(url_for('homepage'))

    return render_template('add_item.html')

@app.route('/place_bid', methods=['POST'])
def place_bid():
    remove_expired_items()  # Clean up expired items
    
    item_id = int(request.form['item_id'])
    bid_amount = float(request.form['bid_amount'])

    con = sqlite3.connect('auct_datas_2.db')
    cur = con.cursor()
    
    # Check if item hasn't expired
    cur.execute("SELECT end_time FROM auctionItems WHERE id = ?", (item_id,))
    result = cur.execute("SELECT end_time FROM auctionItems WHERE id = ?", (item_id,)).fetchone()
    
    if not result or result[0] < int(time.time()):
        con.close()
        return render_template('homepage.html', message="This auction has expired!")

    cur.execute("UPDATE auctionItems SET current_bid = ? WHERE id = ?", (bid_amount, item_id))
    con.commit()
    
    # Fetch updated auctions
    cur.execute("SELECT * FROM auctionItems")
    auctions = []
    for row in cur.fetchall():
        auction = {
            'id': row[0],
            'item': row[1],
            'starting_price': row[2],
            'current_bid': row[3],
            'image': base64.b64encode(row[4]).decode('utf-8') if row[4] else None,
            'description': row[5],
            'end_time': row[6],
            'time_remaining': format_time_remaining(row[6]),
            'end_datetime': datetime.fromtimestamp(row[6]).strftime('%Y-%m-%d %H:%M:%S')
        }
        auctions.append(auction)
    con.close()

    return render_template('homepage.html', auctions=auctions, message="Bid placed successfully!")

if __name__ == "__main__":
    remove_expired_items()  # Clean up any expired items on startup
    app.run(debug=True)