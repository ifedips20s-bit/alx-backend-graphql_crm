#!/usr/bin/env python3
import os
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL endpoint
GRAPHQL_URL = "http://localhost:8000/graphql"

# Set up the transport and client
transport = RequestsHTTPTransport(url=GRAPHQL_URL, verify=True, retries=3)
client = Client(transport=transport, fetch_schema_from_transport=True)

# GraphQL query for orders in the last 7 days
seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()

query = gql("""
query getRecentOrders($dateGte: DateTime!) {
  allOrders(filter: { orderDateGte: $dateGte }) {
    edges {
      node {
        id
        customer {
          email
        }
        orderDate
      }
    }
  }
}
""")

params = {"dateGte": seven_days_ago}

try:
    result = client.execute(query, variable_values=params)
    orders = result.get("allOrders", {}).get("edges", [])
    
    log_file = "/tmp/order_reminders_log.txt"
    with open(log_file, "a") as f:
        f.write(f"\n--- {datetime.now()} ---\n")
        for edge in orders:
            order = edge["node"]
            order_id = order["id"]
            customer_email = order["customer"]["email"]
            f.write(f"Order ID: {order_id}, Customer: {customer_email}\n")
    
    print("Order reminders processed!")

except Exception as e:
    print(f"Error querying GraphQL endpoint: {e}")
