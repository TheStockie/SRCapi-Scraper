import srcomapi, srcomapi.datatypes as dt
import csv
api = srcomapi.SpeedrunCom(); api.debug = 1
subcategory_dict = {}

# Manually add the subcategories following the format
def subcategory_dict_ini():
# ----- Format: subcategory_dict['subcategory_id'] = 'Category Name' -----

# ICO
  subcategory_dict['5lerr0mq'] = '60Hz'
  subcategory_dict['jq600wvq'] = '60Hz'
  subcategory_dict['0q5nnm7q'] = '50Hz'
  subcategory_dict['4lxppk3q'] = 'PS2 NTSC-U'

# SotC (2018)
  subcategory_dict['xqkr6341'] = 'Easy'
  subcategory_dict['gq7nzor1'] = 'Normal'
  subcategory_dict['21gjo6o1'] = 'Hard'

def run_scraper(game, game_dict):
  for category in game.categories:
    if not category.name in game_dict:
      game_dict[category.name] = {}
    if category.type == 'per-level':
      for level in game.levels:
        game_dict[category.name][level.name] = dt.Leaderboard(api, data=api.get("leaderboards/{}/level/{}/{}?embed=variables".format(game.id, level.id, category.id)))
    else:
      game_dict[category.name] = dt.Leaderboard(api, data=api.get("leaderboards/{}/category/{}?embed=variables".format(game.id, category.id)))

def run_ini_simple(r, current_run):
  if len(r.values.values()) > 0:
    subcategory_parse(list(r.values.values())[0], current_run)
  current_run["player"] = r.players
  current_run["times"] = r.times
  current_run["videos"] = r.videos
  current_run["date"] = r.date


def run_parse(keys, writer, game_dict, simple):
  for category in keys:
    category_dict = {}

    # Full Game Runs
    if type(game_dict[category]) is srcomapi.datatypes.Leaderboard:
      writer.writerow([category])
      i = 1
      for run in game_dict[category].runs:
        current_run = {}
        if simple:
          run_ini_simple(run["run"], current_run)
        else:
          current_run = run["run"].data

        category_dict[i] = current_run
        i = i + 1

    for k,v in category_dict.items():
      writer.writerow([k, v])

def subcategory_parse(subcategory, current_run):
  if subcategory in subcategory_dict:
    current_run["subcategory"] = subcategory_dict[subcategory]
  else:
    current_run["subcategory"] = subcategory

subcategory_dict_ini()

### --------------------------------------------------------- ###
# ----- Example Code Implementation: replace all "game_name" instances with whatever game you're going to extract -----
# ----- Best practice to write the exact name in "game name" at the end -----
# game_name = api.search(srcomapi.datatypes.Game, {"name": "game name"})[0] 
# game_name_runs = {}
# run_scraper(game_name, game_name_runs)
# game_name_csv = open("game_name.csv", "w", encoding='utf-8')
# game_name_writer = csv.writer(game_name_csv)
# ----- Simple flag is for the complexity of the data. True for Simple, False for complex -----
# run_parse(game_name_runs.keys(), game_name_writer, game_name_runs, simple_flag)
# game_name_csv.close()

# ICO
ico = api.search(srcomapi.datatypes.Game, {"name": "ico"})[0]
ico_runs = {}
run_scraper(ico, ico_runs)
ico_csv = open("ico.csv", "w", encoding='utf-8')
ico_writer = csv.writer(ico_csv)
run_parse(ico_runs.keys(), ico_writer, ico_runs, True)
ico_csv.close()

# SotC
sotc = api.search(srcomapi.datatypes.Game, {"name": "shadow of the colossus"})[0]
sotc_runs = {}
run_scraper(sotc, sotc_runs)
sotc_csv = open("sotc.csv", "w", encoding='utf-8')
sotc_writer = csv.writer(sotc_csv)
run_parse(sotc_runs.keys(), sotc_writer, sotc_runs, True)
sotc_csv.close()

# SotC 2018
sotc_2018 = api.search(srcomapi.datatypes.Game, {"name": "shadow of the colossus (2018)"})[0]
sotc_2018_runs = {}
run_scraper(sotc_2018, sotc_2018_runs)
sotc_2018_csv = open("sotc_2018.csv", "w", encoding='utf-8')
sotc_2018_writer = csv.writer(sotc_2018_csv)
run_parse(sotc_2018_runs.keys(), sotc_2018_writer, sotc_2018_runs, True)
sotc_2018_csv.close()

# TLG
tlg = api.search(srcomapi.datatypes.Game, {"name": "the last guardian"})[0]
tlg_runs = {}
run_scraper(tlg, tlg_runs)
tlg_csv = open("tlg.csv", "w", encoding="utf-8")
tlg_writer = csv.writer(tlg_csv)
run_parse(tlg_runs.keys(), tlg_writer, tlg_runs, True)
tlg_csv.close()
