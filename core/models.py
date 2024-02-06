from django.db import models
from shortuuid.django_fields import ShortUUIDField                 # pip install django-shortuuidfield
from django.utils.html import mark_safe
from userauthentication.models import  User
# Create your models here.

STATUS_CHOICE ={
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
}

STATUS ={
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("In_review", "In review"),
    ("published", "Published"),
}

RATING ={
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
    
}




def user_directory_path(instance,filename):
    return 'user_{0}/{1}'.format(instance.user.id,filename)

class Category(models.Model):
    custom_ID = ShortUUIDField(unique=True,length=10,max_length=20,prefix="cat",alphabet="abcedfgh12345")
    title= models.CharField(max_length=100,default="category here")
    image = models.ImageField(upload_to="category",default="category.jpg")

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50">'%(self.image.url))
    
    def __str__(self):
        return self.title
    
# class Tags(models.Model):
#     pass


class Vendor(models.Model):
    Vendor_ID = ShortUUIDField(unique=True,length=10,max_length=20,prefix="ven",alphabet="abcedfgh12345")
    title= models.CharField(max_length=100,default="vendors")
    image = models.ImageField(upload_to=user_directory_path,default="vendor.jpg")

    description = models.TextField(null=True,blank=True)
    address= models.CharField(max_length=100,default="123 Male Street")
    contact= models.CharField(max_length=10,default="56789")
    chat_rep_time= models.CharField(max_length=10,default="100")
    shipping_on_time= models.CharField(max_length=10,default="100")
    authentic_rating= models.CharField(max_length=10,default="100")
    days_return= models.CharField(max_length=10,default="100")
    warranty_period= models.CharField(max_length=10,default="100")
    date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)              #cascade
    


    class Meta:
        verbose_name_plural = "Vendors"

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50">'%(self.image.url))
    
    def __str__(self):
        return self.title

class Product(models.Model):
    P_ID = ShortUUIDField(unique=True,length=10,max_length=20,prefix="prd",alphabet="abcedfgh12345")
    
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)              #cascade 
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name="category")               
    vendor = models.ForeignKey(Vendor,on_delete=models.SET_NULL,null=True,related_name="vendor")               
    
    title= models.CharField(max_length=100,default="Fresh Pears")
    image = models.ImageField(upload_to="category",default="prodcut.jpg")
    description = models.TextField(null=True,blank=True,default="This is the product")

    price = models.DecimalField(max_digits=9999999999999,decimal_places=2,default="1.99")
    old_price = models.DecimalField(max_digits=9999999999999,decimal_places=2,default="2.99")

    specifications = models.TextField(null=True,blank=True)
    stock_count = models.IntegerField(default="10",null=True,blank=True)
    mfd = models.DateField(auto_now_add=False,null=True,blank=True)
    # tags = models.ForeignKey(Tags,on_delete=models.SET_NULL,null=True)

    product_status = models.CharField(choices=STATUS,max_length=10,default="In_review")

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    sku = ShortUUIDField(unique=True,length=4,max_length=10,prefix="sku",alphabet="1234567890")
    
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True,blank=True)

    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50">'%(self.image.url))
    
    def __str__(self):
        return self.title
    

    def get_discount(self):
        new_price = ((self.old_price - self.price) / self.old_price) * 100
        new_price = "{:.0f}".format(new_price) 
        return new_price

class ProductsImages(models.Model):
    images = models.ImageField(upload_to="product-images",default="product.jpg")
    product = models.ForeignKey(Product, related_name="p_images",on_delete=models.SET_NULL,null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product images"

############################## cart, order, orderItems  ##########################
############################## cart, order, orderItems  ##########################
############################## cart, order, orderItems  ##########################
############################## cart, order, orderItems  ##########################


class CartOrder(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9999999999999,decimal_places=2,default="1.99")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE,max_length=30,default="processing")

    class Meta:
        verbose_name_plural = "Cart order"


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder,on_delete=models.CASCADE)
    invoice_no =  models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9999999999999,decimal_places=2,default="1.99")
    total = models.DecimalField(max_digits=9999999999999,decimal_places=2,default="1.99")
   
    class Meta:
        verbose_name_plural = "Cart Order Items"

    def order_img(self):
       return mark_safe('<img src="/media/%s" width="50" height="50">' % (self.image))




############################## Product review  Wishlist Address ##########################
############################## Product review  Wishlist Address ##########################
############################## Product review  Wishlist Address ##########################
############################## Product review  Wishlist Address ##########################

class ProductReview(models.Model):

    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)              #cascade 
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,related_name="review")              #cascade 
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default= None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    


class wishlist_model(models.Model):

    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)              #cascade 
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)              #cascade 
    
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlists"

    def __str__(self):
        return self.product.title
   


class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)              #cascade 
    address = models.CharField(max_length=200,null= True)
    phone_number = models.CharField(max_length=100,null= True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"

    
