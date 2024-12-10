from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/homepage")
def homepage():
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
            'description': row[5]
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

        con = sqlite3.connect('auct_datas_2.db')
        cur = con.cursor()
        cur.execute("INSERT INTO auctionItems (item, starting_price, current_bid, image, description) VALUES (?, ?, ?, ?, ?)",
                    (item, starting_price, starting_price, image, description))
        con.commit()
        con.close()

        return redirect(url_for('homepage'))

    return render_template('add_item.html')

@app.route('/place_bid', methods=['POST'])
def place_bid():
    item_id = int(request.form['item_id'])
    bid_amount = float(request.form['bid_amount'])

    con = sqlite3.connect('auct_datas_2.db')
    cur = con.cursor()
    cur.execute("UPDATE auctionItems SET current_bid = ? WHERE id = ?", (bid_amount, item_id))
    con.commit()
    con.close()

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
            'description': row[5]
        }
        auctions.append(auction)
    con.close()

    return render_template('homepage.html', auctions=auctions, message="Bid placed successfully!")

if __name__ == "__main__":
    app.run(debug=True)