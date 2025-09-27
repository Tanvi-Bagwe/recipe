import time
from datetime import datetime
import requests
import schedule
from logger import logger


def job():
    try:
        logger.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Pinging self to stay awake...")
        
        response = requests.get("https://www.recipehub.pro")
        if response.status_code != 200:
            response = requests.get("https://recipe-92ry.onrender.com")
        logger.info(f"Response: {response.status_code}")
        logger.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Pinged self to stay awake")
    except Exception as e:
        logger.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ping failed: {e}")


# schedule job every 5 minutes
schedule.every(5).minutes.do(job)


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    logger.info("Starting scheduler...")
    run_scheduler()
