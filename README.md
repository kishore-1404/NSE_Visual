# Trading-Simulator-and-Analyzer-Website


### Introduction

This repository contains the project focused on building a trading simulator and analyzer using real (historical) data. The project involves building an interface for analyzing stock market data through chart patterns and filters.

### Task  Overview

The primary goal of the task is to create an interactive platform for analyzing stocks. This includes fetching data for all Nifty 50 stocks, applying filters, and visualizing the data through various chart patterns.

### Features

- **Stock Data Retrieval**: Fetch historical and live data for Nifty 50 stocks using yfinance.
- **Data Storage**: Store the retrieved data in an SQLite database for efficient access.
- **Filtering and Sorting**: Apply various filters and sorting criteria on the stock data.
  - Filter by average price.
  - Sort by current price and volume.
  - Retrieve stocks in ascending and descending order by current price.
- **Interactive Visualization**: Use Plotly for creating interactive line charts for stock analysis.
- **Web Interface**: Develop a user-friendly web interface using Flask, HTML, CSS, and JavaScript.
- **Background Data Update**: Implement a background thread for continuous data updates.

### Algorithm

1. **Import Libraries**:
   - `yfinance` for stock data retrieval.
   - `plotly` for data visualization.
   - `flask` for web development.
   - `SQLAlchemy` and `sqlite` for database management.
   - `pandas` for data manipulation and storage.

2. **Database Management**:
   - Store Nifty 50 historical and live data in an SQLite database.
   - Implement `updateDb` function to update the database and plot graphs based on the updated information.

3. **Web Development**:
   - Use Flask to create routes for handling different functionalities.
   - Design a web page to integrate all backend processes with the frontend.

4. **Filtering Functions**:
   - `/stocks/filter`: Filters stocks based on specified criteria (price, volume, price difference) and returns the result as JSON.
   - `/stocks/avgP_filter`: Filters stocks with an average price greater than the current price, returning the result as JSON.
   - `/stocks/filt_lowtohigh` and `/stocks/filt_hightolow`: Retrieve stocks in ascending and descending order by the current price, returning the result as JSON.

5. **Background Data Update**:
   - Start a background thread to continuously update stock data.

### Optimizations and Design Practices

- **Data Handling Efficiency**:
  - Use `yfinance` for streamlined and accurate stock data retrieval.
  - Optimize data handling using Pandas DataFrames and SQL databases.

- **Automation**:
  - Automate dependency installation with a Makefile.
  - Implement frequent data updates.

- **Effective Visualization**:
  - Utilize Plotly for clear graphical representation and interactive user experience.

- **Modular Code Organization**:
  - Write modular and readable code with well-defined functions and comments.

- **Error Handling and User Feedback**:
  - Implement robust error handling and provide user feedback using try-except blocks.

### How to Use

1. **Setup**:
   - Open the terminal in the working folder.

2. **Install Dependencies**:
   - Run the command:
     ```sh
     make
     ```
   - Ensure `requirements.txt` is present in the working directory. If not, manually install the required libraries.

3. **Run the Application**:
   - Ensure `main.py` is present in the working directory for the make command to work efficiently.

### Conclusion

This project demonstrates the application of design practices in building a trading simulator and analyzer. The interactive platform provides various features for analyzing stock market data effectively and efficiently.
# NSE_Visual
