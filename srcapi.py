import srcomapi, srcomapi.datatypes as dt
import csv
api = srcomapi.SpeedrunCom(); api.debug = 1

def subcategory_parse(subcategory):
  if subcategory == '4lxppk3q':
    current_run["subcategory"] = '60Hz'
  elif subcategory == '0q5nnm7q':
    current_run["subcategory"] = '50Hz'
  else:
    current_run["subcategory"] = 'PS2 NTSC-U'

# Finding ICO
ico = api.search(srcomapi.datatypes.Game, {"name": "ico"})[0]
ico_runs = {}

# Getting all runs
for category in ico.categories:
  if not category.name in ico_runs:
    ico_runs[category.name] = {}
  if category.type == 'per-level':
    for level in ico.levels:
      ico_runs[category.name][level.name] = dt.Leaderboard(api, data=api.get("leaderboards/{}/level/{}/{}?embed=variables".format(ico.id, level.id, category.id)))
  else:
    ico_runs[category.name] = dt.Leaderboard(api, data=api.get("leaderboards/{}/category/{}?embed=variables".format(ico.id, category.id)))

game_dict = {}
# Parsing data
for category in ico_runs.keys():
    category_dict = {}
    if type(ico_runs[category]) is srcomapi.datatypes.Leaderboard:
        i = 1
        for run in ico_runs[category].runs:
            current_run = {}
            r = run["run"]

            if len(r.values.values()) > 0:
              subcategory_parse(list(r.values.values())[0])

            current_run["player"] = r.players
            current_run["times"] = r.times
            current_run["videos"] = r.videos
            current_run["date"] = r.date

            category_dict[i] = current_run
            i = i + 1
        game_dict[category] = category_dict

ico_csv = open("ico.csv", "w", encoding='utf-8')
writer = csv.writer(ico_csv)

for category_name, runs in game_dict.items():
  writer.writerow([category_name, runs])

ico_csv.close()
