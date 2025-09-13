import os
import psycopg2
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# 2. Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def embed_single(text):
    # 3. Create embedding
    response = client.embeddings.create(
        model="text-embedding-3-small",  # or text-embedding-3-large
        input=text
    )
    embedding =  response.data[0].embedding
    return embedding

def embed_multi(texts):
    # 3. Create embedding
    response = client.embeddings.create(
        model="text-embedding-3-small",  # or text-embedding-3-large
        input=texts
    )
    embeddings = [d.embedding for d in response.data]
    return embeddings



if __name__ == "__main__":
    print(len(embed_multi(['hello', 'by'])))