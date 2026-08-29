from langchain_community.document_loaders import PyPDFLoader
import os

def load_pdf():
    pdf_path = "ingestion/data/report.pdf"
    return pdf_path

# if os.path.exists(pdf_path):
#     print("yes")
# else:
#     print("no")
def extract_pdf():
    loader = PyPDFLoader(
        file_path=load_pdf(),
        extract_images=False,
        mode='page',
        extraction_mode='layout'
    )

    docs = []
    docs_lazy = loader.lazy_load()
    for doc in docs_lazy:
        docs.append(doc)
    content = []
    metadata = []
    for page in docs:
        content.append(page.page_content)
        metadata.append(page.metadata)
    return content, metadata
    # print(docs[0].metadata)


if __name__ == '__main__':
    content, metadata = extract_pdf()
    print(content)
    print("====================================================")
    print(metadata)