from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category, Product, Customer


class ERPAppTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            description='Test category description'
        )

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, '/login/?next=/dashboard/')

    def test_dashboard_with_login(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_product_creation(self):
        product = Product.objects.create(
            name='Test Product',
            description='Test description',
            category=self.category,
            price=29.99,
            cost_price=15.00,
            stock_quantity=100,
            color='Blue',
            brand='TestBrand'
        )
        self.assertEqual(product.name, 'Test Product')
        self.assertTrue(product.profit_margin > 0)

    def test_customer_creation(self):
        customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='+1234567890',
            address='123 Test St',
            city='Test City',
            postal_code='12345',
            gender='M'
        )
        self.assertEqual(customer.full_name, 'John Doe')
        self.assertEqual(customer.email, 'john.doe@example.com')