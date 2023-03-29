import json
from typing import List

from embedding import create_embeddings_in_storage, get_similarities_with_list
from data_embedding_storage import DataEmbedding
from model.data_embedding import MDataEmbedding
from model.team import Team
from model.util import ResultCalculate
from base import get_all_teams_from_json

PRODUCT_FOR_SIMILARITY = 0.2
THRESHOLD = 0.85


def calculate(prompt, data_embeddings: List[MDataEmbedding], threshold=THRESHOLD):
    similarities = get_similarities_with_list(prompt, data_embeddings)

    results = []
    # obtained result according similarities and threshold
    for i, similarity in enumerate(similarities):
        if similarity > threshold:
            results.append(ResultCalculate(data_embeddings[i].teams, similarity))

    results = sorted(results, key=lambda x: x.similarity, reverse=True)

    # teams = get_all_teams_from_json()
    # teams = calculate_score_of_teams_with_results(results, teams)
    teams = calculate_score_of_teams_with_results(results)

    teams = sorted(teams, key=lambda x: x.score, reverse=True)

    return teams


def calculate_score_of_teams_with_results(results: List[ResultCalculate], teams=None):
    if teams is None:
        teams = []

    for result in results:
        increase_for_exist = (result.similarity * PRODUCT_FOR_SIMILARITY)

        for name_team in result.teams:
            is_exist_team = False

            for i, team in enumerate(teams):
                if team.name == name_team:
                    is_exist_team = True
                    if teams[i].score == 0:
                        teams[i].score = result.similarity
                        continue

                    teams[i].score = teams[i].score + increase_for_exist

            if is_exist_team:
                continue

            teams.append(Team(name=name_team, score=result.similarity))

    return teams


def consult():
    with DataEmbedding() as storage:
        data_embeddings = storage.get_data_embeddings()

    while True:
        prompt = input("\nIngresa la iniciativa a calcular: ")

        if prompt == '':
            continue

        if prompt == 'create':
            create_embeddings_in_storage()

            with DataEmbedding() as storage:
                data_embeddings = storage.get_data_embeddings()

            print('Embeddings creados satisfactoriamente.')
            continue

        if prompt == "exit":
            break

        results = calculate(prompt, data_embeddings)

        print('========================')
        print('Resultado: ', json.dumps([x.__dict__ for x in results]))


if __name__ == '__main__':
    consult()
