import os

import psycopg2
from model.data_embedding import MDataEmbedding


class DataEmbedding:
    POSTGRES_GET_ALL = "SELECT id, input, teams, embeddings FROM local.embeddings_jarbeer"
    POSTGRES_UPDATE = "UPDATE local.embeddings_jarbeer SET embeddings = %s, updated_at = now() WHERE id = %s"

    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.port = os.getenv('DB_PORT')
        self.dbname = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.conn = None

    def __enter__(self):
        self.conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.dbname,
            user=self.user,
            password=self.password
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

    def get_data_embeddings(self):
        with self.conn.cursor() as cursor:
            cursor.execute(self.POSTGRES_GET_ALL)
            records = cursor.fetchall()

        list_embeddings = []
        for record in records:
            embeddings_float = [float(d) for d in record[3]]
            list_embeddings.append(
                MDataEmbedding(id_embedding=record[0], input_embedding=record[1], teams=record[2],
                               embeddings=embeddings_float))

        return list_embeddings

    def update_data_embedding(self, id_embedding, embeddings):
        with self.conn.cursor() as cursor:
            cursor.execute(self.POSTGRES_UPDATE, (embeddings, id_embedding))
            self.conn.commit()
