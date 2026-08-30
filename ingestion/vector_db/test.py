from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_pinecone import PineconeEmbeddings
import config.settings as settings

PINECONE_API_KEY = settings.PINECONE_API_KEY

INDEX_NAME = settings.INDEX_NAME

# Create embedding model

embeddings = PineconeEmbeddings(
    model="llama-text-embed-v2",
    pinecone_api_key=PINECONE_API_KEY
)

# Connect to Pinecone

pc = Pinecone(
    api_key=PINECONE_API_KEY
)

# Connect to existing index

index = pc.Index(INDEX_NAME)

vectorstore = PineconeVectorStore(
    index=index,
    embedding=embeddings
)

# Search

query = "I want to understand the market overview. for that you can give me some of the key metrices in order to understand this overview in better way."

results = vectorstore.similarity_search_with_score(
    query,
    k=2
)

# Display results

print("\nSearch results:\n")

for i, (document, score) in enumerate(results, start=1):

    print("=" * 60)

    print(f"Result #{i}")
    print(f"Similarity score: {score}")

    print("\nText:")
    print(document.page_content)

    print("\nMetadata:")
    print(document.metadata)

print("=" * 60)