from celery import shared_task
import requests
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

GRAPHQL_URL = "http://localhost:8000/graphql"

transport = RequestsHTTPTransport(url=GRAPHQL_URL, verify=True, retries=3)
client = Client(transport=transport, fetch_schema_from_transport=True)

@shared_task
def generate_crm_report():
    query = gql("""
    query {
      allCustomers {
        totalCount
      }
      allOrders {
        edges {
          node {
            totalAmount
          }
        }
      }
    }
    """)

    try:
        result = client.execute(query)
        total_customers = result.get("allCustomers", {}).get("totalCount", 0)
        orders = result.get("allOrders", {}).get("edges", [])
        total_orders = len(orders)
        total_revenue = sum(float(order["node"]["totalAmount"]) for order in orders)

        log_file = "/tmp/crm_report_log.txt"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, "a") as f:
            f.write(f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n")

        print("CRM report generated successfully!")

    except Exception as e:
        print(f"Error generating CRM report: {e}")
