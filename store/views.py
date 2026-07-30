from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Product, Contact, Orders, OrderUpdate, Wishlist, Review
from django.db.models import Avg, Count
from math import ceil
import json
import uuid
import requests
from django.views.decorators.csrf import csrf_exempt
from .esewa_utils import generate_signature, ESEWA_MERCHANT_CODE, ESEWA_PAYMENT_URL, ESEWA_STATUS_CHECK_URL


def index(request):
    allProds = []
    categories = Product.objects.values_list('category', flat=True).distinct()
    for cat in categories:
        products_in_cat = Product.objects.filter(category=cat).annotate(
            avg_rating=Avg('reviews__rating'), review_count=Count('reviews', distinct=True)
        )
        brands_in_cat = products_in_cat.values_list('brand', flat=True).distinct()
        brand_rows = []
        for brand in brands_in_cat:
            brand_products = products_in_cat.filter(brand=brand)
            brand_rows.append({'brand': brand, 'products': brand_products})
        allProds.append({'category': cat, 'brand_rows': brand_rows})
    return render(request, 'store/index.html', {'allProds': allProds})


def searchMatch(query, item):
    query = query.lower()
    return query in item.description.lower() or query in item.product_name.lower() or query in item.category.lower()


def search(request):
    query = request.GET.get('search', '')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat).annotate(
            avg_rating=Avg('reviews__rating'), review_count=Count('reviews', distinct=True)
        )
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query) < 4:
        params = {'msg': "Please make sure to enter a relevant search query"}
    return render(request, 'store/search.html', params)


def about(request):
    return render(request, 'store/about.html')

def deals(request):
    # Mock deals by grabbing products with ID divisible by 2 (or just a slice) to show variety without DB change
    deals_products = Product.objects.all().annotate(
        avg_rating=Avg('reviews__rating'), review_count=Count('reviews', distinct=True)
    )[:8]
    return render(request, 'store/deals.html', {'products': deals_products})

def new_arrivals(request):
    # Fetch newest products by pub_date
    new_products = Product.objects.order_by('-pub_date').annotate(
        avg_rating=Avg('reviews__rating'), review_count=Count('reviews', distinct=True)
    )[:12]
    return render(request, 'store/new_arrivals.html', {'products': new_products})

def brands(request):
    # Group products by subcategory (acting as brand)
    brands_data = {}
    products = Product.objects.all()
    for prod in products:
        brand = prod.subcategory if prod.subcategory else "Other Brands"
        if brand not in brands_data:
            brands_data[brand] = []
        brands_data[brand].append(prod)
    return render(request, 'store/brands.html', {'brands_data': brands_data})

def support(request):
    return render(request, 'store/support.html')

def category(request, category_name):
    # Fetch products matching the category name
    products = Product.objects.filter(category__iexact=category_name).annotate(
        avg_rating=Avg('reviews__rating'), review_count=Count('reviews', distinct=True)
    )
    return render(request, 'store/category.html', {'products': products, 'category_name': category_name})


def contact(request):
    thank = False
    if request.method == "POST":
        contact = Contact(
            name=request.POST.get('name', ''),
            email=request.POST.get('email', ''),
            phone=request.POST.get('phone', ''),
            desc=request.POST.get('desc', '')
        )
        contact.save()
        thank = True
    return render(request, 'store/contact.html', {'thank': thank})


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = [{'text': item.update_desc, 'time': item.timestamp} for item in update]
                return HttpResponse(
                    json.dumps({"status": "success", "updates": updates, "itemsJson": order[0].items_json},
                               default=str))
            return HttpResponse('{"status":"noitem"}')
        except Exception:
            return HttpResponse('{"status":"error"}')
    return render(request, 'store/tracker.html')


def productView(request, myid):
    product = Product.objects.filter(id=myid).annotate(
        avg_rating=Avg('reviews__rating'), review_count=Count('reviews', distinct=True)
    )
    return render(request, 'store/Productview.html', {'product': product[0]})


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '0')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        current_user = request.user if request.user.is_authenticated else None

        order = Orders(
            user=current_user,
            items_json=items_json,
            name=name,
            email=email,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            phone=phone,
            amount=amount
        )
        order.save()

        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()

        transaction_uuid = f"{order.order_id}-{uuid.uuid4().hex[:8]}"
        total_amount = str(amount)
        product_code = ESEWA_MERCHANT_CODE
        signature = generate_signature(total_amount, transaction_uuid, product_code)

        esewa_data = {
            'amount': total_amount, 'tax_amount': '0', 'total_amount': total_amount,
            'transaction_uuid': transaction_uuid, 'product_code': product_code,
            'product_service_charge': '0', 'product_delivery_charge': '0',
            'success_url': 'http://127.0.0.1:8000/store/esewa/success/',
            'failure_url': 'http://127.0.0.1:8000/store/esewa/failure/',
            'signed_field_names': 'total_amount,transaction_uuid,product_code',
            'signature': signature,
        }
        return render(request, 'store/esewa.html', {'esewa_data': esewa_data, 'esewa_url': ESEWA_PAYMENT_URL})
    return render(request, 'store/checkout.html')


def toggle_wishlist(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'login_required'})
    try:
        product = Product.objects.get(id=product_id)
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        if not created:
            wishlist_item.delete()
            return JsonResponse({'status': 'removed'})
        return JsonResponse({'status': 'added'})
    except Product.DoesNotExist:
        return JsonResponse({'status': 'error'})


@csrf_exempt
def esewa_success(request):
    encoded_data = request.GET.get('data', '')
    import base64
    try:
        decoded = base64.b64decode(encoded_data).decode('utf-8')
        response_data = json.loads(decoded)
    except Exception:
        response_data = {}

    transaction_uuid = response_data.get('transaction_uuid', '')
    total_amount = response_data.get('total_amount', '')
    verify_params = {'product_code': ESEWA_MERCHANT_CODE, 'total_amount': total_amount,
                     'transaction_uuid': transaction_uuid}
    verified_status = None
    try:
        r = requests.get(ESEWA_STATUS_CHECK_URL, params=verify_params, timeout=10)
        if r.status_code == 200: verified_status = r.json()
    except Exception:
        pass

    return render(request, 'store/paymentstatus.html', {'response': response_data, 'verified_status': verified_status})


def esewa_failure(request):
    return render(request, 'store/paymentstatus.html', {'response': {'status': 'FAILED'}, 'verified_status': None})


def reports(request):
    return render(request, 'store/reports.html')