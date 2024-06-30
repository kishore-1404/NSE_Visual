from flask_sqlalchemy import SQLAlchemy
import yfinance as yf
from stock_list import STOCKS
from stock_list import Nifty50

db = SQLAlchemy()

class WatchList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), unique=True, nullable=False)

    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

class StockData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True, nullable=False)
    longName = db.Column(db.String(100), nullable=False)
    open = db.Column(db.Float)
    previousClose = db.Column(db.Float)
    currentPrice = db.Column(db.Float)
    dayHigh = db.Column(db.Float)
    dayLow = db.Column(db.Float)
    fiftyDayAverage = db.Column(db.Float)
    fiftyTwoWeekHigh = db.Column(db.Float)
    fiftyTwoWeekLow = db.Column(db.Float)
    volume = db.Column(db.Integer)
    forwardPE = db.Column(db.Float)
    trailingPE = db.Column(db.Float)
    industry = db.Column(db.String(50))
    payoutRatio = db.Column(db.Float)
    pegRatio = db.Column(db.Float)
    regularMarketVolume = db.Column(db.Integer)
    sector = db.Column(db.String(50))
    twoHundredDayAverage = db.Column(db.Float)

    def to_dict(self):
        return {
            'symbol': self.symbol,
            'longName': self.longName,
            'open': self.open,
            'previousClose': self.previousClose,
            'currentPrice': self.currentPrice,
            'dayHigh': self.dayHigh,
            'dayLow': self.dayLow,
            'fiftyDayAverage': self.fiftyDayAverage,
            'fiftyTwoWeekHigh': self.fiftyTwoWeekHigh,
            'fiftyTwoWeekLow': self.fiftyTwoWeekLow,
            'volume': self.volume,
            'forwardPE': self.forwardPE,
            'trailingPE': self.trailingPE,
            'industry': self.industry,
            'payoutRatio': self.payoutRatio,
            'pegRatio': self.pegRatio,
            'regularMarketVolume': self.regularMarketVolume,
            'sector': self.sector,
            'twoHundredDayAverage': self.twoHundredDayAverage,
        }


relevant_keys = [
    'symbol', 'longName', 'open', 'previousClose', 'currentPrice',
    'dayHigh', 'dayLow', 'fiftyDayAverage', 'fiftyTwoWeekHigh',
    'fiftyTwoWeekLow', 'volume', 'forwardPE', 'trailingPE', 'industry',
    'payoutRatio', 'pegRatio', 'regularMarketVolume', 'sector', 'twoHundredDayAverage'
]
expected_types = {
            'symbol': str,
            'longName': str,
            'open': float,
            'previousClose': float,
            'currentPrice': float,
            'dayHigh': float,
            'dayLow': float,
            'fiftyDayAverage': float,
            'fiftyTwoWeekHigh': float,
            'fiftyTwoWeekLow': float,
            'volume': int,
            'forwardPE': float,
            'trailingPE': float,
            'industry': str,
            'payoutRatio': float,
            'pegRatio': float,
            'regularMarketVolume': int,
            'sector': str,
            'twoHundredDayAverage': float,
            # Add more attributes as needed
        }

def update_stocks(StockList=Nifty50):
    # Fetch data from Yahoo Finance using yfinance
    for symbol in StockList:
        tick = yf.Ticker(symbol)
        data = tick.get_info()

        # Initialize relevant_data with default values
        relevant_data = {key: None for key in relevant_keys}

        # Update relevant_data with available values from data
        for key in relevant_keys:
            if key in data:
                relevant_data[key] = data[key]

        if relevant_data['symbol']==None:
            continue
        for key, value in relevant_data.items():
            expected_type = expected_types[key]
            if not isinstance(value, expected_type):
                if key == 'longName' or key == 'industry' or key =='sector':
                    relevant_data[key] = ''  # Replace None with an empty string
                else:
                    relevant_data[key] = None 

        # Update or insert data into the database
        stock = StockData.query.filter_by(symbol=symbol).first()

        if stock:
            # If the stock already exists, update its data
            for key, value in relevant_data.items():
                setattr(stock, key, value)
        else:
            # If the stock doesn't exist, create a new entry
            stock = StockData(**relevant_data)
            db.session.add(stock)

        # Commit the changes to the database
        db.session.commit()


def update_stock_data(symbol):
    # Fetch data from Yahoo Finance using yfinance
        tick = yf.Ticker(symbol)
        data = tick.get_info()
        # Extract relevant keys from the data dictionary
        # Initialize relevant_data with default values
        relevant_data = {key: None for key in relevant_keys}

        # Update relevant_data with available values from data
        for key in relevant_keys:
            if key in data:
                relevant_data[key] = data[key]

        
        if relevant_data['symbol']!=None:

            for key, value in relevant_data.items():
                expected_type = expected_types[key]
                if not isinstance(value, expected_type):
                    if key == 'longName' or key == 'industry' or key =='sector':
                        relevant_data[key] = ''  # Replace None with an empty string
                    else:
                        relevant_data[key] = None 

            # Update or insert data into the database
            stock = StockData.query.filter_by(symbol=symbol).first()

            if stock:
                # If the stock already exists, update its data
                for key, value in relevant_data.items():
                    setattr(stock, key, value)
            else:
                # If the stock doesn't exist, create a new entry
                stock = StockData(**relevant_data)
                db.session.add(stock)

            # Commit the changes to the database
            db.session.commit()
        else:
            return "Stock Is Irrelevant ; Not Updated"


