import sqlite3
from sentence_transformers import SentenceTransformer

# Initialize the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Your text data
texts = ["Hello, world!", "This is a sample text."]

# Generate embeddings
embeddings = model.encode(texts)

# Connect to Chroma DB (SQLite for this example)
conn = sqlite3.connect('chroma.db')
c = conn.cursor()

# Create a table (if not exists)
c.execute('''CREATE TABLE IF NOT EXISTS text_embeddings
             (id INTEGER PRIMARY KEY, text TEXT, embedding BLOB)''')

# Insert data
for text, embedding in zip(texts, embeddings):
    # Convert numpy array to bytes for storage
    embedding_blob = embedding.tobytes()
    c.execute("INSERT INTO text_embeddings (text, embedding) VALUES (?, ?)", (text, embedding_blob))

# Commit and close
conn.commit()
conn.close()