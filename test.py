
import yfinance as yf
import pandas as pd

apple_stock = yf.Ticker("AAPL")

price = apple_stock.info["regularMarketPrice"]

print("The price of Apple stock today is:", price)

# Get the last week's prices
last_week_prices = apple_stock.history(period="1week")

# Print the table
print(pd.DataFrame(last_week_prices))

# Show the table of the last week's prices using pandas
last_week_prices_table = pd.DataFrame(last_week_prices)
print(last_week_prices_table)

