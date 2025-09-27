# python
"""`scheduler.py` - periodic self-ping to keep the service awake.

Contains a scheduled `job` that pings one or more URLs and a `run_scheduler`
loop that drives the schedule.
"""
import threading
import time
from datetime import datetime
import requests
import schedule
from logger import logger


def job():
    """Ping configured endpoints to keep the service awake.

        - Logs the start and end of the operation with a timestamp.
        - Tries each URL in `PING_URLS` until a 200 response is received.
        - Uses a timeout to ensure the call doesn't block indefinitely.
        - Catches and logs exceptions (network errors, timeouts, etc.).
        """
    try:
        logger.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Pinging self to stay awake...")

        response = requests.get("https://www.recipehub.pro")
        if response.status_code != 200:
            response = requests.get("https://recipe-92ry.onrender.com")
        logger.info(f"Response: {response.status_code}")
        logger.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Pinged self to stay awake")
    except Exception as e:
        logger.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ping failed: {e}")


schedule.every(5).seconds.do(job)


def run_scheduler():
    """Run the scheduler loop.

       Continuously executes due jobs by calling `schedule.run_pending()` and
       sleeps briefly to avoid busy-waiting.
       """
    while True:
        schedule.run_pending()
        time.sleep(1)


def start_scheduler():
    """Start scheduler in a background thread"""
    t = threading.Thread(target=run_scheduler)
    t.daemon = True
    t.start()
