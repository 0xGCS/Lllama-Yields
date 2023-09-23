from datetime import datetime
import requests
import json

# Fetch vault data
url = 'https://api.beefy.finance/vaults'
response = requests.get(url)
vault_data = response.json()

# Fetch APY data
url = 'https://api.beefy.finance/apy'
response = requests.get(url)
apy_data = response.json()

allowed_chains = ["ethereum", "polygon", "base", "optimism", "arbitrum", "avax", "zksync", "zkevm", "bsc"]

filtered_data = []
for item in vault_data:
    if item["status"] == "active" and item["chain"] in allowed_chains:
        if "IL_NONE" in item.get("risks", []) and "CONTRACTS_VERIFIED" in item.get("risks", []):
            refined_item = {key: item[key] for key in ["id", "name", "token", "tokenAddress", "platformId", "assets", "risks", "strategyTypeId", "createdAt", "chain"] if key in item}
            
            # Convert Unix timestamp to "YYYY-MM-DD HH:MM:SS"
            refined_item["createdAt"] = datetime.fromtimestamp(refined_item["createdAt"]).strftime('%Y-%m-%d %H:%M:%S')

            # Attach APY value if exists
            if refined_item["id"] in apy_data:
                refined_item["apy"] = apy_data[refined_item["id"]]
            
            filtered_data.append(refined_item)

# Save to JSON file
with open("beefy.json", "w") as file:
    json.dump(filtered_data, file, indent=4)

print("Filtered data saved to beefy.json")