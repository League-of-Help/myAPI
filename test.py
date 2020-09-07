import requests
data = requests.get('http://ddragon.leagueoflegends.com/cdn/10.16.1/data/en_US/champion.json').json()
print(data['data']['Shaco']['tags'])
