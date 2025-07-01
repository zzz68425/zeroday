import requests

API_KEY = "jina_52651cb7f287474db4b5d806f80e4c5aDL6vec4YpEmbZQPrQn_39FcaBB5i"
url = f"https://embeddings-dashboard-api.jina.ai/api/v1/api_key/fe_user?api_key={API_KEY}"

res = requests.get(url)
data = res.json()

#token餘額
balance = data.get("wallet", {}).get("total_balance", None)