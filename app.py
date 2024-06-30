from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, StockData, update_stock_data, update_stocks, User,WatchList
from stock_list import Nifty50
import threading
from yahoo_plot import plot_interactive_line_chart
import yfinance as yf

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stock_data.db'
db.init_app(app)

# app.config['SQLALCHEMY_DATABASE_URI_USERS'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS_USERS'] = False
# db_user.init_app(app)

with app.app_context():
    db.create_all()
    # update_stocks(Nifty50)  
    db.session.commit()
    WatchList.query.delete()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is None:
            new_user = User(username=username, password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! Please login.')
            return redirect(url_for('index'))
        else:
            flash('Username exists')
            return redirect(url_for('register'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('stocks'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('index'))
    return render_template('login.html')


# @app.route('/dashboard')
# def dashboard():
#     if 'user_id' in session:
#         return render_template('welcome.html', username=session['username'])
#     else:
#         return redirect(url_for('dashboard'))
        
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/charts',methods=['GET'])
def charts():
    if 'user_id' not in session:
        return render_template('login.html')

    return render_template('charts.html')

@app.route('/stocks')
def stocks():
    return render_template('stocks.html')




#Backend Process

@app.route('/graph')
def graph():
    watchlist_symbols = WatchList.query.with_entities(WatchList.symbol).all()
    watchlist_symbols = [symbol[0] for symbol in watchlist_symbols]
    watchlist_symbols = [stock.replace('.NS', '') for stock in watchlist_symbols]
    graph_html_content=plot_interactive_line_chart(watchlist_symbols)
    return render_template('charts.html', graph_html_content=graph_html_content)

@app.route('/WatchList_db/<symbol>')
def add_to_watchlist(symbol):
    existing_item = WatchList.query.filter_by(symbol=symbol).first()
    new_watchlist={'symbol':symbol} 
    if existing_item:
        return "Exist Already" 
    else:
        new_watchlist_item = WatchList(**new_watchlist)
        db.session.add(new_watchlist_item)
        db.session.commit()
        return "Added to Watchlist"
@app.route('/reset/watch_list')
def reset_watch_list():
    WatchList.query.delete()
    db.session.commit()
    return "Watch list resetted"

#To populate table
@app.route('/api/stock_data', methods=['GET'])
def get_stock_data():
    stock_data = StockData.query.all()

    # Convert the list of StockData objects to a list of dictionaries
    stock_data_list = []
    for data in stock_data:
        stock_data_list.append({
            'id': data.id,
            'symbol': data.symbol,
            'longName': data.longName,
            'open': data.open,
            'previousClose': data.previousClose,
            'currentPrice': data.currentPrice,
            'dayHigh':data.dayHigh,
            # Add other fields as needed
        })

    # Return the JSONified data
    return jsonify(stock_data_list)


# Add this route at the end of your existing routes in app.py
@app.route('/api/watchlist_symbols', methods=['GET'])
def get_watchlist_symbols():
    watchlist_symbols = WatchList.query.with_entities(WatchList.symbol).all()
    watchlist_symbols = [symbol[0] for symbol in watchlist_symbols]
    return jsonify(watchlist_symbols)

#To get filtered stocks
@app.route('/stocks/filter', methods=['GET'])
def filter_stocks_price():
    try:
        min_price = float(request.args.get('min_price', float('-inf')))
        max_price = float(request.args.get('max_price', float('inf')))
        min_volume = float(request.args.get('min_volume', 0))
        max_volume = float(request.args.get('max_volume', float('inf')))
        min_diff_price = float(request.args.get('min_diff_price', float('-inf')))
    except ValueError:
        return jsonify(error="Invalid filter values"), 400

    # Query the database with filters and additional condition
    filtered_stocks = StockData.query.filter(
        StockData.currentPrice.between(min_price, max_price),
        StockData.volume.between(min_volume, max_volume),
        (StockData.previousClose - StockData.fiftyDayAverage) >= min_diff_price
    ).all()

    # Convert filtered_stocks to a list of dictionaries for JSON response
    filtered_stocks_data = [
        {key: value for key, value in stock.__dict__.items() if not key.startswith('_')}
        for stock in filtered_stocks
    ]

    return jsonify(filtered_stocks_data)

# Avg price & current price filter
@app.route('/stocks/avgP_filter',methods=['GET'])
def get_filter_avgList():
    filtered_stocks = StockData.query.filter(StockData.fiftyDayAverage > StockData.currentPrice).all()
    result = [{'symbol': stock.symbol, 'open': stock.open, 'previousClose': stock.previousClose,
               'currentPrice': stock.currentPrice, 'dayHigh': stock.dayHigh} for stock in filtered_stocks]
    return jsonify(result)

#Low to high filter
@app.route('/stocks/filt_lowtohigh',methods=['GET'])
def get_filter_ascend():
    # Retrieve items in ascending order based on current price
    filtered_stocks = StockData.query.order_by(StockData.currentPrice.asc()).all()
    result = [{'symbol': stock.symbol, 'open': stock.open, 'previousClose': stock.previousClose,
               'currentPrice': stock.currentPrice, 'dayHigh': stock.dayHigh} for stock in filtered_stocks]
    return jsonify(result)


#High to low filter
@app.route('/stocks/filt_hightolow',methods=['GET'])
def get_filter_decend():
    # Retrieve items in ascending order based on current price
    filtered_stocks = StockData.query.order_by(StockData.currentPrice.desc()).all()
    result = [{'symbol': stock.symbol, 'open': stock.open, 'previousClose': stock.previousClose,
               'currentPrice': stock.currentPrice, 'dayHigh': stock.dayHigh} for stock in filtered_stocks]
    return jsonify(result)


#To update database
@app.route('/update_stock_data/<symbol>')
def update_stock_route(symbol):
    # Call the function to update stock data
    update_stock_data(symbol)
    return "Stock data updated successfully!"

@app.route('/update_stock_list/<list>')
def update_stock_list(lit=Nifty50):
    # Call the function to update stock data
    update_stocks(lit)
    return "Stock data updated successfully!"

def update_stock_background():
    with app.app_context():
        update_stocks(Nifty50)
        update_stocks()

if __name__ == '__main__':
    update_thread = threading.Thread(target=update_stock_background)
    update_thread.start()
    
    # Run the Flask app
    app.run(debug=True)
    

