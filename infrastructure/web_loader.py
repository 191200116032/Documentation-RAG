import requests

class WebDocumentLoader:
    def load(self, url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
