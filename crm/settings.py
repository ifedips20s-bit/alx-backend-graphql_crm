INSTALLED_APPS = [
    # ... other apps
    "django_crontab",
]


CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),  # heartbeat every 5 minutes
    ('0 */12 * * *', 'crm.cron.update_low_stock'),  # low-stock update every 12 hours
    ('0 8 * * *', 'crm.cron.send_order_reminders'), # daily order reminders at 8 AM
]
