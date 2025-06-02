from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from erp_app.models import Category, Product, Customer, Sale, SaleItem, Income
from decimal import Decimal
import random
from datetime import datetime, timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = 'Create dummy data for the clothes shop ERP'

    def handle(self, *args, **options):
        self.stdout.write('Creating dummy data...')

        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write('Created admin user (username: admin, password: admin123)')

        # Create categories
        categories_data = [
            {'name': 'T-Shirts', 'description': 'Casual and formal t-shirts'},
            {'name': 'Jeans', 'description': 'Denim jeans for all occasions'},
            {'name': 'Dresses', 'description': 'Elegant dresses for women'},
            {'name': 'Jackets', 'description': 'Warm and stylish jackets'},
            {'name': 'Shoes', 'description': 'Footwear for all seasons'},
            {'name': 'Accessories', 'description': 'Bags, belts, and more'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create products
        products_data = [
            {'name': 'Classic Cotton T-Shirt', 'category': 'T-Shirts', 'price': 25.99, 'cost': 12.50, 'stock': 50,
             'color': 'White', 'brand': 'ComfortWear'},
            {'name': 'Vintage Denim Jacket', 'category': 'Jackets', 'price': 89.99, 'cost': 45.00, 'stock': 25,
             'color': 'Blue', 'brand': 'RetroStyle'},
            {'name': 'Summer Floral Dress', 'category': 'Dresses', 'price': 65.99, 'cost': 32.00, 'stock': 30,
             'color': 'Pink', 'brand': 'FloralFashion'},
            {'name': 'Slim Fit Jeans', 'category': 'Jeans', 'price': 79.99, 'cost': 40.00, 'stock': 40,
             'color': 'Dark Blue', 'brand': 'DenimCo'},
            {'name': 'Running Sneakers', 'category': 'Shoes', 'price': 120.00, 'cost': 60.00, 'stock': 35,
             'color': 'Black', 'brand': 'SportMax'},
            {'name': 'Leather Handbag', 'category': 'Accessories', 'price': 150.00, 'cost': 75.00, 'stock': 20,
             'color': 'Brown', 'brand': 'LuxeBags'},
            {'name': 'Graphic Print Tee', 'category': 'T-Shirts', 'price': 29.99, 'cost': 15.00, 'stock': 60,
             'color': 'Black', 'brand': 'UrbanStyle'},
            {'name': 'High Waist Jeans', 'category': 'Jeans', 'price': 85.99, 'cost': 42.00, 'stock': 35,
             'color': 'Light Blue', 'brand': 'TrendyDenim'},
            {'name': 'Evening Gown', 'category': 'Dresses', 'price': 199.99, 'cost': 100.00, 'stock': 15,
             'color': 'Red', 'brand': 'ElegantWear'},
            {'name': 'Winter Coat', 'category': 'Jackets', 'price': 180.00, 'cost': 90.00, 'stock': 20, 'color': 'Navy',
             'brand': 'WarmWear'},
        ]

        sizes = ['XS', 'S', 'M', 'L', 'XL']

        for prod_data in products_data:
            category = Category.objects.get(name=prod_data['category'])
            for size in random.sample(sizes, random.randint(2, 4)):
                product, created = Product.objects.get_or_create(
                    name=prod_data['name'],
                    size=size,
                    color=prod_data['color'],
                    defaults={
                        'description': f"High quality {prod_data['name'].lower()} in {prod_data['color'].lower()} color",
                        'category': category,
                        'price': Decimal(str(prod_data['price'])),
                        'cost_price': Decimal(str(prod_data['cost'])),
                        'stock_quantity': prod_data['stock'],
                        'brand': prod_data['brand'],
                    }
                )
                if created:
                    self.stdout.write(f'Created product: {product.name} - {product.size}')

        # Create customers
        customers_data = [
            {'first_name': 'Emma', 'last_name': 'Johnson', 'email': 'emma.johnson@email.com', 'phone': '+1234567890',
             'city': 'New York', 'gender': 'F'},
            {'first_name': 'Michael', 'last_name': 'Smith', 'email': 'michael.smith@email.com', 'phone': '+1234567891',
             'city': 'Los Angeles', 'gender': 'M'},
            {'first_name': 'Sarah', 'last_name': 'Davis', 'email': 'sarah.davis@email.com', 'phone': '+1234567892',
             'city': 'Chicago', 'gender': 'F'},
            {'first_name': 'James', 'last_name': 'Wilson', 'email': 'james.wilson@email.com', 'phone': '+1234567893',
             'city': 'Houston', 'gender': 'M'},
            {'first_name': 'Jessica', 'last_name': 'Brown', 'email': 'jessica.brown@email.com', 'phone': '+1234567894',
             'city': 'Phoenix', 'gender': 'F'},
            {'first_name': 'David', 'last_name': 'Miller', 'email': 'david.miller@email.com', 'phone': '+1234567895',
             'city': 'Philadelphia', 'gender': 'M'},
            {'first_name': 'Ashley', 'last_name': 'Garcia', 'email': 'ashley.garcia@email.com', 'phone': '+1234567896',
             'city': 'San Antonio', 'gender': 'F'},
            {'first_name': 'Christopher', 'last_name': 'Martinez', 'email': 'chris.martinez@email.com',
             'phone': '+1234567897', 'city': 'San Diego', 'gender': 'M'},
        ]

        for cust_data in customers_data:
            customer, created = Customer.objects.get_or_create(
                email=cust_data['email'],
                defaults={
                    'first_name': cust_data['first_name'],
                    'last_name': cust_data['last_name'],
                    'phone': cust_data['phone'],
                    'address': f"123 Main Street, Apt {random.randint(1, 100)}",
                    'city': cust_data['city'],
                    'postal_code': f"{random.randint(10000, 99999)}",
                    'gender': cust_data['gender'],
                    'date_of_birth': datetime(1980 + random.randint(0, 30), random.randint(1, 12),
                                              random.randint(1, 28)).date(),
                }
            )
            if created:
                self.stdout.write(f'Created customer: {customer.full_name}')

        # Create sales and income
        admin_user = User.objects.get(username='admin')
        customers = Customer.objects.all()
        products = Product.objects.all()

        for i in range(20):
            # Random date in the last 6 months
            sale_date = timezone.now() - timedelta(days=random.randint(1, 180))
            customer = random.choice(customers)

            sale = Sale.objects.create(
                customer=customer,
                sale_date=sale_date,
                total_amount=Decimal('0.00'),
                payment_method=random.choice(['cash', 'card', 'bank_transfer']),
                created_by=admin_user,
                notes=f"Sale to {customer.full_name}"
            )

            # Add 1-3 items to each sale
            total_amount = Decimal('0.00')
            for j in range(random.randint(1, 3)):
                product = random.choice(products)
                quantity = random.randint(1, 3)
                unit_price = product.price
                item_total = quantity * unit_price

                SaleItem.objects.create(
                    sale=sale,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=item_total
                )

                total_amount += item_total

                # Update product stock
                product.stock_quantity = max(0, product.stock_quantity - quantity)
                product.save()

            sale.total_amount = total_amount
            sale.save()

            # Create corresponding income record
            Income.objects.create(
                title=f"Sale #{sale.id}",
                amount=total_amount,
                income_type='sale',
                date=sale_date.date(),
                description=f"Income from sale to {customer.full_name}",
                sale=sale
            )

        # Create some additional income records
        for i in range(10):
            Income.objects.create(
                title=f"Service Income #{i + 1}",
                amount=Decimal(str(random.uniform(50, 500))),
                income_type='service',
                date=(timezone.now() - timedelta(days=random.randint(1, 90))).date(),
                description="Income from alteration services"
            )

        self.stdout.write(self.style.SUCCESS('Successfully created dummy data!'))
        self.stdout.write('You can now login with username: admin, password: admin123')