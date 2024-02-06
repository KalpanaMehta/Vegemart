from django.urls import path,include
from core import views
app_name = "core"
urlpatterns = [
    path('',views.index,name = "index"),
    path('products/',views.product_list_view,name = "product_list"),
    path('product/<P_ID>/',views.product_detail_view,name = "product-detail"),


    path('category/',views.category_list_view,name = "category_list"),
    path('category/<custom_ID>/',views.category_product_list_view,name = "category_product_list"),
    path('vendor/',views.vendor_list_view,name = "vendor-list"),
  
   #  ADd reviews

   path('ajax-add-review/<int:PID>',views.ajax_add_review,name = "ajax-add-review"),

    path('search/',views.search_view,name = "search"),


    path('filter-products/',views.filter_product,name = "filter-product"),


    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),

    path('cart/', views.cart_view, name='cart'),

    path('delete-from-cart/', views.delete_item_from_cart, name='delete-from-cart'),

    path('checkout/', views.checkout_view, name='checkout'),
    path('payment/', views.payment_view, name='payment'),

   path('paymenthandler/', views.paymenthandler, name='paymenthandler'),

#    dashboard 

   path('dashboard/', views.customer_dashboard, name='dashboard'),
   path('dashboard/order/<int:id>', views.order_detail, name='order-detail'),
  
   path("make-default-address/",views.make_address_default,name="make-default-address"),

   path('wishlist/', views.wishlist_view, name='wishlist'),

   path('add-to-wishlist/', views.add_to_wishlist, name='add-to-wishlist'),
  
   path('remove-from-wishlist/', views.remove_wishlist, name='remove-from-wishlist'),
   





    
   
  
]