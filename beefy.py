import requests
import json

url = 'https://api.beefy.finance/vaults'

headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json' 
}

response = requests.request("GET", url, headers=headers, data={})
data = json.loads(response.text)

allowed_chains = ["ethereum", "polygon", "base", "optimism", "arbitrum", "avax", "zksync", "zkevm", "bsc"]

filtered_data = [
  item for item in data
  if item["status"] == "active" and 
     item["chain"] in allowed_chains and
     "IL_NONE" in item["risks"] and
     "CONTRACTS_VERIFIED" in item["risks"]
]

with open("beefy.json", "w") as file:
  json.dump(filtered_data, file, indent=4)

print("Filtered data saved to beefy.json")
