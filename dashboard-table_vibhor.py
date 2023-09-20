# dashboard url
url = "https://chartink.com/dashboard/56411"



import os
import csv
import sys
import telebot
from telegram import InputFile

try:
    import requests_html
except (ModuleNotFoundError, ImportError):
    print("requests module not found")
    os.system(f"{sys.executable} -m pip install -U requests-html")
finally:
    import requests_html



session = requests_html.HTMLSession()
r = session.get(url)
r.html.render(sleep=3)
id_name = 'vgt-table'
class_name = 'vue-grid-item'


tables = r.html.find(f'.{class_name}')
for table in tables:
    final_data = []
    title = table.find('.truncate',first = True)
    tbl = table.find(f'#{id_name}',first = True)
    if tbl != None:
        for item in tbl.find('tr'):
                headerdata = [head.text.split("Sort table")[0] for head in item.find("th")]
                if headerdata:
                    final_data.append(headerdata)
                data = [head.text for head in item.find("td")]
                if 'No data for table' in data:
                    continue
                elif data:
                    final_data.append(data)
        if final_data:
            file_name = f'{title.text}.csv'
            if os.path.exists(file_name):
                os.remove(file_name)
            
            with open(file_name, mode='w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                for data in final_data:
                    csv_writer.writerow(data)  # Write header


# Set up your Telegram bot API token
TELEGRAM_BOT_TOKEN = '6499086834:AAHPQWd9YenVWV0sfmXrGB-doKo0LxMle90'
YOUR_CHAT_ID = "-1001933568192"

# import telebot
# from telegram import InputFile



# Get a list of all CSV files in the current directory
csv_files = [file for file in os.listdir() if file.endswith('.csv')]

# Create a new Telegram bot object
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Iterate over the CSV files and send them to the Telegram bot
for csv_file in csv_files:
    # Try to send the CSV data to the Telegram bot
    try:
        with open(csv_file, 'rb') as file:

            bot.send_document(YOUR_CHAT_ID, document=file)
    except Exception as e:
        print(f'Error sending CSV file to Telegram bot: {e}')

####################################################################################################################################.





