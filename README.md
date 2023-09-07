# Description
Telegram bot that tracks the yields from the DeFi Llama API and post any new pools found into Telegram.

# Requirements
This bot fetches data from the DeFiLlama API and stores it in a MYSQL database. The database used here has the following schema:

date datetime
chain varchar(255)
project varchar(255)
symbol varchar(255)
tvlUsd decimal(20,8)
apyBase decimal(20,8)
apyReward decimal(20,8)
apy decimal(20,8)
rewardTokens varchar(700)
pool varchar(255)
apyPct1D decimal(20,8)
apyPct7D decimal(20,8)
apyPct30D decimal(20,8)
underlyingTokens varchar(700)
apyMean30d decimal(20,8)

You also need to obtain a Telegram bot token.


# Screenshots
<img width="412" alt="image" src="https://github.com/gcs1915/Lllama-Yields/assets/104216578/b82b7acb-cb15-49b2-a8a6-d34e771ccc7f">
<img width="412" alt="image" src="https://github.com/gcs1915/Lllama-Yields/assets/104216578/151ffa07-6313-464f-a02e-41557047ca54">

