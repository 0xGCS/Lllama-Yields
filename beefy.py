import requests
import json

# Fetch data from the vaults endpoint
vaults_url = 'https://api.beefy.finance/vaults'
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

response = requests.get(vaults_url, headers=headers)
data = json.loads(response.text)

# Fetch data from the APY endpoint
apy_url = 'https://api.beefy.finance/apy'
response = requests.get(apy_url, headers=headers)
apy_data = json.loads(response.text)

allowed_chains = ["ethereum", "polygon", "base", "optimism", "arbitrum", "avax", "zksync", "zkevm", "bsc"]

# Filter the original data
filtered_data = [
    item for item in data
    if item["status"] == "active" and
    item["chain"] in allowed_chains and
    "IL_NONE" in item["risks"] and
    "CONTRACTS_VERIFIED" in item["risks"]
]

# Create a list to store the refined dictionaries
refined_data = []

# Include only selected keys and add APY value to each item
for item in filtered_data:
    refined_item = {key: item.get(key) for key in ["id", "name", "token", "tokenAddress", "tokenProviderId", "platformId", "assets", "risks", "strategyTypeId", "createdAt", "chain"]}

    # Add the APY value if available
    item_id = item.get("id", "")
    apy_value = apy_data.get(item_id)
    if apy_value is not None:
        refined_item["apy"] = apy_value
    
    refined_data.append(refined_item)

# Save the refined data to a JSON file
with open("beefy.json", "w") as file:
    json.dump(refined_data, file, indent=4)

print("Filtered and refined data saved to beefy.json")
