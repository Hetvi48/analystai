import os
import tempfile
import asyncio
import boto3
import config.settings as settings
from langchain_community.document_loaders import PyPDFLoader

class PDFExtract:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            region_name = settings.AWS_REGION,
            endpoint_url = settings.AWS_ENDPOINT_URL_S3,
            aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
        )
        self.BUCKET_NAME = settings.NEON_BUCKET_NAME

    async def extract_pdf(self, obj_key):
        """Download one PDF from Neon and extract its pages."""
        temp_path = None

        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(
                suffix = ".pdf",
                delete = False,
            )as temp_file:
                temp_path = temp_file.name

            # Download PDF from Neon Object Storage
            await asyncio.to_thread(
                self.s3.download_file,
                self.BUCKET_NAME,
                obj_key,
                temp_path,
            )

            # Load PDF from PyPDFLoader
            loader = PyPDFLoader(
                file_path = temp_path,
                extract_images = False,
                mode = "page",
                extraction_mode = "layout",
            )

            docs = await asyncio.to_thread(loader.load)

            # Preserve source filename in metadata
            for doc in docs:
                doc.metadata["source"] = obj_key.split("/")[-1]

            print(f"Extracted {len(docs)} pages from {obj_key}")

            return docs

        except Exception as e:
            print(f"Error extracting {obj_key} : {e}")
            return []

        finally:
            # Remove temporary file
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

    async def extract_multiple_pdfs(self):
        """Extract all pdfs from the documents/ prefix."""

        # list all objects from BUCKET with "documents/" prefix.
        response = await asyncio.to_thread(
            self.s3.list_objects_v2,
            Bucket = self.BUCKET_NAME,
            Prefix = "documents/",
        )

        # list of pdf keys
        pdf_keys = [obj["Key"] for obj in response.get("Contents", []) if obj["Key"].lower().endswith(".pdf")]

        # print pdf_keys - for testing
        # print("="*20)
        # print(pdf_keys)
        # print("="*20)
        # output:
        # ['documents/Hetvi-Khadela-4-Resume.pdf', 'documents/Hetvi-Khadela-4-Resume_new.pdf', 'documents/Hetvi-Khadela-4_college_new.pdf', 'documents/report.pdf']

        if not pdf_keys:
            print("No PDFs found in Neon object")
            return []

        tasks = [self.extract_pdf(key) for key in pdf_keys]

        # Extract PDFs concurrently
        results = await asyncio.gather(*tasks)

        # Combine pages from all PDFs
        all_docs = [doc for docs in results for doc in docs]

        print(f"total pages extracted: {len(all_docs)}")

        return all_docs

if __name__ == "__main__":
    extractor = PDFExtract()
    docs = asyncio.run(extractor.extract_multiple_pdfs())
    print(type(docs))
    # print(docs)