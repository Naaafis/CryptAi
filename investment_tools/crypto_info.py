import requests

def get_crypto_data(crypto_symbol):
    url = f"https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": crypto_symbol,
        "order": "market_cap_desc",
        "per_page": 1,
        "page": 1,
        "sparkline": False
    }
    response = requests.get(url, params=params)
    
    print(response.json())
    
    data = response.json()[0]
    
    return {
        "name": data["name"],
        "price": data["current_price"],
        "market_cap": data["market_cap"],
        "price_change_24h": data["price_change_percentage_24h"],
        "volume_24h": data["total_volume"]
    }

# Example usage
crypto = get_crypto_data("bitcoin")
print(crypto)
