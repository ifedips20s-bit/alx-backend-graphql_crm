INSTALLED_APPS = [
    # ... other apps
    "django_crontab",
    "django_celery_beat",
]


CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),  # heartbeat every 5 minutes
    ('0 */12 * * *', 'crm.cron.update_low_stock'),  # low-stock update every 12 hours
    ('0 8 * * *', 'crm.cron.send_order_reminders'), # daily order reminders at 8 AM
]

# Celery configuration
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'generate-crm-report': {
        'task': 'crm.tasks.generate_crm_report',
        'schedule': crontab(day_of_week='mon', hour=6, minute=0),
    },
}