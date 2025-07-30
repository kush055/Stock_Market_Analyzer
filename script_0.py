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

def get_price(ticker_symbol):
    """Fetch the current price for the given ticker."""
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period="1d")
    current_price = data['Close'].iloc[-1]  # Get the latest closing price
    return current_price

def monitor_market(ticker_symbol, buy_price, target_price, stop_loss_price):
    """Monitor the market and trigger alerts."""
    print(f"Monitoring prices for {ticker_symbol}...")
    while True:
        current_price = get_price(ticker_symbol)
        print(f"Current Price of {ticker_symbol}: {current_price:.2f}")

        if current_price >= target_price:
            show_alert(f"Target price reached! Current price of {ticker_symbol}: {current_price:.2f}")
            break
        elif current_price <= stop_loss_price:
            show_alert(f"Stop-loss triggered! Current price of {ticker_symbol}: {current_price:.2f}")
            break

        time.sleep(60)  # Check the price every 60 seconds

def main():
    """Main function to get user inputs and start monitoring."""
    try:
        print("Choose an option:")
        print("1. Nifty 50 (^NSEI)")
        print("2. Sensex (^BSESN)")
        print("3. Custom Ticker")
        choice = int(input("Enter your choice (1/2/3): "))

        if choice == 1:
            ticker_symbol = "^NSEI"
        elif choice == 2:
            ticker_symbol = "^BSESN"
        elif choice == 3:
            ticker_symbol = input("Enter the ticker symbol: ").strip()
        else:
            print("Invalid choice.")
            return

        buy_price = float(input("Enter your buy price: "))
        target_price = float(input("Enter your target price: "))
        stop_loss_price = float(input("Enter your stop-loss price: "))

        if target_price <= buy_price:
            print("Error: Target price must be higher than buy price.")
            return
        if stop_loss_price >= buy_price:
            print("Error: Stop-loss price must be lower than buy price.")
            return

        monitor_market(ticker_symbol, buy_price, target_price, stop_loss_price)

    except ValueError:
        print("Invalid input. Please enter numeric values.")

if __name__ == "__main__":
    main()
