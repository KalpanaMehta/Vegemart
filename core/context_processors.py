# core/context_processors.py

from core.models import Category, Vendor,Product,wishlist_model
from django.contrib import messages
def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    product = Product.objects.all()

    
    return {
        "categories": categories,
        "vendors": vendors,
        "product":product,
    }
