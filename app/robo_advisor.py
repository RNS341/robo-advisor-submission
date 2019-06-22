# app/robo_advisor.py

# modules
import json # to parse JSON
import csv # to export to CSV
import os # operating system dependent functionality
import datetime

# packages
from dotenv import load_dotenv
import requests
import pandas as pd

load_dotenv() # loads from .env

# function to convert numbers to USD
def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

# obtain a list of tickers

symbol = input("Please enter ticker symbol, if finished type DONE ")
stop_loop = ["Done","done","DONE"]
investor_data = {}

while symbol not in stop_loop: 
    api_key = os.environ.get("ALPHAVANTAGE_API_KEY") #sets variable api_key to user API key
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
    test = False

    while test == False:
        if 'Error Message' in parsed_response.keys():
            symbol = input("Ticker invalid.  Please enter a new ticker: ")
            request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
            response = requests.get(request_url)
            parsed_response = json.loads(response.text)
        else: 
            test = True
    
    investor_data[symbol] = {"last_refreshed": [], "close_date": [], "latest_close": [], "recent_high": [], "recent_low": [], "recommendation": []}
    tsd = parsed_response["Time Series (Daily)"]
    dates = list(tsd.keys()) #create a list of all dates
    latest_day = dates[0] #reference the first date which is the most recent
    investor_data[symbol]["last_refreshed"] = parsed_response["Meta Data"]["3. Last Refreshed"]
    investor_data[symbol]["latest_close"] = tsd[latest_day]["4. close"]
    investor_data[symbol]["close_date"] = dates[0]
    
    # find high and low price
    high_prices = []
    low_prices = []

    for date in dates: 
        high_price = tsd[date]["2. high"]
        high_prices.append(float(high_price))
        low_price = tsd[date]["3. low"]
        low_prices.append(float(low_price))

    investor_data[symbol]["recent_high"] = max(high_prices)
    investor_data[symbol]["recent_low"] = min(low_prices)

    if float(investor_data[symbol]["latest_close"]) < float(investor_data[symbol]["recent_low"]) * 1.2:
        investor_data[symbol]["recommendation"] = "Buy"
    else:
        investor_data[symbol]["recommendation"] = "Hold"

    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", symbol + ".csv")

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
    symbol = input("Please enter another ticker or type 'DONE': ")

symbol_keys = list(investor_data.keys())

date_time = datetime.date.today()

print("\n")
print("-------------------------")
print(f"REQUEST AT: {date_time}")
print("-------------------------")


for key in symbol_keys:

    print("\n")
    print("-------------------------")
    print(f"Stock Ticker: {key}")
    print("-------------------------")
    print("LATEST DAY: ", investor_data[key]["last_refreshed"])
    #print(f"LATEST DAY: {last_refreshed}")
    print("LATEST CLOSE: ", to_usd(float(investor_data[key]["latest_close"])))
    #print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
    print("RECENT HIGH: ", to_usd(float(investor_data[key]["recent_high"])))
    #print(f"RECENT HIGH: {to_usd(float(recent_high))}")
    print("RECENT LOW: ", to_usd(float(investor_data[key]["recent_low"])))
    #print(f"RECENT LOW: {to_usd(float(recent_low))}")
    print("-------------------------")
    print(investor_data[key]["recommendation"])
    print("RECOMMENDATION: BUY!")
    print("RECOMMENDATION REASON: TODO")
    print("-------------------------")
    #print(f"DATA WRITTEN TO 'PRICES.CSV': {csv_file_path}...")
    print("-------------------------")


print("\n")
