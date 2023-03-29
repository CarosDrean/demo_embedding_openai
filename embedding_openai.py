import os

import openai
from dotenv import load_dotenv

# charge .env globally
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')


def create_embedding_openai(prompt):
    response = openai.Embedding.create(
        input=prompt,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']
