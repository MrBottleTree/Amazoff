from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class UserType(models.TextChoices):
    BUYER = 'buyer', 'Buyer'
    SELLER = 'seller', 'Seller'

class Status(models.TextChoices):
    PENDING = 'pending', 'Pending'
    ACCEPTED = 'accepted', 'Accepted'
    REJECTED = 'rejected', 'Rejected'

class category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return f"{self.name}"

class people(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(max_length=254, unique=True, null=False)
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=False)
    user_type = models.CharField(max_length=6, choices=UserType.choices, default=UserType.BUYER)

    def __str__(self):
        return f"{self.user_type} {self.user_name}"
    
class address(models.Model):
    associated_with = models.ForeignKey(people, on_delete=models.CASCADE, related_name="addresses")
    address_id = models.AutoField(primary_key=True)
    street = models.CharField(max_length=50, null=False)
    city = models.CharField(max_length=50, null=False)
    state = models.CharField(max_length=50, null=False)
    zip_code = models.CharField(max_length=10, null=False)
    country = models.CharField(max_length=50, null=False)
    address_type = models.CharField(max_length=6, choices=UserType.choices, default=UserType.BUYER)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.zip_code}, {self.country}"

class orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    status = models.CharField(max_length=8, choices=Status.choices, default=Status.PENDING)
    buyer = models.ForeignKey(people, on_delete=models.CASCADE, related_name="orders_placed")
    shipped_from = models.ForeignKey(address, on_delete=models.CASCADE, related_name="shipped_from")
    shipped_to = models.ForeignKey(address, on_delete=models.CASCADE, related_name="shipped_to")

    def __str__(self):
        return f"{self.order_id}: placed by {self.buyer} on {self.order_date} for ${self.total_amount}"

class company(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    industry = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=254, unique=True, null=False)

    def __str__(self):
        return f"{self.name}"

class product(models.Model):
    seller = models.ForeignKey(people, on_delete=models.CASCADE, related_name="products_sold")
    product_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=10000, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    image = models.ImageField(upload_to='product_images/', null=True)
    company = models.ForeignKey(company, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(category, on_delete=models.CASCADE, related_name="products", null=True)

    def __str__(self):
        return f"{self.title}"

class inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(product, on_delete=models.CASCADE, related_name="inventory")
    quantity = models.IntegerField(null=False)
    address = models.ForeignKey(address, on_delete=models.CASCADE, related_name="inventory")
    associated_with = models.ForeignKey(people, on_delete=models.CASCADE, related_name="inventory")

    def __str__(self):
        return f"Inventory ID {self.inventory_id}: managed by {self.associated_with}"

class review(models.Model):
    review_id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=1000, null=False)
    rating = models.IntegerField(
        null=False,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="reviews")
    buyer = models.ForeignKey('People', on_delete=models.CASCADE, related_name="reviews")
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User {self.buyer} rated {self.product} {self.rating} stars"

class orderdetails(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE, related_name="order_details")
    order = models.ForeignKey(orders, on_delete=models.CASCADE, related_name="order_details")
    quantity = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.product} x {self.quantity}"

class cart(models.Model):
    buyer = models.ForeignKey(people, on_delete=models.CASCADE, related_name="cart")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer}'s cart created on {self.created_date}"

class cartitems(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.product} x {self.quantity}"