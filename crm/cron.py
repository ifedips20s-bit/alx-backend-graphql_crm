#!/usr/bin/env python3
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL endpoint
GRAPHQL_URL = "http://localhost:8000/graphql"

# Set up the transport and client
transport = RequestsHTTPTransport(url=GRAPHQL_URL, verify=True, retries=3)
client = Client(transport=transport, fetch_schema_from_transport=True)

# --- GraphQL mutation for low stock products ---
low_stock_mutation = gql("""
mutation {
  updateLowStockProducts {
    success
    products {
      id
      name
      stock
    }
  }
}
""")

def update_low_stock():
    log_file = "/tmp/low_stock_updates_log.txt"
    try:
        result = client.execute(low_stock_mutation)
        updated_products = result.get("updateLowStockProducts", {}).get("products", [])
        
        with open(log_file, "a") as f:
            f.write(f"\n--- {datetime.now()} ---\n")
            f.write(result.get("updateLowStockProducts", {}).get("success", "No success message") + "\n")
            for product in updated_products:
                f.write(f"Product ID: {product['id']}, Name: {product['name']}, Stock: {product['stock']}\n")
        
        print("Low stock products updated and logged!")

    except Exception as e:
        with open(log_file, "a") as f:
            f.write(f"\n--- {datetime.now()} ---\n")
            f.write(f"Error updating low stock products: {e}\n")
        print(f"Error updating low stock products: {e}")

# --- CRM heartbeat logger ---
def log_crm_heartbeat():
    heartbeat_log_file = "/tmp/crm_heartbeat_log.txt"
    try:
        with open(heartbeat_log_file, "a") as f:
            f.write(f"{datetime.now()} CRM is alive\n")
        print("CRM heartbeat logged!")
    except Exception as e:
        print(f"Error logging CRM heartbeat: {e}")
