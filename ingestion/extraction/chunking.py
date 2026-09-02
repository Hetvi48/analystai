from ingestion.extraction.extract import extract_pdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
import config.settings as settings

def chunk_documents():
    docs = extract_pdf()

    splitter = RecursiveCharacterTextSplitter(
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

    chunks = splitter.split_documents(docs)

    return chunks

if __name__ == '__main__':
    docs = extract_pdf()
    # content_new = ' '.join(content)
    print(type(docs))
    # print(docs)
    chunks = chunk_documents(docs)
    for chunk in chunks:
        print("="*20)
        print(chunk.metadata)
        print(chunk.page_content)