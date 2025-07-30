import time
import yfinance as yf

def fetch_option_chain(ticker):
    """
    Fetches the price data for the specified ticker.
    """
    try:
        instrument = yf.Ticker(ticker)

        # Fetching historical data or live data
        option_data = instrument.history(period="1d")
        last_price = option_data["Close"][-1]  # Last closing price
        return last_price

    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def notify(title, message):
    """
    Sends a desktop notification.
    """
    print(f"{title}: {message}")

def main():
    print("Welcome to the Option Chain Monitor!")
    
    # User inputs
    ticker = input("Enter the ticker symbol (e.g., ^NSEI for Nifty50): ").strip()
    option_type = input("Do you want to monitor a Call or Put option? (call/put): ").strip().lower()
    
    if option_type not in ["call", "put"]:
        print("Invalid option type. Please choose either 'call' or 'put'.")
        return

    try:
        # Get user inputs for trading parameters
        strike_price = float(input("Enter the strike price to monitor: "))
        target_price = float(input("Enter the target price to sell: "))
        stop_loss = float(input("Enter the stop-loss price to exit: "))
    except ValueError:
        print("Invalid input. Please enter numeric values for prices.")
        return

    print(f"Monitoring {ticker} {option_type.upper()} option with Strike Price: {strike_price}, Target Price: {target_price}, Stop Loss: {stop_loss}")
    
    # Initialize tracking for notifications
    notified_levels = set()

    while True:
        try:
            # Fetch the price
            current_price = fetch_option_chain(ticker)
            if current_price is None:
                print(f"Error fetching price for {ticker}. Retrying...")
                time.sleep(10)  # Retry quickly if there's an error
                continue

            print(f"Current price for {ticker}: {current_price}")

            # Notify user if the target price is reached
            if current_price == target_price:
                notify("Target Hit", f"{option_type.upper()} Target achieved at {current_price} (Strike: {strike_price})")
                break  # Stop monitoring after hitting the target
            
            # Notify user at intermediate levels (e.g., every increment of 5%)
            increment = (target_price - stop_loss) * 0.05
            level_to_notify = stop_loss + increment * len(notified_levels)
            
            if current_price >= level_to_notify and level_to_notify not in notified_levels:
                notify("Price Update", f"Price reached {current_price}. Target is {target_price}.")
                notified_levels.add(level_to_notify)

            # Notify user if stop-loss is triggered
            if current_price == stop_loss:
                notify("Stop Loss Hit", f"{option_type.upper()} Stop loss triggered at {current_price} (Strike: {strike_price})")
                break  # Stop monitoring after stop-loss

            time.sleep(5)  # Check every 5 seconds
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)  # Retry quickly if there's an error

if __name__ == "__main__":
    print("Starting the Option Chain Monitor...")
    main()