# Stock Data Analysis Project

This project is designed to retrieve and analyze historical stock data using the **EOD Historical Data API**. It includes tools for analyzing stock performance, calculating volatility, finding correlations, and visualizing various key metrics. The project also allows users to screen stocks based on performance.

## Features

- **Data Retrieval**: Get historical stock data using the EOD Historical Data API.
- **Volatility Analysis**: Calculate stock volatility using rolling windows and log returns.
- **Performance Visualization**: Plot stock performance trends and return distributions over time.
- **Correlation Analysis**: Analyze and visualize correlations between multiple stock closing prices.
- **Stock Screener**: Screen stocks based on their 52-week highs and identify top performers.

## Requirements

Ensure you have the following Python libraries installed:

```bash
pip install numpy pandas matplotlib seaborn requests eod
Setup
Clone the Repository
Clone this repository to your local machine:

bash
Copy code
git clone <repository-url>
API Key
Sign up for an API key from EOD Historical Data. Store the API key in a text file (e.g., notApiKey.txt) in your project directory.

Run the Application
Navigate to the directory where app.py is located and run the following command to start the application:

bash
Copy code
python3 app.py
This will begin pulling stock data and running the analysis.

Usage
Volatility Plot: Generate a scatter plot to visualize stock volatility and return magnitudes.
Performance Graph: Create performance visualizations for multiple stocks.
Stock Screener: Identify stocks trading near their 52-week highs.
Correlation Plot: Visualize the correlation between the closing prices of various stocks.
Example
Here is a sample of how to retrieve stock data and generate some basic analysis:

python
Copy code
# Example usage to retrieve and analyze stock data
apiKey = 'your_api_key_here'
tickers = ['AAPL', 'GOOG', 'AMZN']
returns, current_returns, pct_change = getReturnData(*tickers, key=apiKey)

# Plot performance graph for a folder of stock data
performanceGraph('data_files')
Functions
getStockData: Retrieves stock data for a given stock exchange.
getData: Pulls stock data for specific tickers and saves them as CSV files.
getCLP: Retrieves closing prices from CSV files and concatenates them.
performanceGraph: Visualizes stock performance by plotting the percentage change in stock prices.
getSP500: Retrieves a list of S&P 500 stocks based on a specific sector.
getReturnData: Calculates returns, percentage changes, and exports them to Excel.
