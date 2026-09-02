import os
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

INDEX_NAME = "analyst-rag"

chunk_Size = 1000
chunk_Overlap = 150

dimensions = 1024
metric = "cosine"
model = "llama-text-embed-v2"