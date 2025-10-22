import requests
import pandas as pd
from datetime import datetime
import yagmail
API_KEY = "aa4ed1648572449c90bdf7230f4432bd"
SENDER_EMAIL = "brindhasp2006@gmail.com"
SENDER_PASS = "ywcnccobrdwlidex"
RECEIVER_EMAIL = "brindhadeviaids@gmail.com"
CSV_FILE = "crypto_data.csv"
def fetch_crypto_data():
    """Fetch crypto data from CoinMarketCap API and return a DataFrame"""
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": API_KEY}
    params = {"start": "1", "limit": "5", "convert": "USD"}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    crypto_list = []
    for crypto in data["data"]:
        crypto_list.append({
            "Name": crypto["name"],
            "Price (USD)": round(crypto["quote"]["USD"]["price"], 2),
            "Market Cap (USD)": round(crypto["quote"]["USD"]["market_cap"], 2),
            "Fetched At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    df = pd.DataFrame(crypto_list)
    print(df)
    return df
def save_to_csv(df):
    """Save DataFrame to CSV file"""
    try:
        df.to_csv(CSV_FILE, index=False)
        print(f"Data saved successfully to {CSV_FILE}")
    except Exception as e:
        print("Error saving CSV:", e)
def send_email(df):
    """Send the DataFrame as email body and attach CSV"""
    try:
        html_table = df.to_html(index=False)
        yag = yagmail.SMTP(SENDER_EMAIL, SENDER_PASS)
        subject = f"Crypto Price Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        contents = [
            "Here is your latest crypto price report:",
            html_table,
            CSV_FILE
        ]
        yag.send(to=RECEIVER_EMAIL, subject=subject, contents=contents)
        print("Email sent successfully!")
    except Exception as e:
        print("Email error:", e)
if __name__ == "__main__":
    print("Starting Crypto Price Reporter...\n")
    df = fetch_crypto_data()
    save_to_csv(df)
    send_email(df)
    