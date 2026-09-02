from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_pinecone import PineconeEmbeddings
import config.settings as settings

class Retrieval:
    def __init__(self):
        self.PINECONE_API_KEY = settings.PINECONE_API_KEY
        self.INDEX_NAME = settings.INDEX_NAME

    def embedding_and_vectSore(self):
        # Create embedding model
        self.embeddings = PineconeEmbeddings(
            model=settings.model,
            pinecone_api_key=self.PINECONE_API_KEY
        )

        # Connect to Pinecone
        self.pc = Pinecone(
            api_key=self.PINECONE_API_KEY
        )

        # Connect to existing index
        self.index = self.pc.Index(self.INDEX_NAME)

        self.vectorstore = PineconeVectorStore(
            index = self.index,
            embedding = self.embeddings
        )

        return self.vectorstore

    def retrieval(self, query):
        self.vectorstore = self.embedding_and_vectSore()
        # Search
        self.results = self.vectorstore.similarity_search_with_score(
            query,
            k = settings.K
        )

        return self.results


if __name__ == '__main__':
    query = "I want to understand the market overview. for that you can give me some of the key metrices in order to understand this overview in better way."
    retrive_chunk = Retrieval()
    results = retrive_chunk.retrieval(query)

    for i, (document, score) in enumerate(results, start = 1):
        print('='*30)
        print(f"Result 1: ")
        print(f"Similarity Score: {score}")
        print(f"\nRetrieved Text: ")
        print(document.page_content)
        print("\nMetadata:")
        print(document.metadata)