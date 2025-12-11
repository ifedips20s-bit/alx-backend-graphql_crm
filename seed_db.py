import os
import django
from datetime import datetime
from decimal import Decimal

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_graphql.settings")
django.setup()

from crm.models import Customer, Product, Order

# --- Clear existing data (optional) ---
Customer.objects.all().delete()
Product.objects.all().delete()
Order.objects.all().delete()

# --- Seed Customers ---
customers = [
    Customer(first_name="John", last_name="Doe", email="john@example.com", phone="1234567890"),
    Customer(first_name="Jane", last_name="Smith", email="jane@example.com", phone="9876543210"),
    Customer(first_name="Alice", last_name="Brown", email="alice@example.com", phone="5555555555"),
]

Customer.objects.bulk_create(customers)
print("Seeded customers.")

# --- Seed Products ---
products = [
    Product(name="Laptop", price=Decimal("1200.00"), stock=10),
    Product(name="Mouse", price=Decimal("25.50"), stock=50),
    Product(name="Keyboard", price=Decimal("45.00"), stock=30),
]

Product.objects.bulk_create(products)
print("Seeded products.")

# --- Seed Orders ---
# Fetch created objects
all_customers = list(Customer.objects.all())
all_products = list(Product.objects.all())

# Example orders
order1 = Order(customer=all_customers[0])
order1.save()
order1.products.set([all_products[0], all_products[1]])  # Laptop + Mouse

order2 = Order(customer=all_customers[1])
order2.save()
order2.products.set([all_products[1], all_products[2]])  # Mouse + Keyboard

order3 = Order(customer=all_customers[2])
order3.save()
order3.products.set([all_products[0], all_products[2]])  # Laptop + Keyboard

print("Seeded orders.")
