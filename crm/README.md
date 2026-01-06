# CRM Celery Setup

## Prerequisites
- Redis running at `redis://localhost:6379/0`
- Python virtual environment activated

## Steps

1. Install dependencies:

pip install -r requirements.txt


2. Apply migrations:

python manage.py migrate


3. Start Celery worker:


celery -A crm worker -l info


4. Start Celery Beat:


celery -A crm beat -l info


5. Logs:
- CRM reports are written to `/tmp/crm_report_log.txt`
