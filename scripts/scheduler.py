from apscheduler.schedulers.blocking import BlockingScheduler
from scripts.download_and_ingest import download_file, ingest_file
from scripts.process_raw_imports import process_raw_imports


async def run_pipeline():
    print("Beginning pipeline.")
    await download_file()
    print("File downloaded.")
    await ingest_file()
    print("Raw data ingested.")
    await process_raw_imports()
    print("Data processed.")


if __name__ == "__main__":
    scheduler = BlockingScheduler()

    # Add a scheduled task to the pipeline
    scheduler.add_job(run_pipeline, "cron", hour=0, minute=1)  # Every day at 00:01

    print("Scheduler started. Use Ctrl+C to quit.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")
