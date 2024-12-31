import re

import requests
import structlog
from sqlalchemy.orm import Session

from app.config import settings
from app.database import SessionLocal
from app.crud import create_raw_import

from scripts.process_raw_imports import process_raw_imports

logger = structlog.getLogger()

def download_file():
    response = requests.get(f"{settings.travian_server_url}/map.sql")
    response.raise_for_status()
    with open("data.sql", "w") as file:
        file.write(response.text)

def ingest_file():
    db: Session = SessionLocal()
    with open("data.sql", "r") as file:
        for line in file:
            if line.startswith("INSERT INTO"):
                # Parse the INSERT INTO line
                try:
                    create_raw_import(db, line)
                except ValueError as e:
                    logger.error(f"Error parsing line: {line} : {e}")

def main():
    # Download the file
    download_file()

    # Ingest the file
    ingest_file()

    # Process the raw imports
    process_raw_imports()


if __name__ == "__main__":
    main()
