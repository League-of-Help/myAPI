from lxml import html
import json, requests, urllib

def get_patch():
  url_0 = 'https://na.leagueoflegends.com/en-us/news/tags/patch-notes'
  url_1 = 'https://ddragon.leagueoflegends.com/api/versions.json'

  # Get the data from url_0
  try:
    tree = html.fromstring(requests.get(url_0).content)
    url_0_result = tree.xpath('//*[@id="gatsby-focus-wrapper"]/div/div[2]/div/div[1]/div/ol/li[1]/a/article/div[2]/div/h2/text()')[0][6:-6]
  except: url_0_result = '0'

  # Get the data from url_1
  try: url_1_result = (json.loads(urllib.request.urlopen(url_1).read()))[0]
  except: url_1_result = '0'

  return max(url_0_result, url_1_result[0:5])
  
print(get_patch())
