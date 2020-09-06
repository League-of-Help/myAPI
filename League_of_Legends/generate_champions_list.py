from game_data import CHAMPIONS

CHAMPIONS = sorted(CHAMPIONS)
x = len(CHAMPIONS)
word = '[\n'
for i in range(x):
  word += f'\t"{CHAMPIONS[i]}"'
  if i + 1 != x: word += ','
  word += '\n'
word += ']'

with open('champions_list.json', 'w') as f:
  f.write(word)
  f.close()
