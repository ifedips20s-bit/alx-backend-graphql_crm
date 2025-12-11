import graphene
from graphene_django import DjangoObjectType
from crm.models import Customer

class Query(CRMQuery, graphene.ObjectType):
    pass

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ("id", "first_name", "last_name", "email")

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQL!")
    customers = graphene.List(CustomerType)

    def resolve_customers(root, info):
        return Customer.objects.all()

schema = graphene.Schema(query=Query)
