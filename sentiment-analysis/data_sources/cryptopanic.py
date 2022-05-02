import pandas as pd
import requests 
import time
from datetime import datetime, date

URL = 'https://cryptopanic.com/api/v1/posts/?auth_token=a739f16e5d4f1f7ff25794400a689c26f99df0fe'

class Cryptopanic:
    def __init__(
        self,
        filters = 'btc',
        language="en",
    ):
        self.filter = filters
        self.language = language
        
    def getData(self):
        page = requests.get(f'{URL}&currencies={self.filter}&regions={self.language}')
        infinite = True
        crypto_news = []
        today = date.today()
        while infinite: 
            data = page.json()
            news = data["results"]
            if data['next']:
                time.sleep(2)
                page = requests.get(data['next'])
                for element in news: 
                    date_time = datetime.strptime(element['published_at'], "%Y-%m-%dT%H:%M:%SZ")
                    crypto_news.append({"Text": element['title'], "Created_at": date_time.strftime('%Y-%m-%d')})
                    
                    if date_time.strftime('%Y-%m-%d') != today.strftime("%Y-%m-%d"):
                        break
                df = pd.DataFrame(crypto_news)
                if date_time.strftime('%Y-%m-%d') != today.strftime("%Y-%m-%d"):
                        break
            else :
                break
        print(df)
        return df
            
        
        
cryptopanic = Cryptopanic()

cryptopanic.getData()