from create_embeddings import embed_single
from connect_to_db import db_cursor

def find_similar(text):
    embedding = embed_single(text)
    # --- Step 1: Connect to PostgreSQL ---
    with db_cursor() as cur:
        cur.execute(
            """
            select title, 
            description,
            description_embedding <=> %s::vector as cosine_dist
            from public.movies order by cosine_dist
            limit 5
            """,
            (embedding,)
        )

        rows = cur.fetchall()
        return rows

if __name__ == "__main__":
    # text = 'movies that are pro palestine and against israel'
    # text = 'movies that are pro palestine and against israel'
    # text = 'movie about a love story in australia'
    text = 'movie about a love story in a european capital city'
    rows = find_similar(text)
    for row in rows:
        print(row, '\n\n')