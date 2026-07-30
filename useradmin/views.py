from django.shortcuts import render, redirect
from django.contrib import messages
from store.models import Product, Orders, OrderUpdate
from datetime import date
from django.contrib.auth.decorators import login_required, user_passes_test


# Helper to ensure only staff can access the dashboard
def is_staff(user):
    return user.is_staff


@login_required
@user_passes_test(is_staff, login_url='/login/')
def overview_view(request):
    total_products = Product.objects.count()
    total_orders = Orders.objects.count()
    total_revenue = sum(o.amount for o in Orders.objects.all())
    recent_orders = Orders.objects.all().order_by('-order_id')[:5]

    context = {
        'active_tab': 'overview',
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
    }
    return render(request, 'useradmin/overview.html', context)


@login_required
@user_passes_test(is_staff, login_url='/login/')
def add_product_view(request):
    if request.method == 'POST':
        # Safely capture form data
        product_name = (request.POST.get('title') or '').strip()
        description = (request.POST.get('description') or '').strip()
        price_raw = (request.POST.get('price') or '').strip()
        brand = (request.POST.get('brand') or '').strip()
        category = (request.POST.get('category') or '').strip()
        subcategory = (request.POST.get('subcategory') or '').strip()
        image = request.FILES.get('product_image')

        # Server-side validation — every required field is checked here,
        # independent of whatever the browser's own `required` attributes do.
        errors = []

        if not product_name:
            errors.append("Product title is required.")

        if not category:
            errors.append("Category is required.")

        if not brand:
            errors.append("Brand is required.")

        if not image:
            errors.append("A product image is required.")

        price = None
        if not price_raw:
            errors.append("Price is required.")
        else:
            try:
                price = int(float(price_raw))
                if price <= 0:
                    errors.append("Price must be greater than 0.")
            except ValueError:
                errors.append("Price must be a valid number.")

        if errors:
            for error in errors:
                messages.error(request, error)
            # Re-render the form instead of redirecting, so the user
            # doesn't lose everything they already typed.
            # Note: browsers never let a file input's value be
            # re-populated for security reasons, so the chosen image
            # (if any) will need to be re-selected after a validation error.
            return render(request, 'useradmin/add-products.html', {
                'active_tab': 'add_products',
                'old': {
                    'title': product_name,
                    'description': description,
                    'price': price_raw,
                    'brand': brand,
                    'category': category,
                    'subcategory': subcategory,
                },
            })

        # Create and save the new product
        product = Product(
            product_name=product_name,
            description=description,
            price=price,
            brand=brand,
            category=category,
            subcategory=subcategory,
            pub_date=date.today(),
            image=image
        )
        product.save()

        messages.success(request, f"Product '{product_name}' added successfully!")
        return redirect('add_products')

    return render(request, 'useradmin/add-products.html', {'active_tab': 'add_products'})


@login_required
@user_passes_test(is_staff, login_url='/login/')
def reports_view(request):
    return render(request, 'useradmin/reports.html', {'active_tab': 'reports'})


@login_required
@user_passes_test(is_staff, login_url='/login/')
def orders_view(request):
    orders = list(Orders.objects.all().order_by('-order_id'))

    for order in orders:
        latest_update = OrderUpdate.objects.filter(order_id=order.order_id).order_by('-timestamp', '-update_id').first()
        order.latest_status = latest_update.update_desc if latest_update else "No updates yet"

    return render(request, 'useradmin/orders.html', {'active_tab': 'orders', 'orders': orders})