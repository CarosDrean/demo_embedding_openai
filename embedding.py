from typing import List
import numpy as np

from model.data_embedding import MDataEmbedding
from data_embedding_storage import DataEmbedding
from embedding_openai import create_embedding_openai


def create_embeddings_in_storage():
    with DataEmbedding() as storage:
        data_embeddings = storage.get_data_embeddings()

        for data in data_embeddings:
            embedding = create_embedding_openai(data.input)
            storage.update_data_embedding(data.id, embedding)


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def get_similarities_with_list(prompt, data_embeddings: List[MDataEmbedding]):
    embedding_prompt = create_embedding_openai(prompt)

    similarities = []
    for data in data_embeddings:
        if data.embeddings is None:
            break

        similarities.append(cosine_similarity(embedding_prompt, data.embeddings))

    return similarities
