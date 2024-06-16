import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer

class ChromaDBManager:
    def __init__(self, db_path='chroma.db'):
        self.db_path = db_path
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()
        self.create_embeddings_table()

    def create_embeddings_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS embeddings
                          (id INTEGER PRIMARY KEY, text TEXT, embedding BLOB)''')
        self.conn.commit()

    def add_texts_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            texts = file.readlines()
        
        embeddings = self.model.encode(texts)

        for text, embedding in zip(texts, embeddings):
            embedding_blob = embedding.tobytes()
            self.c.execute("INSERT INTO embeddings (text, embedding) VALUES (?, ?)", (text.strip(), embedding_blob))
        
        self.conn.commit()

    def close(self):
        self.conn.close()

# Example usage
if __name__ == "__main__":
    db_manager = ChromaDBManager()
    db_manager.create_embeddings_table()
    db_manager.add_texts_from_file('corpus.txt')
    db_manager.close()