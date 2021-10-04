from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import task1, task2


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(task1, 'interval', minutes=1, id="task_01", replace_existing=True)
    scheduler.add_job(task2, 'interval', minutes=2, id="task_02", replace_existing=True)
    scheduler.start()