"""Main file"""

# python
import sys
import getopt
import pdb
import time
# pyRofex
import pyRofex


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


def logout():
    """Close the websocket connection and the app execution."""

    print("Loggin out reMarkets.")
    time.sleep(1)
    pyRofex.close_websocket_connection()
    sys.exit()


def login(user, password, account):
    """Tries to login to the enviroment."""

    print("Logging in reMarkets..")

    try:
        pyRofex.initialize(
            user=user,
            password=password,
            account=account,
            environment=pyRofex.Environment.REMARKET)
    except:
        print("""Failed to log in. Run:
        python init.py <symbol> -u <user> -p <password> -a <account>
        Put your params in quotes if they have a special character.""")
        sys.exit()
    
    print(f"Logged in as: {user}")


def market_data_handler(md):
    global symbol
    global account

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
        
    time.sleep(3)

    # ORDER
    pyRofex.send_order(
        ticker=symbol,
        side=pyRofex.Side.BUY,
        size=1,
        price=buy_order_price,
        account= account,
        order_type=pyRofex.OrderType.LIMIT)


    logout()


def order_report_handler(order):
    time.sleep(2)
    print(f"Sending a buy order at: {order['orderReport']['price']}")

    print(f"Symbol: '{order['orderReport']['instrumentId']['symbol']}'")
    print(f"Timestamp: {order['timestamp']}")
    print(f"{order['orderReport']['text']}")
    print("")
    logout()


def error_handler(message):
    print(f"Error Message Received: {message}")


def exception_handler(exception):
    print(f"Exception Occurred: {exception}")
    

def run():
    account = None
    user = None
    password = None
    
    argv = sys.argv[1:]
    symbol = [argv[0],]
    argv = argv[1:]
    # extracts the symbol and creates a new argv with only user and password

    try:
        opts, args = getopt.getopt(argv, "u:p:a:")
        # converts the params list in a list of tuples
    except getopt.GetoptError as err:
        print("""Failed to run. Run:
        python init.py <symbol> -u <user> -p <password> -a <account>
        Put your params in quotes if they have a special character.""")
        sys.exit()


    for opt, arg in opts:
        if opt == "-a":
            account = arg
        elif opt == "-u":
            user = arg
        elif opt == "-p":
            password = arg


    login(user, password, account)


    pyRofex.init_websocket_connection(
        order_report_handler=order_report_handler,
        market_data_handler=market_data_handler,
        error_handler=error_handler,
        exception_handler=exception_handler
        )


    # SUBSCRIPTIONS
    pyRofex.market_data_subscription(
        symbol, 
        [pyRofex.MarketDataEntry.LAST,
        pyRofex.MarketDataEntry.BIDS]
        )

    time.sleep(2)

    pyRofex.order_report_subscription()
    

if __name__ == "__main__":
    run()