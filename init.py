"""Main file"""
# Debugger
import pdb
# pyRofex
import pyRofex
# Credentials
import credentials

def login(user, password, account):
    """Tries to login."""

    print("Logging in reMarkets.")
    try:
        pyRofex.initialize(user, password, account, pyRofex.Environment.REMARKET)
    except:
        print("Failed to log in.")
        return False
    print(f"Logged in as: {user}")
    return True


def get_marketdata(symbol):
    """Gets the market data of an instrument"""

    print(f"Getting MarketData from {str(symbol)}")
    try:
        md = pyRofex.get_market_data(ticker = symbol, entries = [pyRofex.MarketDataEntry.BIDS, pyRofex.MarketDataEntry.LAST])
    except:
        print("Invalid symbol.")
        return
    return md


def run():
    user = credentials.user
    password = credentials.password
    account = credentials.account

    if login(user, password, account):
        symbol = input("Input symbol: ")

        md = get_marketdata(symbol)





if __name__ == "__main__":
    run()