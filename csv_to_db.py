import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from create_embeddings import embed_multi
import math
import re

# --- Step 1: Connect to PostgreSQL ---
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="123456"
)
cur = conn.cursor()



# --- Step 2: Convert the CSV file to a list---
df = pd.read_csv("movies.csv")
df = df[["original_title", "overview"]]
df = df.dropna(subset=["original_title", "overview"])

# clear non english letters
pattern = r'^[A-Za-z0-9\s.,!?\'":;()-]+$'
df = df[df['original_title'].apply(lambda x: bool(re.match(pattern, str(x))))]

rows = df.itertuples(index=False, name=None)
rows = list(rows)

def batch_list_to_db(batch):
    titles, descriptions = zip(*batch)
    embeddings = embed_multi(descriptions)
    payload = zip(titles, descriptions, embeddings)

    execute_values(
        cur,
        "INSERT INTO movies (title, description, description_embedding) VALUES %s",
        payload,
        page_size=100
    )

for i in range(0, len(rows), 1000):
    print(i)
    batch = rows[i:i+1000]
    batch_list_to_db(batch)

# --- Step 4: Commit and close ---
conn.commit()
cur.close()
conn.close()
