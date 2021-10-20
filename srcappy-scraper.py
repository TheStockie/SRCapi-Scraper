import requests as r

# response.json() returns a dict of the json

test = r.get('https://www.speedrun.com/api/v1')

def get_game(game_name):
    return r.get('https://www.speedrun.com/api/v1/games/{}'.format(game_name))

def get_category(game_name):
    result = {}
    categories = r.get('https://www.speedrun.com/api/v1/games/{}/categories'.format(game_name))
    for category in categories.json()["data"]:
        if category['type'] == 'per-game':
            result[category["name"]] = category["id"]
    return result

def get_category_runs(category_id):
    return r.get('https://www.speedrun.com/api/v1/runs?category={}&orderby=verify-date&direction=desc&max=200'.format(category_id)).json()

result = get_category_runs("rklxqxwk")
print(len(get_category_runs("rklxqxwk")["data"]))
