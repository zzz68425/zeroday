#用來查餘額
import requests
from lib.config import API_KEY

url = f"https://embeddings-dashboard-api.jina.ai/api/v1/api_key/fe_user?api_key={API_KEY}"

res = requests.get(url)
data = res.json()

#token餘額
balance = data.get("wallet", {}).get("total_balance", None)