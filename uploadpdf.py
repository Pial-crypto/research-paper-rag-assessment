import requests

# FastAPI server URL
url = "http://127.0.0.1:8000/api/papers/upload"

# অবশ্যই ফাইলের সম্পূর্ণ path দিতে হবে, folder নয়
file_path = "D:/Study/Upscale/research-paper-rag-assessment/sample_papers/paper_5.pdf"

# open the PDF file properly
with open(file_path, "rb") as f:
    files = {"file": ("paper_5.pdf", f, "application/pdf")}
    response = requests.post(url, files=files)

# response দেখাও
print("Status code:", response.status_code)

# JSON decode error এড়াতে
try:
    print("Response:", response.json())
except Exception as e:
    print("Response is not JSON:", response.text)
