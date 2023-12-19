# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 15:12:20 2021

@author: Zain
"""
import threading
import time
import winsound
from os import system

from bs4 import BeautifulSoup as bsp
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.chrome.options import Options
from web3 import Web3
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager

from BuyTokens import buyTokens
# from CommandPromptVisuals import changeCmdPosition
from SellTokens import sellTokens
from ThreadingWithReturn import ThreadWithResult
from abi import tokenAbi
from sendWhatsappMessage import sendMessage
import config as config
from decimalData import getTokenDecimal

bsc = 'https://bsc-dataseed.binance.org/'
web3 = Web3(Web3.HTTPProvider(bsc))
if web3.isConnected(): print("Connected to BSC")

# User Input Address for Token
if bool(config.TRADE_TOKEN_ADDRESS):
    address = config.TRADE_TOKEN_ADDRESS
else:
    address = input('Enter token address: ')

# Important Addresses
TokenToSellAddress = web3.toChecksumAddress(address)
WBNB_Address = web3.toChecksumAddress(config.WBNB_ADDRESS)
pancakeRouterAddress = web3.toChecksumAddress(config.PANCAKE_ROUTER_ADDRESS)
walletAddress = config.YOUR_WALLET_ADDRESS
TradingTokenDecimal = None

# To clear command line
clear = lambda: system("cls")
options = Options()
options.headless = True
# options.add_argument("--enable-javascript")
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)

# Numbers to send Whatsapp web message
numbersToNotify = ['+92*********']


def showTx(url):
    webdriver.Chrome(executable_path=ChromeDriverManager().install()).get(url)


def InitializeTrade():
    global driver
    global TokenToSellAddress
    global TradingTokenDecimal
    # Getting ABI
    sellTokenAbi = tokenAbi(TokenToSellAddress, driver)
    pancakeAbi = tokenAbi(pancakeRouterAddress, driver)

    # Enter you wallet Public Address
    BNB_balance = web3.eth.get_balance(walletAddress)
    BNB_balance = web3.fromWei(BNB_balance, 'ether')
    # print(f"Current BNB Balance: {web3.fromWei(BNB_balance, 'ether')}")

    # Create a contract for both PancakeRoute and Token to Sell
    contractPancake = web3.eth.contract(address=pancakeRouterAddress, abi=pancakeAbi)
    contractSellToken = web3.eth.contract(TokenToSellAddress, abi=sellTokenAbi)
    if TradingTokenDecimal is None:
        TradingTokenDecimal = contractSellToken.functions.decimals().call()
        TradingTokenDecimal = getTokenDecimal(TradingTokenDecimal)

    # Get current avaliable amount of tokens from the wallet
    NoOfTokens = contractSellToken.functions.balanceOf(walletAddress).call()
    NoOfTokens = web3.fromWei(NoOfTokens, TradingTokenDecimal)
    symbol = contractSellToken.functions.symbol().call()
    params = {
        'symbol': symbol,
        'web3': web3,
        'walletAddress': walletAddress,
        'contractSellToken': contractSellToken,
        'contractPancake': contractPancake,
        'pancakeRouterAddress': pancakeRouterAddress,
        'TokenToSellAddress': TokenToSellAddress,
        'WBNB_Address': WBNB_Address,
        'TradingTokenDecimal': TradingTokenDecimal
    }
    return BNB_balance, symbol, NoOfTokens, params


def notifyWithSound():
    for i in range(5):
        winsound.PlaySound("beep.wav", winsound.SND_ALIAS)


def runCode():
    url = f'https://swap.arken.finance/tokens/bsc/{address}'
    driver.get(url)
    clear()
    time.sleep(3)
    dataEntered = False
    updateDataCount = 0
    updateData = True
    Lasttrade_message = None
    tx = None

    # Change CMD Promt position
    # changeCmdPosition()

    while True:
        # Getting Price
        page_soup = bsp(driver.page_source, features="lxml")
        price = float(page_soup.find_all("b", {"class": "number"})[0].text[1:].replace(",", ""))

        """ If You want to update wallet tokens and BNB info after every 10 seconds Uncomment the code below """
        # if updateDataCount == 10 or updateData:
        #     clear()
        #     BNB_balance, TokenSymbol, NoOfTokens, params = InitializeTrade()
        #     updateDataCount = 0
        #     updateData = False
        #     clear()
        # updateDataCount += 1

        if not dataEntered:
            BNB_balance, TokenSymbol, NoOfTokens, params = InitializeTrade()

            title = TokenSymbol
            clear()
            print("**============== Welcome to Defi Auto transaction Bot ===============**")
            print("\n** You can set alerts for Up, Down or Both Targets **")
            print("** You'll be notified via system Beep when any of the targets HIT in real time **\n\n")
            print("Current Price for {}: {:.10f} $$".format(title, price))
            upORdown = input("\nPlease specify up, down or updown ud: ")
            clear()
            # message = bool(int(input("Do you want to send message 1/0: ")))
            message = False

            print("\n 1 -> YES \n 0 -> NO \n")
            trade = bool(int(input("Do you want to Trade (Sell and Buy when Target HIT for BNB) ? \nPress 1/0: ")))
            clear()
            print("\nCurrent Price for {}: {:.10f} $$".format(title, price))
            if upORdown == 'ud':
                Up = float(input("Please enter UP Target: "))
                Down = float(input("Please enter Down Target: "))
            else:
                target = float(input(f"Please Enter {upORdown} Target: "))

            dataEntered = True

        if Lasttrade_message is not None:
            print(f"\nLast Trade result: {Lasttrade_message}  \nTx : https://bscscan.com/tx/{tx}\n\n")
        print(f"Token name: {title}")
        print(f"Total avaliable {TokenSymbol}: {NoOfTokens}")
        print(f"Account BNB balance: {BNB_balance}")
        print("Current BNB Price: {:.10f} $$".format(price))
        if bool(config.SELL_TOKENS) and upORdown == 'up':
            print(f"Token to SELL: {config.SELL_TOKENS}")
        if bool(config.BUY_TOKENS) and upORdown == 'down':
            print(f"Token to Buy from BNB: {config.BUY_TOKENS} BNB")
        print(f"Current Token Price: {float(NoOfTokens) * float(price)} $$")
        if upORdown == 'ud':
            print("UP Target: {:.10f} $".format(Up))
            print("Down Target: {:.10f} $".format(Down))
        else:
            print("Target: {:.10f} $".format(target))

        if upORdown == 'up':
            if price > target:
                p1 = threading.Thread(target=notifyWithSound)
                if not trade: p1.start()

                if message:
                    p2 = threading.Thread(target=sendMessage, args=(numbersToNotify, "Price is Up", price))
                if trade:
                    p3 = ThreadWithResult(target=sellTokens, kwargs=params)
                    p1.start()
                    p3.start()
                    p3.join()
                    p1.join()

                    tx, Lasttrade_message = p3.result
                    if tx not in "Failed" and config.SHOW_TX_ON_BROWSER:
                        showTx(f"https://bscscan.com/tx/{tx}")
                        time.sleep(5)
                    updateData = True
                    print("UP Target HIT {:.10f}".format(target))

                    if bool(int(input("Do you want to update UP Target Price ? Press 1/0 : "))):
                        target = float(input("Please Enter New Up Target Price: "))
                    time.sleep(2)

        elif upORdown == 'down':
            if price < target:
                p1 = threading.Thread(target=notifyWithSound)
                if not trade: p1.start()

                if message:
                    p2 = threading.Thread(target=sendMessage, args=(numbersToNotify, "Price is Up", price))
                if trade:
                    p3 = ThreadWithResult(target=buyTokens, kwargs=params)
                    p1.start()
                    p3.start()
                    p3.join()
                    p1.join()

                    tx, Lasttrade_message = p3.result
                    if tx not in "Failed" and config.SHOW_TX_ON_BROWSER:
                        showTx(f"https://bscscan.com/tx/{tx}")
                        time.sleep(5)
                    updateData = True

                    print("DOWN Target HIT {:.10f}".format(target))
                    if bool(int(input("Do you want to update Down Target Price Press 1/0? : "))):
                        target = float(input("Please Enter New Up Target Price: "))
                    time.sleep(2)

        elif upORdown == 'ud':
            if price > Up:
                p1 = threading.Thread(target=notifyWithSound)
                if not trade: p1.start()

                if message:
                    p2 = threading.Thread(target=sendMessage, args=(numbersToNotify, "Price is Up", price))
                if trade:
                    p3 = ThreadWithResult(target=sellTokens, kwargs=params)
                    p1.start()
                    p3.start()
                    p3.join()
                    p1.join()

                    tx, Lasttrade_message = p3.result
                    if tx not in "Failed" and config.SHOW_TX_ON_BROWSER:
                        showTx(f"https://bscscan.com/tx/{tx}")
                        time.sleep(5)
                    updateData = True

                    print("UP Target HIT {:.10f}".format(Up))
                    if bool(int(input("Do you want to update UP Target Price ? Press 1/0 : "))):
                        Up = float(input("Please Enter New Up Target Price: "))
                    time.sleep(2)

            elif price < Down:
                p1 = threading.Thread(target=notifyWithSound)
                if not trade: p1.start()

                if message:
                    p2 = threading.Thread(target=sendMessage, args=(numbersToNotify, "Price is Up", price))
                if trade:
                    p3 = ThreadWithResult(target=buyTokens, kwargs=params)
                    p1.start()
                    p3.start()
                    p3.join()
                    p1.join()

                    tx, Lasttrade_message = p3.result
                    if tx not in "Failed" and config.SHOW_TX_ON_BROWSER:
                        showTx(f"https://bscscan.com/tx/{tx}")
                        time.sleep(5)
                    updateData = True

                    print("DOWN Target HIT {:.10f}".format(Down))
                    if bool(int(input("Do you want to update Down Target Price Press 1/0? : "))):
                        Down = float(input("Please Enter New Up Target Price: "))
                    time.sleep(2)
        else:
            clear()
            print("Invalid Input Please input only *up, *down or *ud")
            time.sleep(2)
            print("Restarting Program")
            time.sleep(1)
            print(".");
            time.sleep(1)
            print("..");
            time.sleep(1)
            print("...");
            time.sleep(1)
            runCode()
        time.sleep(1)
        clear()


if __name__ == "__main__":
    runCode()
