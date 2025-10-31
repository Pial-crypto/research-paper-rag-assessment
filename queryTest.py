import requests

url = "http://127.0.0.1:8000/api/query"
data = {
    "question": "What methodology was used in the transformer paper?",
    "top_k": 5,
    "paper_ids": [1, 3]
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
