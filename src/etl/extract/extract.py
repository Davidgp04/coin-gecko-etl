from dotenv import load_dotenv
import os
import requests
import json
from datetime import datetime
load_dotenv()

def get_price_data(currencies: list, crypto_currencies: list):
    crypto_currencies_str=",".join(crypto_currencies)
    currencies_str=",".join(currencies)
    params = {
        "vs_currencies": currencies_str,
        "ids": crypto_currencies_str, # "ids": "bitcoin,ethereum,cardano",
        # "names": "Bitcoin",
        # "ids": "bitcoin", # "ids": "bitcoin",
        # "names": "Bitcoin,Ethereum,Cardano",
        # "symbols": "btc",
        "include_last_updated_at": "true",
        "precision": "5"
    }

    url = "https://api.coingecko.com/api/v3/simple/price"

    headers = {"x-cg-api-key": os.getenv("COIN_GECKO_API_KEY")}

    response = requests.get(url, headers=headers, params=params)
    response_dict=response.json()
    print(json.dumps(response_dict, indent=4))


    return response_dict

if __name__ == "__main__":
    response_dict = get_price_data(currencies=["usd", "cop"], crypto_currencies=["bitcoin", "ethereum", "cardano"])
    for key, value in response_dict.items():
        print(f"{key}: {value} at {datetime.fromtimestamp(value['last_updated_at'])} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")