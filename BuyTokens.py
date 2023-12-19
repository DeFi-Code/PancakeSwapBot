import config
import time


def buyTokens(**kwargs):
    symbol = kwargs.get('symbol')
    web3 = kwargs.get('web3')
    walletAddress = kwargs.get('walletAddress')
    contractPancake = kwargs.get('contractPancake')
    TokenToBuyAddress = kwargs.get('TokenToSellAddress')
    WBNB_Address = kwargs.get('WBNB_Address')

    toBuyBNBAmount = input(f"Enter amount of BNB you want to buy {symbol}: ")
    toBuyBNBAmount = web3.toWei(toBuyBNBAmount, 'ether')

    pancakeSwap_txn = contractPancake.functions.swapExactETHForTokens(0,
                                                                      [WBNB_Address, TokenToBuyAddress],
                                                                      walletAddress,
                                                                      (int(time.time() + 10000))).buildTransaction({
        'from': walletAddress,
        'value': toBuyBNBAmount,  # Amount of BNB
        'gas': 160000,
        'gasPrice': web3.toWei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(walletAddress)
    })

    signed_txn = web3.eth.account.sign_transaction(pancakeSwap_txn, private_key=config.YOUR_PRIVATE_KEY)
    try:
        tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        result = [web3.toHex(tx_token), f"Bought {web3.fromWei(toBuyBNBAmount, 'ether')} BNB of {symbol}"]
        return result
    except ValueError as e:
        if e.args[0].get('message') in 'intrinsic gas too low':
            result = ["Failed", f"ERROR: {e.args[0].get('message')}"]
        else:
            result = ["Failed", f"ERROR: {e.args[0].get('message')} : {e.args[0].get('code')}"]
        return result
