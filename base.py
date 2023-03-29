import json

from model.team import Team


def get_all_teams_from_json():
    with open('base_data.json', 'r') as f:
        data = json.load(f)

    teams = []
    for team in data:
        teams.append(Team(name=team['name'], score=0))

    return teams
