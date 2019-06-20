# app/robo_advisor.py
#### time 1:09

# modules
import json
import csv
import os

# package
from dotenv import load_dotenv
import requests

load_dotenv()

# function to convert numbers to USD
def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

# Information Inputs

symbol = "MSFT"
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

response = requests.get(request_url)

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys())

latest_day = dates[0]
latest_close = tsd[latest_day]["4. close"]


# maximum of all the high prices
high_prices = []

# minimum of all the low prices
low_prices = []

for date in dates: 
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)

# Information Outputs

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers, lineterminator='\r')
    writer.writeheader() # uses fieldnames set above
    for date in dates:
        prices = {}
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date, 
            "open": to_usd(float(daily_prices["1. open"])),
            "high": to_usd(float(daily_prices["2. high"])),
            "low": to_usd(float(daily_prices["3. low"])),
            "close": to_usd(float(daily_prices["4. close"])),
            "volume": daily_prices["5. volume"]
        })



print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


