import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/83.0.4103.97 Safari/537.36",
}

content = requests.post("https://www.hackthebox.eu/api/invite/generate",headers=headers).content
print(content.decode('ansi'))