import requests
import json

# -----------------------------
# Example Query
# -----------------------------
url = "http://127.0.0.1:8000/api/query"  # তোমার FastAPI চালু থাকা URL
payload = {
   "question": "What methodology was used in the transformer paper?",
  "top_k": 5,
   
}

headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        result = response.json()
        print("✅ Query result:")
        print(json.dumps(result, indent=2))
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
except Exception as e:
    print(f"❌ Exception occurred: {str(e)}")
