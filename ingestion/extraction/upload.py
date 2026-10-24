import boto3
import config.settings as settings
from pathlib import Path
import asyncio

class UploadPDF:
    def __init__(self):
        self.PROJECT_ROOT = Path(__file__).resolve().parents[2]
        self.PDF_FOLDER = self.PROJECT_ROOT / "ingestion" / "data"
        self.s3 = boto3.client(
            's3',
            region_name = settings.AWS_REGION,
            endpoint_url = settings.AWS_ENDPOINT_URL_S3,
            aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
        )
        self.BUCKET_NAME = settings.NEON_BUCKET_NAME

    async def upload_file(self, filepath):
        # define object key
        self.object_key = f"documents/{filepath.name}"

        # code to upload a single file
        await asyncio.to_thread(
            self.s3.upload_file,
            str(filepath),
            self.BUCKET_NAME,
            self.object_key
        )

        # print success statement
        # print(f"{filepath.name} uploaded successfully")

        # return statement
        return {
            "filename": filepath.name,
            "object_key": self.object_key,
            "success": True
        }

    async def upload_multiple_files(self):
        # iterate through all files in the folder with .pdf
        self.pdf_files = [file for file in self.PDF_FOLDER.iterdir() if file.is_file() and file.suffix.lower() == '.pdf']

        if not self.pdf_files:
            print("No pdf found")
            return []
        
        # call upload_pdf function for each file
        tasks = [self.upload_file(file) for file in self.pdf_files]

        self.results = await asyncio.gather(*tasks)

        # print successful statement
        self.successful = sum(
            result["success"] for result in self.results
        )

        # print(
        #     f"Upload complete: {successful}/{len(pdf_files)} successful."
        # )

        return self.results, self.successful

if __name__ == "__main__":
    uploader = UploadPDF()
    result, successful = asyncio.run(uploader.upload_multiple_files())
    print(f"{successful} pdfs uploaded successfully!!")

'''
# without asyncio

s3 = boto3.client(
    's3',
    region_name = settings.AWS_REGION,
    endpoint_url = settings.AWS_ENDPOINT_URL_S3,
    aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
)

BUCKET_NAME = settings.NEON_BUCKET_NAME

for filename in PDF_FOLDER.iterdir():
    if filename.suffix.lower() != ".pdf":
        continue

    filepath = str(filename)

    print(f"Processing: {filename.name}")

    s3.upload_file(
        filepath,
        BUCKET_NAME,
        f"documents/{filename.name}"
    )
'''