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
        '-f', filename
    ]
    env_copy = os.environ.copy()
    env_copy["PGPASSWORD"] = password
    try:
        subprocess.run(cmd, check=True, env=env_copy)
        print(f"Snapshot created successfully: {filename}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating snapshot: {e}")
if __name__ == "__main__":
    create_snapshot()