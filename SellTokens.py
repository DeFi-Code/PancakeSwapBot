import time
import config


def sellTokens(**kwargs):
    symbol = kwargs.get('symbol')
    web3 = kwargs.get('web3')
    walletAddress = kwargs.get('walletAddress')
    contractPancake = kwargs.get('contractPancake')
    pancakeRouterAddress = kwargs.get('pancakeRouterAddress')
    TokenToSellAddress = kwargs.get('TokenToSellAddress')
    WBNB_Address = kwargs.get('WBNB_Address')
    contractSellToken = kwargs.get('contractSellToken')
    TradingTokenDecimal = kwargs.get('TradingTokenDecimal')

    tokensToSell = input(f"Enter amount of {symbol} you want to sell: ")
    tokenToSell = web3.toWei(tokensToSell, TradingTokenDecimal)

    # For tokens that need to be approved First
    # Get Token Balance
    TokenInAccount = contractSellToken.functions.balanceOf(walletAddress).call()
    symbol = contractSellToken.functions.symbol().call()
    
    approve = contractSellToken.functions.approve(pancakeRouterAddress, TokenInAccount).buildTransaction({
        'from': walletAddress,
        'gasPrice': web3.toWei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(walletAddress)
    })
    
    signed_txn = web3.eth.account.sign_transaction(
        approve, private_key=config.YOUR_PRIVATE_KEY)
    
    tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"Approved: {web3.toHex(tx_token)}")
    
    time.sleep(7)

    print(f"Swapping {web3.fromWei(tokenToSell, TradingTokenDecimal)} {symbol} for BNB")

    pancakeSwap_txn = contractPancake.functions.swapExactTokensForETH(
        tokenToSell, 0,
        [TokenToSellAddress, WBNB_Address],
        walletAddress,
        (int(time.time() + 1000000))
    ).buildTransaction({
        'from': walletAddress,
        'gasPrice': web3.toWei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(walletAddress)
    })

    signed_txn = web3.eth.account.sign_transaction(
        pancakeSwap_txn, private_key=config.YOUR_PRIVATE_KEY)

    try:
        tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        result = [web3.toHex(tx_token), f"Sold {web3.fromWei(tokenToSell, TradingTokenDecimal)} {symbol}"]
        return result
    except ValueError as e:
        if e.args[0].get('message') in 'intrinsic gas too low':
            result = ["Failed", f"ERROR: {e.args[0].get('message')}"]
        else:
            result = ["Failed", f"ERROR: {e.args[0].get('message')} : {e.args[0].get('code')}"]
        return result
