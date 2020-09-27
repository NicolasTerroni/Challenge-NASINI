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
    print(f"Logged in as: {credentials.user}")
    return True



def run():
    user = credentials.user
    password = credentials.password
    account = credentials.account

    login(user, password, account)
        #symbol = input("Input symbol: ")




if __name__ == "__main__":
    run()