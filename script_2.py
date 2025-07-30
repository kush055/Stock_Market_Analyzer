from kiteconnect import KiteConnect
import time

# User-defined parameters
STRIKE_PRICE = 18000
TARGET_PRICE = 150
BUY_PRICE = 100
STOP_LOSS = 80

# Kite Connect credentials
API_KEY = "your_api_key"  # Replace with your API key
API_SECRET = "your_api_secret"  # Replace with your API secret
ACCESS_TOKEN = "your_access_token"  # Replace with the access token after login

kite = KiteConnect(api_key=API_KEY)

def fetch_option_chain():
    """
    Fetches option chain data for Nifty50.
    """
    try:
        # Get instruments for NFO (Nifty Futures and Options)
        instruments = kite.instruments(exchange="NFO")
        nifty_instruments = [
            i for i in instruments if i["tradingsymbol"].startswith("NIFTY") and i["instrument_type"] == "CE"
        ]

        # Fetch details for the desired strike price
        for instrument in nifty_instruments:
            if instrument["strike"] == STRIKE_PRICE:
                ltp = kite.ltp(instrument["tradingsymbol"])
                return ltp["last_price"]
        return None
    except Exception as e:
        print(f"Error fetching option chain: {e}")
        return None

def notify(title, message):
    """
    Sends a desktop notification.
    """
    print(f"{title}: {message}")

def main():
    while True:
        try:
            # Fetch the option chain
            current_price = fetch_option_chain()
            if current_price is None:
                print(f"Strike price {STRIKE_PRICE} not found. Retrying...")
                time.sleep(60)
                continue

            print(f"Current price for strike {STRIKE_PRICE}: {current_price}")

            # Check thresholds
            if current_price == BUY_PRICE:
                notify("Buy Alert", f"Buy at {current_price} (Strike: {STRIKE_PRICE})")
            elif current_price >= TARGET_PRICE:
                notify("Target Hit", f"Target achieved at {current_price} (Strike: {STRIKE_PRICE})")
            elif current_price <= STOP_LOSS:
                notify("Stop Loss Hit", f"Stop loss triggered at {current_price} (Strike: {STRIKE_PRICE})")

            time.sleep(5)  # Check every 60 seconds
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    # Log in to get access token
    print("Visit the following URL to login and get the request token:")
    print(kite.login_url())
    request_token = input("Enter the request token: ").strip()
    data = kite.generate_session(request_token, api_secret=API_SECRET)
    ACCESS_TOKEN = data["access_token"]
    kite.set_access_token(ACCESS_TOKEN)

    # Start monitoring
    main()
