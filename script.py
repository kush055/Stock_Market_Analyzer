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

def get_nifty_price():
    """Fetch the current Nifty 50 price."""
    ticker = "^NSEI"  # Yahoo Finance ticker for Nifty 50
    nifty = yf.Ticker(ticker)
    data = nifty.history(period="1d")
    current_price = data['Close'].iloc[-1]  # Get the latest closing price
    return current_price

def monitor_market(buy_price, target_price, stop_loss_price):
    """Monitor Nifty 50 and trigger alerts."""
    print("Monitoring Nifty 50 prices...")
    while True:
        current_price = get_nifty_price()
        print(f"Current Nifty 50 Price: {current_price:.2f}")

        if current_price >= target_price:
            show_alert(f"Target price reached! Current price: {current_price:.2f}")
            break
        elif current_price <= stop_loss_price:
            show_alert(f"Stop-loss triggered! Current price: {current_price:.2f}")
            break

        time.sleep(60)  # Check the price every 60 seconds

def main():
    """Main function to get user inputs and start monitoring."""
    try:
        buy_price = float(input("Enter your buy price: "))
        target_price = float(input("Enter your target price: "))
        stop_loss_price = float(input("Enter your stop-loss price: "))

        if target_price <= buy_price:
            print("Error: Target price must be higher than buy price.")
            return
        if stop_loss_price >= buy_price:
            print("Error: Stop-loss price must be lower than buy price.")
            return

        monitor_market(buy_price, target_price, stop_loss_price)

    except ValueError:
        print("Invalid input. Please enter numeric values.")

if __name__ == "__main__":
    main()
