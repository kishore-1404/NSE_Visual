import sqlite3
import yfinance as yf
from datetime import date,datetime


def updateDb(table_list):
    conn = sqlite3.connect('instance/yahoo_data.db')
    cursor = conn.cursor()
    # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # table_names = cursor.fetchall()
    # table_list = [table[0] for table in table_names]

    for symbol in table_list:
        if symbol=="BAJAJ-AUTO":
            symbol="BAJAJAUTO"
        cursor.execute(f"SELECT Date FROM '{symbol}' ORDER BY Date DESC LIMIT 1")
        start_date=cursor.fetchone()[0]
        end_date=date.today().strftime('%Y-%m-%d')
#if last entry is not today
        if start_date<=end_date:
            day_difference=(datetime.strptime(end_date,'%Y-%m-%d')-datetime.strptime(start_date, '%Y-%m-%d')).days+1
            if symbol=="BAJAJAUTO":
                symbol="BAJAJ-AUTO"
            stock_data = yf.download(symbol+'.NS',period=f'{day_difference}d',interval='1d')
            if symbol=="BAJAJ-AUTO":
                symbol="BAJAJAUTO"
            stock_data.index = stock_data.index.astype(str)

            if not stock_data.empty:
                for index, row in stock_data.iterrows():
                    if symbol=="BAJAJ-AUTO":
                        symbol="BAJAJAUTO"
                    date_checker= f"SELECT COUNT(*) FROM {symbol} WHERE Date = '{index}'"
                    result = conn.execute(date_checker).fetchone()[0]
                    if result>0:
                        update_query = f"""UPDATE {symbol} SET Open = {row['Open']},Close = {row['Close']},High = {row['High']},Low = {row['Low']},[Adj Close] = {row['Adj Close']},Volume = {row['Volume']} WHERE Date = '{index}'"""
                        cursor.execute(update_query)
                    else:
                        update_query=f"""INSERT INTO {symbol} (Date, Open, Close, High, Low, [Adj Close], Volume) VALUES ('{index}',{row['Open']}, {row['Close']}, {row['High']}, {row['Low']},{row['Adj Close']}, {row['Volume']})"""
                        cursor.execute(update_query)
    conn.commit()
    conn.close()