# app.py

import mysql.connector
from flask import Flask, render_template, request

app = Flask(__name__)

# Connect to the database
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="040503",
    database="cars_data"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['GET'])
def results():
    car = request.args.get('car')
    mileage = request.args.get('mileage')

    # Query the database for similar cars
    cursor = db.cursor()
    if mileage:
        query = "SELECT * FROM car_data2 WHERE car = %s AND listing_mileage <= %s"
        params = (car, mileage)
    else:
        query = "SELECT * FROM car_data2 WHERE car = %s"
        params = (car,)
    cursor.execute(query, params)
    listings = cursor.fetchall()

    # Calculate the average market value
    total_price = 0
    for listing in listings:
        price = listing[2]
        try:
            total_price += int(price)
        except ValueError:
            continue

    avg_price = total_price / len(listings) if listings else 0

    return render_template('results.html', market_price=round(avg_price, 2), listings=listings)

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
