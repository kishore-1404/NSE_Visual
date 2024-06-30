from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import yfinance as yf
from database import db, StockData, update_stock_data,update_stocks
from stock_list import Nifty50
from routes_app import routes_app
import threading 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stock_data.db'  # SQLite database file
db.init_app(app)

with app.app_context():
    db.create_all()
    # update_stocks(Nifty50)

# Register the routes defined in routes_app.py
app.register_blueprint(routes_app)

# @app.route('/api/stock_data', methods=['GET'])
# def get_stock_data():
#     stock_data = StockData.query.all()

#     # Convert the list of StockData objects to a list of dictionaries
#     stock_data_list = []
#     for data in stock_data:
#         stock_data_list.append({
#             'id': data.id,
#             'symbol': data.symbol,
#             'longName': data.longName,
#             'open': data.open,
#             'previousClose': data.previousClose,
#             'currentPrice': data.currentPrice,
#             'dayHigh':data.dayHigh,
#             # Add other fields as needed
#         })

#     # Return the JSONified data
#     return jsonify(stock_data_list)

# # Route to render the index.html template
# @app.route('/')
# def index():
#     return render_template('home.html')

# @app.route('/update_stock_data/<symbol>')
# def update_stock_route(symbol):
#     # Call the function to update stock data
#     update_stock_data(symbol)
#     return "Stock data updated successfully!"

# @app.route('/update_stock_list/<list>')
# def update_stock_list(lit):
#     # Call the function to update stock data
#     update_stocks(lit)
#     return "Stock data updated successfully!"


# @app.route('/stocks/filter', methods=['GET'])
# def filter_stocks_price():
#     try:
#         min_price = float(request.args.get('min_price', float('-inf')))
#         max_price = float(request.args.get('max_price', float('inf')))
#         min_volume = float(request.args.get('min_volume', 0))
#         max_volume = float(request.args.get('max_volume', float('inf')))
#         min_diff_price = float(request.args.get('min_diff_price', float('-inf')))
#     except ValueError:
#         return jsonify(error="Invalid filter values"), 400

#     # Query the database with filters and additional condition
#     filtered_stocks = StockData.query.filter(
#         StockData.currentPrice.between(min_price, max_price),
#         StockData.volume.between(min_volume, max_volume),
#         (StockData.previousClose - StockData.fiftyDayAverage) >= min_diff_price
#     ).all()

#     # Convert filtered_stocks to a list of dictionaries for JSON response
#     filtered_stocks_data = [
#         {key: value for key, value in stock.__dict__.items() if not key.startswith('_')}
#         for stock in filtered_stocks
#     ]

#     return jsonify(filtered_stocks_data)

def update_stock_background():
    with app.app_context():
        update_stocks(Nifty50)
        update_stocks()


if __name__ == '__main__':
    update_thread = threading.Thread(target=update_stock_background)
    update_thread.start()
    
    # Run the Flask app
    app.run(debug=True)
    



