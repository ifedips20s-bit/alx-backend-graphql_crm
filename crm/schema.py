import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from .models import Customer, Product, Order
from .filters import CustomerFilter, ProductFilter, OrderFilter

# --- GraphQL Types ---
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ("id", "first_name", "last_name", "email", "phone", "created_at")
        filterset_class = CustomerFilter

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "price", "stock")
        filterset_class = ProductFilter

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ("id", "customer", "products", "total_amount", "order_date")
        filterset_class = OrderFilter

# --- Mutations ---
class CreateCustomer(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, first_name, last_name, email, phone=None):
        if Customer.objects.filter(email=email).exists():
            raise ValidationError("Email already exists.")
        customer = Customer(first_name=first_name, last_name=last_name, email=email, phone=phone)
        customer.full_clean()
        customer.save()
        return CreateCustomer(customer=customer, message="Customer created successfully.")

class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(
            graphene.InputObjectType(
                name="CustomerInput",
                fields={
                    "first_name": graphene.String(required=True),
                    "last_name": graphene.String(required=True),
                    "email": graphene.String(required=True),
                    "phone": graphene.String()
                }
            )
        )

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, input):
        created_customers = []
        errors = []
        with transaction.atomic():
            for c in input:
                try:
                    if Customer.objects.filter(email=c.email).exists():
                        raise ValidationError(f"Email {c.email} already exists.")
                    customer = Customer(
                        first_name=c.first_name,
                        last_name=c.last_name,
                        email=c.email,
                        phone=c.get("phone")
                    )
                    customer.full_clean()
                    customer.save()
                    created_customers.append(customer)
                except ValidationError as e:
                    errors.append(str(e))
        return BulkCreateCustomers(customers=created_customers, errors=errors)

class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        stock = graphene.Int(default_value=0)

    product = graphene.Field(ProductType)

    def mutate(self, info, name, price, stock=0):
        if price <= 0:
            raise ValidationError("Price must be positive.")
        if stock < 0:
            raise ValidationError("Stock cannot be negative.")
        product = Product(name=name, price=price, stock=stock)
        product.save()
        return CreateProduct(product=product)

class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)
        order_date = graphene.DateTime(default_value=timezone.now)

    order = graphene.Field(OrderType)

    def mutate(self, info, customer_id, product_ids, order_date=None):
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise ValidationError("Invalid customer ID.")

        products = Product.objects.filter(id__in=product_ids)
        if not products.exists():
            raise ValidationError("No valid products selected.")

        order = Order(customer=customer, order_date=order_date)
        order.save()
        order.products.set(products)
        order.total_amount = sum(p.price for p in products)
        order.save()

        return CreateOrder(order=order)

# --- Low Stock Mutation ---
class UpdateLowStockProducts(graphene.Mutation):
    success = graphene.String()
    products = graphene.List(ProductType)

    def mutate(self, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated_products = []

        for product in low_stock_products:
            product.stock += 10
            product.save()
            updated_products.append(product)

        return UpdateLowStockProducts(
            success="Low stock products updated successfully",
            products=updated_products
        )

# --- Single Mutation Class ---
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
    update_low_stock_products = UpdateLowStockProducts.Field()

# --- Query Class ---
class Query(graphene.ObjectType):
    # Non-filtered queries
    customers = graphene.List(CustomerType)
    products = graphene.List(ProductType)
    orders = graphene.List(OrderType)

    # Filtered connection queries
    all_customers = DjangoFilterConnectionField(CustomerType)
    all_products = DjangoFilterConnectionField(ProductType)
    all_orders = DjangoFilterConnectionField(OrderType)

    # Resolvers for non-filtered queries
    def resolve_customers(root, info):
        return Customer.objects.all()

    def resolve_products(root, info):
        return Product.objects.all()

    def resolve_orders(root, info):
        return Order.objects.all()
