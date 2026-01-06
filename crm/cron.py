#!/usr/bin/env python3
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL endpoint
GRAPHQL_URL = "http://localhost:8000/graphql"

# Set up the transport and client
transport = RequestsHTTPTransport(url=GRAPHQL_URL, verify=True, retries=3)
client = Client(transport=transport, fetch_schema_from_transport=True)

# Define the mutation
mutation = gql("""
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
    """Executes the low-stock mutation and logs updated products."""
    try:
        result = client.execute(mutation)
        updated_products = result.get("updateLowStockProducts", {}).get("products", [])
        success_message = result.get("updateLowStockProducts", {}).get("success", "")

        log_file = "/tmp/low_stock_updates_log.txt"
        with open(log_file, "a") as f:
            f.write(f"\n--- {datetime.now()} ---\n")
            f.write(f"{success_message}\n")
            for product in updated_products:
                f.write(f"Product: {product['name']}, Stock: {product['stock']}\n")

        print("Low stock update processed!")

    except Exception as e:
        print(f"Error updating low-stock products: {e}")

/tmp/crm_heartbeat_log.txt", "def log_crm_heartbeat():