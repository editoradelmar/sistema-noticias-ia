import requests

url = "http://localhost:8000/api/upload-file"
with open(r"D:\hromero\Desktop\Escritorio\Carta a Vanessa.pdf", "rb") as f:
    r = requests.post(url, files={"file": ("Carta a Vanessa.pdf", f, "application/pdf")})
print(r.status_code)
print(r.text)