import asyncio
import re

import requests
import structlog
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.config import settings
from app.database import AsyncSessionLocal
from app.crud import create_raw_import

from scripts.process_raw_imports import process_raw_imports

logger = structlog.getLogger()

async def download_file():
    response = requests.get(f"{settings.travian_server_url}/map.sql")
    response.raise_for_status()
    with open("data.sql", "w") as file:
        file.write(response.text)

async def ingest_file():
    async with AsyncSessionLocal() as session:
        with open("data.sql", "r") as file:
            for line in file:
                if line.startswith("INSERT INTO"):
                    # Parse the INSERT INTO line
                    try:
                        await create_raw_import(session, line)
                    except ValueError as e:
                        logger.error(f"Error parsing line: {line} : {e}")

async def main():
    # Download the file
    await download_file()

    # Ingest the file
    await ingest_file()

    # Process the raw imports
    await process_raw_imports()


if __name__ == "__main__":
    asyncio.run(main())
