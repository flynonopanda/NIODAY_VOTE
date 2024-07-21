import requests
import json
import time
import schedule
from datetime import datetime
import pandas as pd

# Constants
API_URL = "https://gateway-front-external.nio.com/moat/10086/app/bs/mix/in/xgc/content/536984?app_ver=9.9.9&app_id=10086"
HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Authorization": "Bearer",
    "Content-Type": "application/json;charset=utf-8",
    "Dnt": "1",
    "If-None-Match": 'W/"66c3-G93B+/IdMHeaNgic29kjgB1Pcv8"',
    "Origin": "https://app.nio.com",
    "Referer": "https://app.nio.com/",
    "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"macOS"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}

# Function to fetch vote data
def fetch_vote_data():
    try:
        response = requests.get(API_URL, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            options = data['data']['votes'][0]['questions'][0]['options']
            guangzhou_votes = next(option['votes'] for option in options if option['id'] == '105144')
            hangzhou_votes = next(option['votes'] for option in options if option['id'] == '105145')

            now = datetime.now().strftime("%H:%M")
            difference = hangzhou_votes - guangzhou_votes

            new_row = {"时间": now, "杭州": hangzhou_votes, "广州": guangzhou_votes, "票差": difference}

            # Load existing data if exists
            try:
                df = pd.read_csv('vote_results.csv')
            except FileNotFoundError:
                df = pd.DataFrame(columns=["时间", "杭州", "广州", "票差"])

            # Remove any existing row with the same time to avoid duplicates
            df = df[df["时间"] != now]

            # Append the new row at the top
            df = pd.concat([pd.DataFrame([new_row]), df], ignore_index=True)
            df.to_csv('vote_results.csv', index=False)  # Save the DataFrame to a CSV file

            # Confirm writing
            written_df = pd.read_csv('vote_results.csv')
            if not written_df.empty and written_df.iloc[0].equals(pd.Series(new_row)):
                print(f"New data written to file: 时间: {now}, 杭州: {hangzhou_votes}, 广州: {guangzhou_votes}, 票差: {difference}")
            else:
                print(f"Failed to write new data to file: {new_row}")

        else:
            print(f"Failed to fetch data: {response.status_code}")
            print(response.text)  # Print the error message if failed
    except Exception as e:
        print(f"An error occurred: {e}")

# Schedule the fetch_vote_data function to run every minute
schedule.every(1).minutes.do(fetch_vote_data)

if __name__ == "__main__":
    print("Starting data collection...")
    while True:
        schedule.run_pending()
        time.sleep(1)