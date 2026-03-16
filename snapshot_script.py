import subprocess
import os
from dotenv import load_dotenv
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO,
                    format= "%(asctime)s [%(levelname)s] %(message)s")
load_dotenv()
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

file_path_global = "snapshots/"

def create_snapshot():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{dbname}_snapshot_{timestamp}.dump"    
    cmd = [
        "pg_dump",
        "-h", host,
        "-p", port,
        '-d', dbname,
        "-U", user,
        "-F", "c",
        '-f', f"{file_path_global}{filename}"
    ]
    env_copy = os.environ.copy()
    env_copy["PGPASSWORD"] = password
    try:
        subprocess.run(cmd, check=True, env=env_copy)
        print(f"Snapshot created successfully: {filename}")
        return filename
    except subprocess.CalledProcessError as e:
        print(f"Error creating snapshot: {e}")
        return None

def upload_to_s3(filename):
    import boto3
    s3 = boto3.client('s3')
    bucket_name = os.getenv("BUCKET_NAME")
    file_path = f"{file_path_global}{filename}"
    try:
        s3.upload_file(file_path, bucket_name, filename)
        logging.info(f"File {filename} uploaded to S3 bucket {bucket_name} successfully.")
    except Exception as e:
        logging.error(f"Error uploading file to S3: {e}")
if __name__ == "__main__":
    filename = create_snapshot()
    if filename:
        upload_to_s3(filename)