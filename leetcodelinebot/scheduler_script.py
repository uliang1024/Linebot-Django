from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import timezone

from leetcodelinebot.views import settlement_event, reminder_event, report_event

def scheduler_event():
    # 创建一个调度器对象
    scheduler = BlockingScheduler()

    # 设置台湾时区
    taipei_tz = timezone('Asia/Taipei')

    # 添加定时任务，并设置触发时间（台湾时间）
    scheduler.add_job(settlement_event, 'cron', hour=13, minute=56, timezone=taipei_tz)
    scheduler.add_job(reminder_event, 'cron', hour=13, minute=58, timezone=taipei_tz)
    scheduler.add_job(report_event, 'cron', hour=14, minute=0, timezone=taipei_tz)

    # 启动调度器
    scheduler.start()