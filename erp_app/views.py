from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from .models import Product, Customer, Sale, SaleItem, Income, Category
from .forms import LoginForm, ProductForm, CustomerForm
import json


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'erp_app/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# @login_required
# def dashboard(request):
#     # Calculate metrics
#     today = timezone.now().date()
#     this_month = today.replace(day=1)
#     last_month = (this_month - timedelta(days=1)).replace(day=1)
#     this_week_start = today - timedelta(days=today.weekday())
#
#     # Total earnings this month
#     total_earnings = Income.objects.filter(
#         date__gte=this_month
#     ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
#
#     # Last month earnings for comparison
#     last_month_earnings = Income.objects.filter(
#         date__gte=last_month,
#         date__lt=this_month
#     ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
#
#     # Calculate percentage change
#     if last_month_earnings > 0:
#         earnings_change = ((total_earnings - last_month_earnings) / last_month_earnings) * 100
#     else:
#         earnings_change = 100 if total_earnings > 0 else 0
#
#     # Balance (simplified as total earnings - costs)
#     total_costs = Product.objects.aggregate(
#         total=Sum('cost_price')
#     )['total'] or Decimal('0')
#     balance = total_earnings - (total_costs * Decimal('0.1'))  # Simplified calculation
#
#     # Total sales this week
#     weekly_sales = Sale.objects.filter(
#         sale_date__gte=this_week_start
#     ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0')
#
#     # Recent products
#     recent_products = Product.objects.filter(is_active=True)[:4]
#
#     # Monthly earnings data for chart
#     monthly_data = []
#     for i in range(12):
#         month_start = (this_month - timedelta(days=30 * i)).replace(day=1)
#         month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
#         month_earnings = Income.objects.filter(
#             date__gte=month_start,
#             date__lte=month_end
#         ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
#         monthly_data.append({
#             'month': month_start.strftime('%b'),
#             'earnings': float(month_earnings)
#         })
#
#     monthly_data.reverse()
#
#     # Customer statistics
#     total_customers = Customer.objects.filter(is_active=True).count()
#     new_customers_this_month = Customer.objects.filter(
#         created_at__gte=this_month,
#         is_active=True
#     ).count()
#
#     new_customer_percentage = (new_customers_this_month / total_customers * 100) if total_customers > 0 else 0
#
#     context = {
#         'total_earnings': total_earnings,
#         'earnings_change': float(earnings_change),
#         'balance': balance,
#         'weekly_sales': weekly_sales,
#         'recent_products': recent_products,
#         'monthly_data': json.dumps(monthly_data),
#         'new_customer_percentage': new_customer_percentage,
#         'total_customers': total_customers,
#         'new_customers_this_month': new_customers_this_month,
#     }
#
#     return render(request, 'erp_app/dashboard.html', context)


@login_required
def products(request):
    search_query = request.GET.get('search', '')
    products = Product.objects.filter(is_active=True)

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    products = products.order_by('-created_at')

    context = {
        'products': products,
        'search_query': search_query,
    }

    return render(request, 'erp_app/products.html', context)


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('products')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()

    return render(request, 'erp_app/add_product.html', {'form': form})


@login_required
def customers(request):
    search_query = request.GET.get('search', '')
    customers = Customer.objects.filter(is_active=True)

    if search_query:
        customers = customers.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )

    customers = customers.order_by('-created_at')

    context = {
        'customers': customers,
        'search_query': search_query,
    }

    return render(request, 'erp_app/customers.html', context)


@login_required
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer added successfully!')
            return redirect('customers')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomerForm()

    return render(request, 'erp_app/add_customer.html', {'form': form})


# @login_required
# def income(request):
#     # Get income data
#     incomes = Income.objects.all().order_by('-date')
#
#     # Calculate totals
#     total_income = incomes.aggregate(total=Sum('amount'))['total'] or Decimal('0')
#
#     # Monthly income data
#     today = timezone.now().date()
#     this_month = today.replace(day=1)
#
#     monthly_income = []
#     for i in range(12):
#         month_start = (this_month - timedelta(days=30 * i)).replace(day=1)
#         month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
#         month_total = Income.objects.filter(
#             date__gte=month_start,
#             date__lte=month_end
#         ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
#
#         monthly_income.append({
#             'month': month_start.strftime('%B %Y'),
#             'total': month_total
#         })
#
#     monthly_income.reverse()
#
#     context = {
#         'incomes': incomes,
#         'total_income': total_income,
#         'monthly_income': monthly_income,
#     }
#
#     return render(request, 'erp_app/income.html', context)
#

@login_required
def help_view(request):
    return render(request, 'erp_app/help.html')


@login_required
def dashboard(request):
    from decimal import Decimal

    # Calculate metrics
    today = timezone.now().date()
    this_month = today.replace(day=1)
    last_month = (this_month - timedelta(days=1)).replace(day=1)
    this_week_start = today - timedelta(days=today.weekday())

    # Total earnings this month
    total_earnings = Income.objects.filter(
        date__gte=this_month
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    # Last month earnings for comparison
    last_month_earnings = Income.objects.filter(
        date__gte=last_month,
        date__lt=this_month
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    # Calculate percentage change
    if last_month_earnings > 0:
        earnings_change = float(((total_earnings - last_month_earnings) / last_month_earnings) * 100)
    else:
        earnings_change = 100.0 if total_earnings > 0 else 0.0

    # Balance (simplified as total earnings - costs)
    total_costs = Product.objects.aggregate(
        total=Sum('cost_price')
    )['total'] or Decimal('0')
    balance = total_earnings - (total_costs * Decimal('0.1'))  # Simplified calculation

    # Total sales this week
    weekly_sales = Sale.objects.filter(
        sale_date__gte=this_week_start
    ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0')

    # Recent products
    recent_products = Product.objects.filter(is_active=True)[:4]

    # Monthly earnings data for chart (last 12 months)
    monthly_data = []
    for i in range(11, -1, -1):  # Start from 11 months ago to current month
        if i == 0:
            month_start = this_month
        else:
            # Calculate month start by going back i months
            year = this_month.year
            month = this_month.month - i
            while month <= 0:
                month += 12
                year -= 1
            month_start = this_month.replace(year=year, month=month, day=1)

        # Calculate month end
        if month_start.month == 12:
            month_end = month_start.replace(year=month_start.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            month_end = month_start.replace(month=month_start.month + 1, day=1) - timedelta(days=1)

        month_earnings = Income.objects.filter(
            date__gte=month_start,
            date__lte=month_end
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

        monthly_data.append({
            'month': month_start.strftime('%b'),
            'earnings': float(month_earnings)
        })

    # Customer statistics
    total_customers = Customer.objects.filter(is_active=True).count()
    new_customers_this_month = Customer.objects.filter(
        created_at__gte=this_month,
        is_active=True
    ).count()

    new_customer_percentage = (new_customers_this_month / total_customers * 100) if total_customers > 0 else 0

    context = {
        'total_earnings': float(total_earnings),
        'earnings_change': earnings_change,
        'balance': float(balance),
        'weekly_sales': float(weekly_sales),
        'recent_products': recent_products,
        'monthly_data': json.dumps(monthly_data),
        'new_customer_percentage': new_customer_percentage,
        'total_customers': total_customers,
        'new_customers_this_month': new_customers_this_month,
    }

    return render(request, 'erp_app/dashboard.html', context)


@login_required
def income(request):
    from decimal import Decimal

    # Get income data
    incomes = Income.objects.all().order_by('-date')[:50]  # Limit to 50 records

    # Calculate totals
    total_income = Income.objects.aggregate(total=Sum('amount'))['total'] or Decimal('0')

    # Monthly income data (last 12 months)
    today = timezone.now().date()
    this_month = today.replace(day=1)

    monthly_income = []
    for i in range(11, -1, -1):  # Start from 11 months ago to current month
        if i == 0:
            month_start = this_month
        else:
            # Calculate month start by going back i months
            year = this_month.year
            month = this_month.month - i
            while month <= 0:
                month += 12
                year -= 1
            month_start = this_month.replace(year=year, month=month, day=1)

        # Calculate month end
        if month_start.month == 12:
            month_end = month_start.replace(year=month_start.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            month_end = month_start.replace(month=month_start.month + 1, day=1) - timedelta(days=1)

        month_total = Income.objects.filter(
            date__gte=month_start,
            date__lte=month_end
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

        monthly_income.append({
            'month': month_start.strftime('%B %Y'),
            'total': float(month_total)
        })

    context = {
        'incomes': incomes,
        'total_income': float(total_income),
        'monthly_income': monthly_income,
        'this_month_income': monthly_income[-1]['total'] if monthly_income else 0,
    }

    return render(request, 'erp_app/income.html', context)