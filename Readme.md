<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/OlivierKuhn/PancakeSwapBot">
    <img src="images/Defi_PancakeBot.png" alt="Logo" width="230" height="160">
  </a>

  <h3 align="center">Defi PancakeSwap BOT</h3>
     <div align="center"><img src="https://img.shields.io/discord/921546042346979388?color=5865F2&label=Discord&logo=discord">

  <p align="center">
    Simple yet fast and efficient pancakeswap-bot running on the blockchain.
    <hr>
</div>



## Introduction

Pancakeswap Bot a fast and efficient bot written in Phyton to automatically buy and sell tokens on the blockchain as soon as liquidity is added and trade is enabled.

The bot is extremely fast as long as you use a good node and not a public one. With a node from Quicknode you can expect a buy/sell transaction in less than 5 seconds.


## Getting Started
### Requirements
<ul>
    <li>Windows 10 / Ubuntu / Mac OS</li>
	<li>Latest <a href="https://nodejs.org/en/download/">NodeJS</a> installed.</li>
	<li>A <b>decent</b> internet connection.</li>
	<li>
		A <b>decent</b> BSC node, preferably paid, but you may also use free ones.
		</ul>
	</li>
</ul>

### Installation
1. Download and install Bot from <a href="https://nodejs.org/en/download/">here</a>.
2. Download and install NodeJS from <a href="https://nodejs.org/en/download/">here</a>.
3. That's it! Time for configuration. 🎉


### Configuration

```ini
[WALLET]
; This is your BSC wallet's private key.
SECRET_KEY=private_wallet_key

; The uptime of this node is pretty bad, you should consider using a private node.
WSS_NODE=wss://bsc-ws-node.nariox.org:443


[CONTRACTS]
; These variables support some pre-defined contracts (BNB, ETH, BUSD). 
; For other contracts you'll have to specify the contract address yourself.
INPUT=BNB
OUTPUT=BUSD


[TRANSACTION]

GAS_LIMIT=500000
GAS_PRICE=5

; This variable is the amount of crypto you wish to use with the input contract.
; If for example you use WBNB as input, you will have to use WBNB's format.
AMOUNT_IN=0.0033

BUY_SLIPPAGE=10
```


### Features
* Buy and sell using ANY pair.
* Multi blockchain support.
* Wrapped mode for any ETH-like token.
* Pinksale / dxsale support.
* Mempool sniping mode.
* Honeypot checking.
* Advanced token caching.
* Measures against anti-bots:
     * Tax checker
     * Multi-buy mode
     * Block-offset system
* Autosell modes:
     * Sell using a delay
     * Sell on multiplier hit
     * Sell using the space key
     * Stop loss / trailing auto-sell.
Auto updates (updates are done automatically without the need of a re-download)


### Supported chains
- Binance Smart Chain
- Arbitrum
- Avalanche
- Ethereum
- Polygon
- Cronos
- Milkomeda
- Metis
- Fantom
- Dogechain

If you wish to change the blockchain the bot will operate on, just change the WSS_NODE endpoint in config.ini to the right endpoint.

#### Public WSS Nodes
- Binance Smart Chain: wss://bsc-ws-node.nariox.org:443
- Ethereum: wss://main-light.eth.linkpool.io/ws
- Polygon: wss://rpc-mainnet.matic.network

_Note: The nodes listed above are free nodes and are NOT always online._

### Supported tokens
The bot currently supports any token using the uniswap interface.



### Usage
To launch the bot use the command ```node index.js```

#### Premium parameters

##### General
<table>
  <tr>
    <th>Parameter</th>
    <th>Description</th>
    <th>Accepts</th>
  </tr>
  <tr>
    <td>--buy-only</td>
    <td>Enables manual buy mode. This will only buy the token and then exit.</td>
    <td>-</td>
  </tr>
  <tr>
    <td>--sell-only</td>
    <td>Enables manual sell mode. This will only sell the token and then exit.</td>
    <td>-</td>
  </tr>
  <tr>
    <td>--input</td>
    <td>Overwrites the input parameter in the config.</td>
    <td><code>contract address</code></td>
  </tr>
  <tr>
    <td>--output</td>
    <td>Overwrites the output parameter in the config.</td>
    <td><code>contract address</code></td>
  </tr>
  <tr>
    <td>--config</td>
    <td>Used to specify a different config path (used for multi configs setup).</td>
    <td><code>string</code></td>
  </tr>
  <tr>
    <td>--force-approve</td>
    <td>Forces the approve transaction for the input/output. (used for debugging)</td>
    <td>-</td>
  </tr>
  <tr>
    <td>--simulate</td>
    <td>Simulate your current config as a real transaction.</td>
    <td>-</td>
  </tr>
</table>

##### Transaction

<table>
  <tr>
    <th>Parameter</th>
    <th>Description</th>
    <th>Accepts</th>
  </tr>
  <tr>
    <td>--wrapped</td>
    <td>Uses the wrapped version of the bnb/eth token. (available for all blockchains)</td>
    <td>-</td>
  </tr>
  <tr>
    <td>--block-offset</td>
    <td>Waits an amount of blocks before sending out the buy transaction.</td>
    <td><code>number</code></td>
  </tr>
  <tr>
    <td>--spam</td>
    <td>Sends an x amount of transactions at the same time. (spam buy)</td>
    <td><code>number</code></td>
  </tr>
  <tr>
    <td>--amount_in</td>
    <td>Used to specify the amount you wish to spend with your INPUT token.</td>
    <td><code>number</code></td>
  </tr>
  <tr>
    <td>--amount_out</td>
    <td>Used to specify the amount you wish to buy from your OUTPUT token.</td>
    <td><code>number</code></td>
  </tr>
  <tr>
    <td>--min_liq</td>
    <td>Used to specify the minimum liquidity before the bot starts to buy.</td>
    <td><code>number</code></td>
  </tr>
</table>

##### Tax

<table>
  <tr>
    <th>Parameter</th>
    <th>Description</th>
    <th>Accepts</th>
  </tr>
  <tr>
    <td>--verify-tax</td>
    <td>Checks wether the taxes for buying / selling does not exceed the limits configured.</td>
    <td>-</td>
  </tr>
  <tr>
    <td>--max-buy-tax</td>
    <td>Sets the max allowed buy tax.</td>
    <td><code>number</code></td>
  </tr>
  <tr>
    <td>--max-sell-tax</td>
    <td>Sets the max allowed sell tax.</td>
    <td><code>number</code></td>
  </tr>
</table>

##### Gas

<table>
  <tr>
    <th>Parameter</th>
    <th>Description</th>
    <th>Accepts</th>
  </tr>
  <tr>
    <td>--gas-price</td>
    <td>Sets the gas price.</td>
    <td><code>number</code></td>
  </tr>
  <tr>
    <td>--gas-limit</td>
    <td>Sets the gas limit.</td>
    <td><code>number</code></td>
  </tr>
</table>

##### Slippage

<table>
  <tr>
    <th>Parameter</th>
    <th>Description</th>
    <th>Accepts</th>
  </tr>
  <tr>
    <td>--buy-slippage</td>
    <td>Sets the buy slippage.</td>
    <td><code>number</code></td>
  </tr>
  <tr>
    <td>--sell-slippage</td>
    <td>Sets the sell slippage.</td>
    <td><code>number</code></td>
  </tr>
</table>

##### Autosell

<table>
  <tr>
    <th>Parameter</th>
    <th>Description</th>
    <th>Accepts</th>
  </tr>
  <tr>
    <td>--sell-with-multiplier</td>
    <td>Enables the sell with multiplier autosell mode.</td>
    <td>-</td>
  </tr>
  <tr>
    <td>--sell-multiplier</td>
    <td>Sets the multiplier to sell at for the sell with multiplier mode.</td>
    <td><code>number</code></td>
  </tr>
  <tr><td></td><td></td><td></td></tr>
  <tr>
    <td>--sell-with-delay</td>
    <td>Enables the sell with delay autosell mode.</td>
    <td>-</td>
  </tr>
  <tr>
    <td>--sell-delay</td>
    <td>Sets the delay to sell with for the sell with delay mode.</td>
    <td><code>number</code></td>
  </tr>
  <tr><td></td><td></td><td></td></tr>
  <tr>
    <td>--sell-on-loss</td>
    <td>Enables the sell on loss autosell mode.</td>
    <td>-</td>
  </tr>
  <tr>
    <td>--sl-minimum-multiplier</td>
    <td>Sets the minimum multiplier for the sell on loss mode to start.</td>
    <td><code>number</code></td>
  </tr>
  <tr>
    <td>--sl-percentage</td>
    <td>Sets the percentage of the maximum impact on your multiplier.</td>
    <td><code>number</code></td>
  </tr>
</table>

</ul>
