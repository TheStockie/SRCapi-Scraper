import srcomapi, srcomapi.datatypes as dt
import csv
api = srcomapi.SpeedrunCom(); api.debug = 1

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

test = {}
# Parsing data
for category in ico_runs.keys():
    test2 = {}
    if type(ico_runs[category]) is srcomapi.datatypes.Leaderboard:
        test3 = {}
        i = 1
        for run in ico_runs[category].runs:
            true_run = run["run"]
            print(true_run)
            test3["player"] = true_run.players
            test3["times"] = true_run.times
            test3["videos"] = true_run.videos
            test3["date"] = true_run.date

            test2[i] = test3
            i = i + 1
        test[category] = test2

ico_csv = open("ico.csv", "w")
writer = csv.writer(ico_csv)

for key, value in test.items():
    writer.writerow([key, value])

ico_csv.close()