from lxml import html
import os, requests, game_data

# Create the champion folder if it doesn't exist.
parent_dir = os.path.dirname(os.path.abspath(__file__))
print(parent_dir)
directory = 'champion'
path = os.path.join(parent_dir, directory)
try: os.mkdir(path)
except: print(f'Creating {path} file failed.')

def get_champ_ability(champion):
  url = f'https://na.leagueoflegends.com/en-us/champions/{champion}/'
  tree = html.fromstring(requests.get(url).content)

  try:
    return (
      tree.xpath('//*[@id="gatsby-focus-wrapper"]/div/section[2]/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/ol/li[1]/h5/text()')[0].replace("\n", " "),
      tree.xpath('//*[@id="gatsby-focus-wrapper"]/div/section[2]/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/ol/li[1]/p/text()')[0].replace("\n", " "),
      tree.xpath('//*[@id="gatsby-focus-wrapper"]/div/section[2]/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/ol/li[2]/h5/text()')[0].replace("\n", " "),
      tree.xpath('//*[@id="gatsby-focus-wrapper"]/div/section[2]/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/ol/li[2]/p/text()')[0].replace("\n", " "),
      tree.xpath('//*[@id="gatsby-focus-wrapper"]/div/section[2]/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/ol/li[3]/h5/text()')[0].replace("\n", " "),
      tree.xpath('//*[@id="gatsby-focus-wrapper"]/div/section[2]/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/ol/li[3]/p/text()')[0].replace("\n", " "),
      tree.xpath('//*[@id="gatsby-focus-wrapper"]/div/section[2]/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/ol/li[4]/h5/text()')[0].replace("\n", " "),
      tree.xpath('//*[@id="gatsby-focus-wrapper"]/div/section[2]/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/ol/li[4]/p/text()')[0].replace("\n", " "),
      tree.xpath('//*[@id="gatsby-focus-wrapper"]/div/section[2]/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/ol/li[5]/h5/text()')[0].replace("\n", " "),
      tree.xpath('//*[@id="gatsby-focus-wrapper"]/div/section[2]/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/ol/li[5]/p/text()')[0].replace("\n", " ")
    )
  except:
    try: return game_data.RECENT_ABILITIES[champion[0].upper() + champion[1:]]
    except: print(f"Unable to load {champion}'s abilities.")

if __name__ == '__main__':
  for champion in game_data.CHAMPIONS:
    print(f"Generating {champion}'s file.")

    if champion in game_data.LoL_NAMES: name = game_data.LoL_NAMES[champion]
    else: name = champion
    champion_abilities = get_champ_ability(name.lower())

    try:
      word = f'''{{
  "display_name": "{champion}",
  "name": "{name}",
  "abilities": {{
    "p": [
      "{champion_abilities[0]}",
      "{champion_abilities[1]}"
    ],
    "q": [
      "{champion_abilities[2]}",
      "{champion_abilities[3]}"
    ],
    "w": [
      "{champion_abilities[4]}",
      "{champion_abilities[5]}"
    ],
    "e": [
      "{champion_abilities[6]}",
      "{champion_abilities[7]}"
    ],
    "r": [
      "{champion_abilities[8]}",
      "{champion_abilities[9]}"
    ]
  }}\n}}'''
    except: word = '"No data"'

    with open(f'{path}/{name}.json', 'w+') as f:
      f.write(word)
      f.close()

  input('JSON files generated successfuly, press enter to close this dialog...')
