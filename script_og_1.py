import yfinance as yf
import tkinter as tk
from tkinter import messagebox
import time 


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

            if current_price == target_price:
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
        # Add more Nifty 50 stocks here as needed
    }

    print("Available stocks/indices to monitor:")
    for i, (name, ticker) in enumerate(nifty_tickers.items(), 1):
        print(f"{i}. {name}")

    try:
        choice = input("Select the number corresponding to the stock/index you want to monitor: ").strip()
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