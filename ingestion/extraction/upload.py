import boto3
import config.settings as settings
import os
from pathlib import Path
import asyncio

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PDF_FOLDER = PROJECT_ROOT / "ingestion" / "data"

s3 = boto3.client(
    's3',
    region_name = settings.AWS_REGION,
    endpoint_url = settings.AWS_ENDPOINT_URL_S3,
    aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
)

BUCKET_NAME = settings.NEON_BUCKET_NAME

async def upload_file(filepath):
    # define object key
    object_key = f"documents/{filepath.name}"

    # code to upload a single file
    await asyncio.to_thread(
        s3.upload_file,
        str(filepath),
        BUCKET_NAME,
        object_key
    )

    # print success statement
    print(f"{filepath.name} uploaded successfully")

    # return statement
    return {
        "filename": filepath.name,
        "object_key": object_key,
        "success": True
    }

async def upload_multiple_files():
    # iterate through all files in the folder with .pdf
    pdf_files = [file for file in PDF_FOLDER.iterdir() if file.is_file() and file.suffix.lower() == '.pdf']

    if not pdf_files:
        print("No pdf found")
        return []
    
    # call upload_pdf function for each file
    tasks = [upload_file(file) for file in pdf_files]

    results = await asyncio.gather(*tasks)

    # print successful statement
    successful = sum(
        result["success"] for result in results
    )

    print(
        f"Upload complete: {successful}/{len(pdf_files)} successful."
    )

    return results

if __name__ == "__main__":
    asyncio.run(upload_multiple_files())

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