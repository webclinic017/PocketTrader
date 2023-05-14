# encoding: utf-8
import sys
import time

# Importing API
from alpaca.trading.client import TradingClient
from alpaca.data import CryptoHistoricalDataClient, StockHistoricalDataClient
from alpaca.data.live import StockDataStream

# Importing necessary files
import config
from logger import *
from PocketTrader import Trader


def check_account_status(api):
    try:
        account = api.get_account()
        if account.status != "ACTIVE":
            logging.info("The account is not ACTIVE, aborting")
            sys.exit()
    except Exception as e:
        logging.error("Could not get account info, aborting")
        logging.info(str(e))
        sys.exit()


def cancel_all_orders(api):
    logging.info("Cancelling all orders...")

    try:
        api.cancel_orders()
        logging.info("All orders cancelled")
    except Exception as e:
        logging.error("Could not cancel all orders")
        logging.error(e)
        sys.exit()


def is_asset_tradable(api, ticker):
    try:
        asset = api.get_asset(ticker)
        if asset.tradable:
            logging.info("Asset exists and is tradable")
            return True
        else:
            logging.info("Asset exists but not tradable, exiting")
            sys.exit()
    except Exception as e:
        logging.error("Asset does not exist or something happened!")
        logging.error(e)
        sys.exit()


def main():
    # paper=True enables paper trading
    api = TradingClient(config.API_KEY, config.SECRET_KEY, paper=True)

    # keys required - real time data for later
    # stock_stream = StockDataStream(config.API_KEY, config.SECRET_KEY)

    initialize_logging()

    check_account_status(api)

    cancel_all_orders(api)

    ticker = input("INSERT TICKER: ")

    is_asset_tradable(api, ticker)

    trader = Trader(ticker, api)

    while True:
        trading_success = trader.run(ticker)

        if not trading_success:
            logging.info("Trading was not successful, locking asset")
            time.sleep(config.sleepTimeME)
        else:
            logging.info("Trading was successful!")
            time.sleep(config.sleepTimeME)


if __name__ == "__main__":
    main()
