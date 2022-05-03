import time
import requests 
import pandas as pd
from datetime import datetime, date


class Cryptopanic:
    def __init__( self, filters = "btc", language="en" ):
        self.filter = filters
        self.language = language
        
    def getData(self):
        token="a739f16e5d4f1f7ff25794400a689c26f99df0fe"
        page = requests.get(f"https://cryptopanic.com/api/v1/posts/?auth_token={token}&currencies={self.filter}&regions={self.language}")
        crypto_news = []
        today = date.today().strftime("%Y-%m-%d")
        while True: 
            data = page.json()
            news = data["results"]
            if data["next"]:
                time.sleep(2)
                page = requests.get(data["next"])
                for element in news: 
                    date_time = datetime.strptime(element["published_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
                    crypto_news.append({"Text": element["title"], "Created_at": date_time})
                    if date_time != today:
                        break
                df = pd.DataFrame(crypto_news)
                if date_time != today:
                    break
            else:
                break
        return df

Cryptopanic().getData()