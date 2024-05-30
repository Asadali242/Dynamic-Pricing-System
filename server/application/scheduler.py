import atexit
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def initialize_scheduler():
    scheduler.start()

def register_jobs(hourly_update, new_minute_update, seasonal_update, hourly_suggestion_emitter, seasonal_suggestion_emitter, clear_expired_rules, socketio, suggestions):
    scheduler.add_job(hourly_update, 'cron', hour='*')  

    scheduler.add_job(hourly_suggestion_emitter, 'cron', hour='*', args=[socketio, suggestions])
    #should be every hour like above, just doing minute for testing below
    #scheduler.add_job(hourly_suggestion_emitter, 'cron', minute='*', args=[socketio, suggestions])

    scheduler.add_job(seasonal_suggestion_emitter, 'cron', month='3,6,9,12', day='1-7', hour='0-23', minute='*', args=[socketio, suggestions])
    #should be every first week of every season like above, just doing minute for testing below
    #scheduler.add_job(seasonal_suggestion_emitter, 'cron', minute='*', args=[socketio, suggestions]) 

    scheduler.add_job(new_minute_update, 'cron', minute='*')
    scheduler.add_job(seasonal_update, 'cron', month='3,6,9,12', day='1', hour='0', minute='0')  
    scheduler.add_job(clear_expired_rules, 'cron', minute='*')

def register_shutdown():
    atexit.register(lambda: scheduler.shutdown())