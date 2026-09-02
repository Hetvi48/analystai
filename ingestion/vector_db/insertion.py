import config.settings as settings
from ingestion.extraction.chunking import chunk_documents
from langchain_pinecone import PineconeVectorStore
from langchain_pinecone import PineconeEmbeddings
from pinecone import Pinecone, ServerlessSpec

class Insertion:
    def __init__(self):
        self.pinecone_api_key = settings.PINECONE_API_KEY
        self.INDEX_NAME = settings.INDEX_NAME
        self.chunks = chunk_documents()

    def createIndex(self):
        try:
            pc = Pinecone(pinecone_api_key=self.pinecone_api_key)
            if not pc.has_index(self.INDEX_NAME):

                pc.create_index(
                    name = self.INDEX_NAME,
                    dimension = settings.dimensions,
                    metric = settings.metric,
                    spec=ServerlessSpec(
                        cloud="aws",
                        region="us-east-1"
                    )
                )
            return True
        except Exception as e:
            print("inedax creation failed")
            return False

    def embeddings(self):
        if self.createIndex():
            try:
                self.embeddings = PineconeEmbeddings(
                    model = settings.model,
                    pinecone_api_key = self.pinecone_api_key
                )
                return self.embeddings
            except Exception as e:
                return False
        else:
            print("Index is not created")
            return False

    def vecStore(self):
        self.embedding = self.embeddings()
        if self.embedding:
            try:
                self.vectorstore = PineconeVectorStore.from_documents(
                    documents=self.chunks,
                    embedding=self.embedding,
                    index_name=self.INDEX_NAME
                )
                return True
            except Exception as e:
                print("problem in vector store")
                return False
        else:
            print("Embeddings are not created yet")
            return False

if __name__ == '__main__':
    inser = Insertion()
    if inser.vecStore():
        print("Successful")
    else:
        print("Failed")