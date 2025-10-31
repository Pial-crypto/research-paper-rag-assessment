import requests


API_URL = "http://127.0.0.1:8000/api/papers"


paper_id = "6904973362117ae85b12aea6"  


response = requests.delete(f"{API_URL}/{paper_id}")

print("Status code:", response.status_code)


try:
    print("Response JSON:", response.json())
except Exception:
    print("Raw Response:", response.text)
