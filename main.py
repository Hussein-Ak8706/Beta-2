from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Auction data structure (this can be replaced with a database)
auctions = [
    {"id": 1, "item": "Laptop", "starting_price": 500},
    {"id": 2, "item": "Projector", "starting_price": 200},
]


con = sqlite3.connect('auc_datas.db')
cur = con.cursor()

# Route to display the auction homepage
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/homepage")
def homepage():
    return render_template("homepage.html", auctions=auctions)


# Route to handle bid submissions
@app.route('/place_bid', methods=['POST'])
def place_bid():
    item_id = int(request.form['item_id'])
    bid_amount = float(request.form['bid_amount'])

    # Find the auction by item_id and update the bid (logic can be more complex)
    for auction in auctions:
        if auction['id'] == item_id:
            auction['current_bid'] = bid_amount
            break
    

    return render_template('homepage.html', auctions=auctions, message="Bid placed successfully!")
    

if __name__ == "__main__":
    app.run(debug=True)
