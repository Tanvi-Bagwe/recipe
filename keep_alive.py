import threading
import time
from datetime import datetime

import requests
import schedule


def job():
    try:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Pinging self to stay awake...")
        response = requests.get("https://www.recipehub.pro")
        if response.status_code != 200:
            response = requests.get("https://recipe-92ry.onrender.com")
        print(response)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Pinged self to stay awake")
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ping failed: {e}")
    time.sleep(1)


schedule.every(5).minutes.do(job)


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


def start_scheduler():
    t = threading.Thread(target=run_scheduler)
    t.daemon = True
    t.start()
