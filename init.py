"""Main file"""

# python
import sys
import getopt
import pdb
# pyRofex
import pyRofex


def login(user, password, account):
    """Tries to login."""

    print("Logging in reMarkets..")
    try:
        pyRofex.initialize(user=user,
                   password=password,
                   account=account,
                   environment=pyRofex.Environment.REMARKET)
    except:
        print("""
Failed to log in.
Checkout your parameters and run:
python init.py <symbol> -u <user> -p <password>
Put your params in quotes if they have a special character.
""")
        return False
    print(f"Logged in as: {user}")
    return True


def get_marketdata(symbol):
    """Gets the market data of an instrument"""

    print(f"Getting MarketData from '{str(symbol)}'")

    md = pyRofex.get_market_data(
        ticker = symbol, 
        entries = [
            pyRofex.MarketDataEntry.BIDS, 
            pyRofex.MarketDataEntry.LAST])

    return md


def get_last_price(md):
    """Returns the last price of the symbol."""

    if md["marketData"]["LA"] == None:
        last_price = None
    else:
        last_price = md["marketData"]["LA"]["price"]

    return last_price
    

def get_bid(md):
    """Returns the bid of the symbol."""
    print("Consulting BID.")

    if len(md["marketData"]["BI"]) < 1:
        bid = None
    else:
        bid = md["marketData"]["BI"][0]["price"]

    return bid


def send_buy_order(symbol ,buy_order_price):
    """Sends a buy order to the market"""
    print(f"Sending a buy order at: ${buy_order_price}")

    try:
        order = pyRofex.send_order(ticker=symbol,
                           side=pyRofex.Side.BUY,
                           size=1,
                           price=buy_order_price,
                           order_type=pyRofex.OrderType.LIMIT)
    except:
        print("Could not send the buy order. Check if the account is correct.")
        return

    return order


def logout():
    print("Loggin out reMarkets.")
    sys.exit()


def run():
    user = None
    password = None
    account = 'REM5049'

    argv = sys.argv[1:]
    symbol = argv[0]
    argv = argv[1:]
    # extracts the symbol and creates a new argv with only user and password


    try:
        opts, args = getopt.getopt(argv, "u:p:") #falta a:
        # converts the params list in a list of tuples
    except getopt.GetoptError as err:
        print("""Failed to run. Use:
python init.py <symbol> -u <user> -p <password>
Put your params in quotes if they have a special character.""")
        sys.exit()


    for opt, arg in opts:
        if opt == "-u":
            user = arg
        elif opt == "-p":
            password = arg


    if login(user, password, account):

        md = get_marketdata(symbol)

        if md["status"] == "OK":

            # LP
            last_price = get_last_price(md)
            print(f"Last price: {last_price}")

            # BID
            bid = get_bid(md)
            if bid == None:
                print("No active BIDs.")
                buy_order_price = 75.25
            else:
                print(f"BID price: {bid}")
                buy_order_price = (bid-0.01)

            # BUY ORDER
            order = send_buy_order(symbol, buy_order_price)
            pdb.set_trace()

            logout()

        else:
            print("Invalid symbol.")
            logout()

    else:
        print("Closing.")


if __name__ == "__main__":
    run()