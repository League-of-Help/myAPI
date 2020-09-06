from lxml import html
from time import time
import os, requests, game_data

# Create the champion folder if it doesn't exist.
parent_dir = os.path.dirname(os.path.abspath(__file__)) # Get current folder
directory = 'champion'                                  # Define the name of the folder where the champions' files will be saved
path = os.path.join(parent_dir, directory)              # Define the path where the champions' files will be saved
try: os.mkdir(path)                                     # Try to create the file if it does not exist
except: print(f'Creating {path} file failed.')

# Check the internet connection
internet_access = False                                 # Set internet access to False by default
try:
  requests.head('http://216.58.192.142', timeout=2)     # Try logging on to "Google.com"
  internet_access = True                                # If logged successfuly set internet access to True
except:
  input('Please check your internet connection or try again later...')


class load_LoL_data():
  def __init__(self):
    self.urls = {
      'league of legends': {
        'champions': 'https://na.leagueoflegends.com/champions'
      },
      'league of legends fandom': {
        'free rotation': 'https://leagueoflegends.fandom.com/wiki/Free_champion_rotation'
      },
      'opgg': {
        'champions': 'https://na.op.gg/champion'
      }
    }
  
  def load_url(self, url):
    return html.fromstring(requests.get(url).content)

  def get_champion_rotation(self):
    tree = self.load_url(f'{self.urls["league of legends fandom"]["free rotation"]}')
    return [tree.xpath(f'//*[@id="mw-content-text"]/div[1]/div[1]/ol/li[{i}]/div/div[2]/a/text()')[0] for i in range (1, 16)]

  def get_champion_meta_tier(self, champion):
    champion = champion.replace('-', '').lower()
    tree = self.load_url(f'{self.urls["opgg"]["champions"]}/{champion}/statistics')
    try: return tree.xpath('//*[@class="champion-stats-header-info__tier"]/b/text()')[0][-1]
    except: print(f"Unable to load champion meta tier.")

  def get_champion_ability(self, champion):
    tree = self.load_url(f'{self.urls["league of legends"]["champions"]}/{champion}/')
    xpaths = []

    try:
      for i in range(1, 6):
        xpaths.append(
          tree.xpath(f'//*[@id="gatsby-focus-wrapper"]/div/section[2]/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/ol/li[{i}]/h5/text()')[0].replace("\n", " "),
        )
        xpaths.append(
          tree.xpath(f'//*[@id="gatsby-focus-wrapper"]/div/section[2]/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/ol/li[{i}]/p/text()')[0].replace("\n", " ")
        )
      return xpaths
    except:
      try: return game_data.RECENT_ABILITIES[champion[0].upper() + champion[1:]]
      except: print(f"Unable to load champion abilities.")
    

if __name__ == '__main__' and internet_access:          # Run the programm if this specific file is executed
  time0 = time()                                        # Set the time to 0 for the remaining time estimation
  data = load_LoL_data()                                # Initializing an instance of the class load_LoL_data
  free_rotation = data.get_champion_rotation()          # Create the list of free champions in weekly rotation
  total_champions = len(game_data.CHAMPIONS)
  for index, champion in enumerate(game_data.CHAMPIONS):# Generate a file for each champion
    # Print the champion currently being generated
    if index > 0:
      print(f"Generating {champion}'s file ([{index + 1}/{total_champions}] | {round((time() - time0) * (total_champions - index))} seconds left)...")    
    else:
      print(f"Generating {champion}'s file ([{index + 1}/{total_champions}] | {round((time() - time0) * (total_champions * 4))} estimated remaining seconds).")    
    time0 = time()

    if champion in game_data.LoL_NAMES: name = game_data.LoL_NAMES[champion]
    else: name = champion
    champion_abilities = data.get_champion_ability(name.lower())

    if champion in free_rotation: free = 'true'
    else: free = 'false'

    try:
      word = f'''{{
  "display_name": "{champion}",
  "name": "{name}",
  "meta_tier": {data.get_champion_meta_tier(champion)},
  "free": {free},
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
