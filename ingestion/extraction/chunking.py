# from ingestion.extraction.extract import extract_pdf
from ingestion.extraction.download_pdf import PDFExtract
import asyncio
from langchain_text_splitters import RecursiveCharacterTextSplitter
import config.settings as settings

class ChunkDoc:
    def __init__(self):
        extractor = PDFExtract()
        self.docs = asyncio.run(extractor.extract_multiple_pdfs())

    def chunk_documents(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = settings.chunk_Size,
            chunk_overlap = settings.chunk_Overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

        self.chunks = self.splitter.split_documents(self.docs)
        return self.chunks

if __name__ == '__main__':
    obj = ChunkDoc()

    print(f"Total extracted pages: {len(obj.docs)}")

    chunks = obj.chunk_documents()

    print(f"Total chunks generated: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        print("=" * 40)
        print(f"Chunk number: {i + 1}")
        print(f"Metadata: {chunk.metadata}")
        print(f"Content preview: {chunk.page_content}")