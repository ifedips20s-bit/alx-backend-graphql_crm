#!/bin/bash

# Activate virtual environment (adjust path to your venv)
source /home/ifedips/desktop/alx-backend-graphql_crm/venv/bin/activate

# Navigate to the Django project root
cd /home/ifedips/desktop/alx-backend-graphql_crm

# Run Django shell command to delete inactive customers
DELETED_COUNT=$(python manage.py shell -c "
from crm.models import Customer
from django.utils import timezone
from datetime import timedelta

one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(order__isnull=True, created_at__lt=one_year_ago)
count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

# Log the result with timestamp
echo \"\$(date '+%Y-%m-%d %H:%M:%S') - Deleted \$DELETED_COUNT inactive customers\" >> /tmp/customer_cleanup_log.txt
