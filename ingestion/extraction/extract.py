from langchain_community.document_loaders import PyPDFLoader
import os

def load_pdf():
    pdf_path = "ingestion/data/report.pdf"
    return pdf_path

# check is the file exist or not
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

    docs = loader.load()
    return docs

    # it is also possible to get content and metadata separately after extracting the document.
    # docs = []
    # docs_lazy = loader.load()
    # for doc in docs_lazy:
    #     docs.append(doc)
    # content = []
    # metadata = []
    # for page in docs:
    #     content.append(page.page_content)
    #     metadata.append(page.metadata)
    # return content, metadata
    # print(docs[0].metadata)

if __name__ == '__main__':
    docs = extract_pdf()
    print(type(docs))
    print(docs)

    # if you use the content and metadata, uncomment the following 
    # content, metadata = extract_pdf()
    # print(content)
    # print("====================================================")
    # print(metadata)