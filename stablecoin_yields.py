import requests
import json
import sqlite3  # Change the import here
import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime
from telegram import Bot

url = 'https://yields.llama.fi/pools'

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data={})
data = json.loads(response.text)

# Replace with the path of your .env file
load_dotenv('.env')

# Initialize the Telegram Bot
bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("chat_id")

bot = Bot(token=bot_token)

async def main():
    # Change the database connection to work with SQLite
    cnx = sqlite3.connect('crypto.db')
    cursor = cnx.cursor()

    # Retrieve existing pool IDs from the database
    existing_pool_ids_query = "SELECT DISTINCT pool FROM stables"  # Change table name to 'stables'
    cursor.execute(existing_pool_ids_query)
    existing_pool_ids = set(row[0] for row in cursor.fetchall())

    # Filter and process data as before
    filtered_data = [item for item in data["data"] if item["stablecoin"] and item["tvlUsd"] > 400000 and item["apy"] > 10]

    filtered_output = {
        "status": data["status"],
        "data": [
            {
                "chain": item["chain"],
                "project": item["project"],
                "symbol": item["symbol"],
                "tvlUsd": item["tvlUsd"],
                "apyBase": item["apyBase"],
                "apyReward": item["apyReward"],
                "apy": item["apy"],
                "rewardTokens": item["rewardTokens"],
                "pool": item["pool"],
                "apyPct1D": item["apyPct1D"],
                "apyPct7D": item["apyPct7D"],
                "apyPct30D": item["apyPct30D"],
                "underlyingTokens": item["underlyingTokens"],
                "apyMean30d": item["apyMean30d"]
            }
            for item in filtered_data
        ]
    }

    # Track new pool IDs
    new_pool_ids = []

    # Check for new pools and insert new data
    for item in filtered_output["data"]:
        if item["pool"] not in existing_pool_ids:
            new_pool_ids.append(item["pool"])  # Add the new pool ID to the list
            insert_query = """
            INSERT INTO stables (date, chain, project, symbol, tvlUsd, apyBase, apyReward, apy, rewardTokens, pool, apyPct1D, apyPct7D, apyPct30D, underlyingTokens, apyMean30d)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(insert_query, (
                datetime.now(),
                item["chain"],
                item["project"],
                item["symbol"],
                item["tvlUsd"],
                item["apyBase"],
                item["apyReward"],
                item["apy"],
                ', '.join(item["rewardTokens"]) if item["rewardTokens"] else None,
                item["pool"],
                item["apyPct1D"],
                item["apyPct7D"],
                item["apyPct30D"],
                ', '.join(item["underlyingTokens"]) if item["underlyingTokens"] else None,
                item["apyMean30d"]
            ))

    # Commit the transaction and close the connection
    cnx.commit()
    cursor.close()
    cnx.close()

    # Get today's date in the desired format
    today_date = datetime.now().strftime("%B %d, %Y")

    # Provide feedback about new pools
    if new_pool_ids:
        new_pools_messages = []
        for item in filtered_output["data"]:
            if item["pool"] in new_pool_ids:
                pool_message = "\n".join(
                    [
                        f'pool : {item["pool"]}',
                        f'chain : {item["chain"]},',
                        f'project : {item["project"]},',
                        f'symbol : {item["symbol"]},',
                        f'tvlUsd : {item["tvlUsd"]:,.2f},',
                        f'apy : {item["apy"]:.2f},'
                    ]
                )
                new_pools_messages.append(pool_message)
                new_pools_messages.append("")  # Add an empty line after each pool
        
        new_pools_message = "\n".join(new_pools_messages)
        
        message = (
            f"{today_date}\n\n"
            f"New Stablecoin pools were found:\n{new_pools_message}"
        )
        await bot.send_message(chat_id=chat_id, text=message)
    else:
        await bot.send_message(chat_id=chat_id, text=f"{today_date}\n\nNo new Stablecoin pools were found.")


if __name__ == "__main__":
    asyncio.run(main())  # Run the asynchronous main function
