from django.http import JsonResponse
from django.shortcuts import render,redirect  # html page render
from core.models import Product,Category,CartOrder,CartOrderItems,wishlist_model,Vendor,ProductReview,Address
from django.template.loader import render_to_string
from django.contrib import messages
from django.db.models import Count, Avg
from django.contrib.auth.decorators import login_required
from core.forms import ProductReviewForm
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.core import serializers

from userauthentication.models import Profile
# Create your views here.
def index(request):    # request paramter is used while form or rendering the html
    products = Product.objects.filter(featured=True).order_by("-id")[:8]
    categories = Category.objects.all()[:2]
    categoriesright=Category.objects.all()[2:]
    # products = Product.objects.filter(featured= True).order_by("-id")
    context={
        "products":products,
        "categories":categories,
        "categoriesright":categoriesright
    }
    return render(request,'core/index.html',context)

def product_list_view(request):    # request paramter is used while form or rendering the html
    # products = Product.objects.all().order_by("-id")
    products = Product.objects.filter(product_status= "published").order_by("-id")
    new_products = Product.objects.filter(product_status= "published").order_by("-id")[:4]
    context={
        "products":products,
        "new_products":new_products,

    }
    return render(request,'core/product_list.html',context)

def category_list_view(request):    # request paramter is used while form or rendering the html
    # products = Product.objects.all().order_by("-id")
    categories = Category.objects.all
    context={
        "categories":categories,

    }
    return render(request,'core/category_list.html',context)

def category_product_list_view(request,custom_ID):

    category  = Category.objects.get(custom_ID = custom_ID)
    products = Product.objects.filter(product_status="published",category=category)
    categories = Category.objects.all
    # vendors = Vendor.objects.all
    context ={
        "category":category,
        "products":products,
        "categories":categories,
        # "vendors":vendors,
    }
    return render(request,'core/category_product_list.html',context)


def vendor_list_view(request):
    vendors = Vendor.objects.all()

    context={
        "vendors": vendors,
    }
    return render(request,'core/vendor_list.html',context)


def product_detail_view(request,P_ID):
    product = Product.objects.get(P_ID = P_ID)
    products = Product.objects.filter(category=product.category).exclude(P_ID=P_ID).order_by("-id")[:8]
    # getting all reviews
    # print(product,products)
    reviews = ProductReview.objects.filter(product=product).order_by("-date")
    
    review_form = ProductReviewForm()
    p_image = product.p_images.all()
    context = {
        "p": product,
        "p_image":p_image,
        "reviews":reviews,
        "products":products,
        "review_form":review_form
    }
    return render(request,'core/product-detail.html',context)

def ajax_add_review(request,P_ID):
    product = Product.objects.get(P_ID = P_ID)
    user = request.user

    review = ProductReview.objects.create(
        user = user,
        product = product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )
    context = {
        "user":user.username,
        'review':request.POST['review'],
        'rating':request.POST['rating'],
        
    }
    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    return JsonResponse(
        {'bool':True,
        'context':context,
        'average_reviews':average_reviews}

    )




def search_view(request):
    query = request.GET.get("q")
    categories = Category.objects.all
    products = Product.objects.filter(title__icontains=query).order_by("-date")
    context={
        "products":products,
        "query":query,
        "categories":categories,
    }
    return render(request,'core/searchProduct.html',context)


def filter_product(request):
    categories = request.GET.getlist('category[]')
    vendors= request.GET.getlist('vendor[]')
    print(categories)
    products = Product.objects.filter(product_status="published").order_by("-id").distinct()
    if len(categories) >0:
        products= products.filter(category__id__in=categories).distinct()

    if len(vendors) >0:
        products= products.filter(vendors__id__in=vendors).distinct()

    context={
        "products": products,
    }  
    data= render_to_string("core/async/product_list.html",context)
    return JsonResponse({"data":data})



def add_to_cart(request):
    
    cart_product = {}

    cart_product[str(request.GET['id'])] = {
        "title": request.GET['title'],
        "qty": request.GET['qty'],
        "price": request.GET['price'],
        "image": request.GET['image'],
        "pid": request.GET['pid'],
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    
    return JsonResponse({"data":request.session['cart_data_obj'],'totalcartitems': len(request.session['cart_data_obj'])})


def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        return render(request, 'core/cart.html',{"cart_data":request.session['cart_data_obj'],'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})
    else:
        messages.warning(request,"Your cart is empty")
        return redirect("core:index")
           


def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj']= cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

   
    context = render_to_string("core/async/cart-list.html",{"cart_data":request.session['cart_data_obj'],'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount} )
    print('working')
    return JsonResponse({"data":context,'totalcartitems': len(request.session['cart_data_obj'])})
  
@login_required
def checkout_view(request):
   
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

       
    try:
        active_address = Address.objects.get(user=request.user,status=True)
    except:
        messages.warning(request,"There are multiple addresses,only one should be ACTIVATED")
        active_address=None
    return render(request,"core/checkout.html",{"cart_data":request.session['cart_data_obj'],'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount,'active_address':active_address})


razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

def payment_view(request):
    cart_total_amount = 0
    amount = 0

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            amount += int(item['qty']) * float(item['price'])

        order = CartOrder.objects.create(
            user=request.user,
            price=amount
        )

        # Create CartOrderItems for the order
        for p_id, item in request.session['cart_data_obj'].items():
            cart_order_items = CartOrderItems.objects.create(
                order=order,
                invoice_no="INVOICE_NO-" + str(order.id),
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=float(item['price']) * float(item['qty']),
            )

    currency = 'INR'

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount * 100,  # Razorpay expects the amount in paise (multiply by 100)
        currency=currency,
        payment_capture='0'
    ))

    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
    invoice_no = "INVOICE_NO-" + str(order.id)  # Use the correct invoice_no value based on your logic

    # Pass payment details to frontend.
    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZORPAY_API_KEY,
        'razorpay_amount': amount * 100,  # Pass the amount in paise to match Razorpay's expectation
        'currency': currency,
        'callback_url': callback_url,
        'invoice_no': invoice_no,
    }

    return render(request, 'core/payment.html', context=context)



# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
    cart_total_amount = 0
    amount = 0

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            amount += int(item['qty']) * float(item['price'])

        order = CartOrder.objects.create(
            user=request.user,
            price=amount
        )

        # Create CartOrderItems for the order
        for p_id, item in request.session['cart_data_obj'].items():
            cart_order_items = CartOrderItems.objects.create(
                order=order,
                invoice_no="INVOICE_NO-" + str(order.id),
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=float(item['price']) * float(item['qty']),
            )

    razorpay_order = razorpay_client.order.create(dict(
        amount=amount * 100,  # Razorpay expects the amount in paise (multiply by 100)
        payment_capture='0'
    ))
    razorpay_order_id = razorpay_order['id']
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = amount
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request, 'core/payment-completed.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'core/payment-failed.html')
            else:
 
                # if signature verification fails.
                return render(request, 'core/payment-failed.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()

@login_required
def customer_dashboard(request):
    orders = CartOrder.objects.filter(user=request.user).order_by("-id")
    address = Address.objects.filter(user = request.user)
    profile= Profile.objects.get(user=request.user)
    if request.method=="POST":
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        new_address = Address.objects.create(
        user= request.user,
        address=address,
        phone_number=mobile,
        )
        messages.success(request,"Address Added Successfully")
        return redirect("core:dashboard")
    context={
        "orders":orders,
        "address":address,
        "profile":profile,
    }
    return render(request,"core/dashboard.html",context)

def order_detail(request,id):
    order = CartOrder.objects.get(user= request.user, id=id)
    products = CartOrderItems.objects.filter(order=order)
    context ={
        "products":products
    }
    return render(request,"core/order-detail.html",context)

def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean":True})
    

@login_required
def wishlist_view(request):
    
    wishlist = wishlist_model.objects.all()
     
    context={
        'w': wishlist,
    }
   
    return render(request,"core/wishlist.html",context)

def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id = product_id)
    context = {}
    
    wishlist_count = wishlist_model.objects.filter(product=product,user=request.user).count()
   
    if wishlist_count >0:
        context= {
            "bool":True
        }
    else:
        new_wishlist = wishlist_model.objects.create(
        product=product,
        user= request.user
        )
    context={
        "bool":True
    }
    return JsonResponse(context)

def remove_wishlist(request):
    pid = request.GET['id']
    wishlist= wishlist_model.objects.filter(user= request.user)

    product = wishlist_model.objects.get(id=pid)
    product.delete()
    context={
        "bool":True,
        "w": wishlist
    }
    wishlist_json = serializers.serialize('json',wishlist)
    data= render_to_string("core/async/wishlist-list.html",context)
    return JsonResponse({"data":data,"w":wishlist_json})







