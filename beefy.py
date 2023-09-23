from datetime import datetime
import requests
import json
import mysql.connector
import os
from dotenv import load_dotenv


# Fetch vault data
url = 'https://api.beefy.finance/vaults'
response = requests.get(url)
vault_data = response.json()

# Fetch APY data
url = 'https://api.beefy.finance/apy'
response = requests.get(url)
apy_data = response.json()

#replace with path of your .env file
load_dotenv(<'file_path'>)

allowed_chains = ["ethereum", "polygon", "base", "optimism", "arbitrum", "avax", "zksync", "zkevm", "bsc"]

filtered_data = []
for item in vault_data:
    if item["status"] == "active" and item["chain"] in allowed_chains:
        if "IL_NONE" in item.get("risks", []) and "CONTRACTS_VERIFIED" in item.get("risks", []):
            refined_item = {key: item[key] for key in ["id", "name", "token", "tokenAddress", "tokenProviderId","platformId", "assets", "risks", "strategyTypeId", "createdAt", "chain"] if key in item}
            
            # Convert Unix timestamp to "YYYY-MM-DD HH:MM:SS"
            refined_item["createdAt"] = datetime.fromtimestamp(refined_item["createdAt"]).strftime('%Y-%m-%d %H:%M:%S')

            # Attach APY value if exists
            if refined_item["id"] in apy_data:
                refined_item["apy"] = apy_data[refined_item["id"]]
            
            filtered_data.append(refined_item)

# Connect to DB - replace with actual details
cnx = mysql.connector.connect(
    host=os.getenv('host'),
    user=os.getenv('user'),
    passwd=os.getenv('passwd'),
    database=os.getenv('database')
)
cursor = cnx.cursor()

# SQL query string
insert_query = """
INSERT INTO beefy (date, id, name, token, tokenAddress, tokenProviderId, platformId, assets, risks, strategyTypeId, createdAt, chain, apy)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for refined_item in filtered_data:
    cursor.execute(insert_query, (
        datetime.now(),
        refined_item["id"],
        refined_item["name"],
        refined_item["token"],
        refined_item.get("tokenAddress", None),
        refined_item.get("tokenProviderId", None),  # Use get to handle cases where the key might not be present
        refined_item["platformId"],
        ','.join(refined_item['assets']),
        ','.join(refined_item['risks']),
        refined_item['strategyTypeId'],
        refined_item['createdAt'],  # Use the refined createdAt that has been converted to datetime
        refined_item['chain'],
        refined_item.get('apy', None)
    ))

# Commit the transaction and close the connection
cnx.commit()
cursor.close()
cnx.close()

print("Filtered data saved to database")