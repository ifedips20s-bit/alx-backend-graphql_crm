import os
import django
from django.utils import timezone

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_graphql.settings")
django.setup()

from crm.models import Customer, Product, Order

# --- Seed Customers ---
customers_data = [
    {"first_name": "Alice", "last_name": "Smith", "email": "alice@example.com", "phone": "+1234567890"},
    {"first_name": "Bob", "last_name": "Johnson", "email": "bob@example.com", "phone": "123-456-7890"},
    {"first_name": "Carol", "last_name": "Williams", "email": "carol@example.com", "phone": None},
]

customers = []
for c in customers_data:
    customer = Customer(**c)
    customer.full_clean()  # validates email, phone etc.
    customer.save()
    customers.append(customer)

print(f"Seeded {len(customers)} customers.")

# --- Seed Products ---
products_data = [
    {"name": "Laptop", "price": 999.99, "stock": 10},
    {"name": "Smartphone", "price": 499.99, "stock": 20},
    {"name": "Headphones", "price": 199.99, "stock": 50},
]

products = []
for p in products_data:
    product = Product(**p)
    product.full_clean()
    product.save()
    products.append(product)

print(f"Seeded {len(products)} products.")

# --- Seed Orders ---
orders_data = [
    {"customer": customers[0], "product_indices": [0, 2]},  # Alice buys Laptop + Headphones
    {"customer": customers[1], "product_indices": [1]},     # Bob buys Smartphone
]

orders = []
for o in orders_data:
    order = Order(customer=o["customer"], order_date=timezone.now())
    order.save()  # save before adding M2M
    selected_products = [products[i] for i in o["product_indices"]]
    order.products.set(selected_products)
    # calculate total_amount
    order.total_amount = sum(p.price for p in selected_products)
    order.save()
    orders.append(order)

print(f"Seeded {len(orders)} orders.")
