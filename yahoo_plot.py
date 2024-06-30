import sqlite3
import pandas as pd
import plotly.graph_objects as go
from updateDb import updateDb

# Function to retrieve stock data from SQLite database
def get_stock_data_from_db(symbol):
    db_file = "instance/yahoo_data.db"
    conn = sqlite3.connect(db_file)
    if symbol=="BAJAJ-AUTO":
        symbol="BAJAJAUTO"
    query = f"SELECT * FROM {symbol}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Function to plot interactive line chart for multiple stocks using Plotly
def plot_interactive_line_chart(stocks):
    fig = go.Figure()
    updateDb(stocks)
    for stock_symbol in stocks:
        stock_data = get_stock_data_from_db(stock_symbol)
        fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Close'], mode='lines', name=stock_symbol, showlegend=True))

    fig.update_layout(
        title='Stock Prices Over Time',
        xaxis_title='Date',
        yaxis_title='Closing Price',
        legend_title='Stock Symbol',
        legend=dict(orientation='h', yanchor='top', y=1.05, xanchor='right', x=1),
    )
    
    fig.update_xaxes(
        rangeslider_visible=True, 
        rangeselector=dict(buttons=list([
            dict(count=7, label='1w', step='day', stepmode='backward'),
            dict(count=1, label='1m', step='month', stepmode='backward'),
            dict(count=6, label='6m', step='month', stepmode='backward'),
            dict(count=1, label='YTD', step='year', stepmode='todate'),
            dict(count=1, label='1y', step='year', stepmode='backward'),
            dict(count=5, label='5y', step='year', stepmode='backward'),  # Added 5-year range
            dict(step='all')
        ]))
    )
    
    scale_adjustment_input = go.layout.Updatemenu(
        type='buttons',
        showactive=False,
        buttons=[
            dict(label='Linear Scale',
                 method='relayout',
                 args=['yaxis.type', 'linear']),
            dict(label='Logarithmic Scale',
                 method='relayout',
                 args=['yaxis.type', 'log']),
        ],
        x=1.05,
        xanchor='left',
        y=0.9,
        yanchor='top',
    )
    
    fig.update_layout(updatemenus=[scale_adjustment_input])
    
    for stock_symbol in stocks:
        fig.add_trace(go.Scatter(x=[], y=[], name=stock_symbol, showlegend=True))


    layout = {
        'title': 'Stock Prices Over Time',
        'xaxis_title': 'Date',
        'yaxis_title': 'Closing Price',
        'legend_title': 'Stock Symbol',
        'legend': dict(orientation='h', yanchor='top', y=1.05, xanchor='right', x=1),
        'height': 1200, # Set your desired height
        'width':1500
    }

    fig.update_layout(**layout)
    # fig.write_html('graph.html')
    html_cont=fig.to_html(full_html=False)
    return html_cont

# Example: Plotting interactive line chart for WIPRO and TCS
# stocks_to_plot = ['TCS', 'ADANIENT', 'SBIN','LT','LTIM','WIPRO','KOTAKBANK','BAJAJAUTO']
# plot_interactive_line_chart(stocks_to_plot)
