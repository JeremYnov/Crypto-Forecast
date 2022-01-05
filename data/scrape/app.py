from bs4 import BeautifulSoup as bs
import requests
import datetime

scrape={
    'last_fetch': None,
    'coins': []
}

for div_a in bs(requests.get('https://coinmarketcap.com/historical/').content,'html.parser').find_all('a', {'class': 'historical-link cmc-link'}):
    scrape['last_fetch']=datetime.datetime.now()
    snapshot_date=div_a.split('/')[2]
    if len(snapshot_date) != 8: print('Historical snapshot parse failed. Stop !'); quit()
    snapshot_html=requests.get('https://coinmarketcap.com/historical/{}'.format(snapshot_date))
    if snapshot_html.status_code != 200: print('Request failed. Stop !'); quit()
    for row in bs(snapshot_html.content,'html.parser').find_all('tr', {'class': 'cmc-table-row'}):
        col=row.find_all('td', {'class': 'cmc-table__cell'})
        historyData={
            'date': snapshot_date,
            'rank': col[0].find('div').text,
            'market-cap': col[3].find('div').text[1:],
            'price(USD)': col[4].find('div').text[1:],
            'circulating-supply': col[5].find('div').text.split(' ')[0],
            'volume-24-h(USD)': col[6].find('a').text[1:],
            'change-hour(percent)': col[7].find('div').text[:-1],
            'change-day(percent)': col[8].find('div').text[:-1],
            'change-week(percent)': col[9].find('div').text[:-1]
        }
        for coin in scrape['coins']:
            if coin['name'] == col[1].find_all('a')[1].text:
                coin['history'].append(historyData)
                print("1")
                break
            print("0")

        scrape['coins'].append({ 
            'name': col[1].find_all('a')[1].text,
            'symbol': col[2].find('div').text,
            'history': [historyData]
        })

print(scrape)
