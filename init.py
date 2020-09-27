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

    md = pyRofex.get_market_data(ticker = symbol, entries = [pyRofex.MarketDataEntry.BIDS, pyRofex.MarketDataEntry.LAST])

    return md



def get_last_price(md):
    """Returns the last price of the symbol."""

    if md["marketData"]["LA"] == None:
        last_price = None
    else:
        last_price = md["marketData"]["LA"]["price"]

    return last_price
    


def run():
    user = credentials.user
    password = credentials.password
    account = credentials.account

    if login(user, password, account):
        symbol = input("Input symbol: ")

        md = get_marketdata(symbol)

        if md["status"] == "OK":
            
            last_price = get_last_price(md)
            print(f"Last price: {last_price}")

        else:
            print("Invalid symbol.")
            return






    else:
        print("Closing.")
        return



if __name__ == "__main__":
    run()