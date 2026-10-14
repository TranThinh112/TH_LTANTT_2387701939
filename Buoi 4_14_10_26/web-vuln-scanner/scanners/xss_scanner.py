import requests
from urllib.parse import urlsplit

class XSSScanner:
    def __init__(self):
        self.payloads = [
            "<script>alert(1)</script>",
            '"><svg/onload=alert(1)>'
        ]

    def scan(self, url):
        results = []
        separator = "&" if urlsplit(url).query else "?"

        for payload in self.payloads:
            test_url = f"{url}{separator}q={payload}"
            try:
                response = requests.get(test_url, timeout=5)
                if payload in response.text:
                    results.append({
                        "type": "XSS",
                        "payload": payload,
                        "url": test_url,
                        "risk": "HIGH"
                    })
            except requests.RequestException:
                pass
        return results
