mkdiimport yfinance as yf
from nsepy.derivatives import get_expiry_date, get_expiry_date_list
from nsepy import get_history
import tkinter as tk
from tkinter import messagebox
import time
from datetime import datetime

def show_alert(message):
    """Display a pop-up alert."""
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    messagebox.showinfo("Price Alert", message)
    root.destroy()

def get_stock_price(ticker):
    """Fetch the current price of the given ticker."""
    stock = yf.Ticker(ticker)
    try:
        data = stock.history(period="1d")
        if data.empty:
            raise ValueError(f"No data available for {ticker}.")
        current_price = data['Close'].iloc[-1]  # Get the latest closing price
        return current_price
    except Exception as e:
        print(f"Error fetching price data for {ticker}: {e}")
        return None

def get_nifty_option_chain():
    """Fetch the option chain for Nifty 50 from NSE using nsepy."""
    try:
        # Get today's date to find expiry for the current month
        today = datetime.today()
        year = today.year
        month = today.month
        expiry_dates = get_expiry_date_list(year, month)  # List all expiry dates for this month
        
        if not expiry_dates:
            print(f"No expiry dates found for Nifty options in {month}-{year}.")
            return None
        
        expiry_date = expiry_dates[0]  # Use the first expiry date found

        # Fetch option chain data for Nifty (Call options example)
        option_chain = get_history(symbol="NIFTY", index=True, start="2024-12-01", end="2024-12-31", option_type="CE", strike_price=20000, expiry_date=expiry_date)
        return option_chain
    except Exception as e:
        print(f"Error fetching option chain data: {e}")
        return None

def display_option_chain(option_chain):
    """Display the Nifty 50 option chain."""
    if option_chain is not None and not option_chain.empty:
        print("\nNifty 50 Option Chain (Limited Display):\n")
        print("Strike Price | CE OI | CE LTP | PE OI | PE LTP")
        print("-" * 50)
        # Displaying first 10 records, customize this as needed
        for idx, row in option_chain.head(10).iterrows():
            strike_price = row['strikePrice']
            ce_oi = row['openInterest'] if 'openInterest' in row else "NA"
            ce_ltp = row['lastPrice'] if 'lastPrice' in row else "NA"
            pe_oi = row['openInterest'] if 'openInterest' in row else "NA"
            pe_ltp = row['lastPrice'] if 'lastPrice' in row else "NA"
            print(f"{strike_price:<12} {ce_oi:<7} {ce_ltp:<7} {pe_oi:<7} {pe_ltp:<7}")
    else:
        print("No option chain data available.")

def monitor_market(ticker, buy_price, target_price, stop_loss_price):
    """Monitor the selected stock/index and trigger alerts."""
    print(f"Monitoring {ticker} prices...")
    try:
        while True:
            current_price = get_stock_price(ticker)
            if current_price is None:
                print("Retrying in 60 seconds...")
                time.sleep(60)
                continue

            print(f"Current Price of {ticker}: {current_price:.2f}")

            if current_price >= target_price:
                show_alert(f"Target price reached for {ticker}! Current price: {current_price:.2f}")
                break
            elif current_price <= stop_loss_price:
                show_alert(f"Stop-loss triggered for {ticker}! Current price: {current_price:.2f}")
                break

            time.sleep(60)  # Check the price every 60 seconds
    except KeyboardInterrupt:
        print("Monitoring stopped by user.")

def main():
    """Main function to get user inputs and start monitoring."""
    nifty_tickers = {
        "Nifty 50": "^NSEI",
        "Reliance Industries": "RELIANCE.NS",
        "TCS": "TCS.NS",
        "HDFC Bank": "HDFCBANK.NS",
        "Infosys": "INFY.NS",
        "ICICI Bank": "ICICIBANK.NS",
    }

    print("Available stocks/indices to monitor:")
    for i, (name, ticker) in enumerate(nifty_tickers.items(), 1):
        print(f"{i}. {name}")

    try:
        choice = input("Select the number corresponding to the stock/index you want to monitor (or type 'options' for Nifty 50 Option Chain): ").strip()

        if choice.lower() == 'options':
            option_chain = get_nifty_option_chain()
            display_option_chain(option_chain)
            return

        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(nifty_tickers):
            print("Invalid choice. Please restart and select a valid number.")
            return

        choice = int(choice)
        selected_name = list(nifty_tickers.keys())[choice - 1]
        selected_ticker = nifty_tickers[selected_name]

        print(f"You selected: {selected_name} ({selected_ticker})")
        buy_price = float(input("Enter your buy price: "))
        target_price = float(input("Enter your target price: "))
        stop_loss_price = float(input("Enter your stop-loss price: "))

        if target_price <= buy_price:
            print("Error: Target price must be higher than buy price.")
            return
        if stop_loss_price >= buy_price:
            print("Error: Stop-loss price must be lower than buy price.")
            return

        monitor_market(selected_ticker, buy_price, target_price, stop_loss_price)

    except ValueError:
        print("Invalid input. Please enter numeric values.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()