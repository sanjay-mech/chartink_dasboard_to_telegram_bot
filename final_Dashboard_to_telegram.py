import time
import os
import csv
import sys
from requests_html import HTMLSession
import telebot
import pandas as pd
import schedule  # Import the schedule library

TELEGRAM_BOT_TOKEN = '6499086834:AAHPQWd9YenVWV0sfmXrGB-doKo0LxMle90'
YOUR_CHAT_ID = "-1001933568192"
url = "https://chartink.com/dashboard/192776"

try:
    import requests_html
except (ModuleNotFoundError, ImportError):
    print("requests module not found")
    os.system(f"{sys.executable} -m pip install -U requests-html")

def scrape_and_send():
    # Initialize the HTMLSession
    session = HTMLSession()
    r = session.get(url)
    r.html.render(sleep=3)
    id_name = 'vgt-table'
    class_name = 'vue-grid-item'

    tables = r.html.find(f'.{class_name}')
    for table in tables:
        final_data = []
        title = table.find('.truncate', first=True)
        tbl = table.find(f'#{id_name}', first=True)
        if tbl is not None:
            for item in tbl.find('tr'):
                headerdata = [head.text.split("Sort table")[0] for head in item.find("th")]
                if headerdata:
                    final_data.append(headerdata)
                data = [head.text for head in item.find("td")]
                if data:
                    final_data.append(data)
            if final_data:
                # Create a CSV file with a unique name based on the timestamp
                timestamp = int(time.time())
                file_name = f'{title.text}.csv'
                with open(file_name, mode='w', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    for data in final_data:
                        csv_writer.writerow(data)  # Write data to CSV

                # Read CSV using pandas with the first row as headers
                df = pd.read_csv(file_name)

                # Exclude the "Volume" column
                df = df.drop(columns=['Volume '])

                # Check if the DataFrame is not empty
                if not df.empty:
                    # Extract symbols, prices, and change
                    symbols = df['Symbol '].tolist()
                    prices = df['Price '].tolist()
                    change = df['% change '].tolist()

                    # Create a list of symbol, price, and change pairs with file name
                    symbol_price_list = [f"Symbol: {symbol}, Price: {price}, Change: {chg}%" for symbol, price, chg in zip(symbols, prices, change)]
                    
                    # Join the list items into a single message
                    message = f"Screener Name: {file_name}\n\n" + "\n".join(symbol_price_list)

                    # Send the message
                    bot = telebot.TeleBot(token=TELEGRAM_BOT_TOKEN)
                    bot.send_message(chat_id=YOUR_CHAT_ID, text=message)
                else:
                    print(f"The CSV file {file_name} is empty.")
            else:
                print("No data found on the webpage.")

# Schedule the job to run every 15 minutes
schedule.every(0).minutes.do(scrape_and_send)

while True:
    schedule.run_pending()
    time.sleep(1)
