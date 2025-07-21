from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.utils.reminder import push_same_message 

scheduler = AsyncIOScheduler()

def start_scheduler():
    scheduler.add_job(push_same_message, "interval", hours=24)
    scheduler.start()