from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/homepage")
def homepage():
    con = sqlite3.connect('auct_datas.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM auctionItems")
    auctions = []
    for row in cur.fetchall():
        auction = {
            'id': row[0],
            'item': row[1],
            'starting_price': row[2],
            'current_bid': row[3],
            'image': row[4],
            'description': row[5]
        }
        auctions.append(auction)
    con.close()
    return render_template("homepage.html", auctions=auctions)

@app.route('/place_bid', methods=['POST'])
def place_bid():
    item_id = int(request.form['item_id'])
    bid_amount = float(request.form['bid_amount'])

    con = sqlite3.connect('auct_datas.db')
    cur = con.cursor()
    cur.execute(f"UPDATE auctionItems SET current_bid = ? WHERE id = ?", (bid_amount, item_id))
    con.commit()
    con.close()

    return render_template('homepage.html', auctions=auctions, message="Bid placed successfully!")

if __name__ == "__main__":
    app.run(debug=True)