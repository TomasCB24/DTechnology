import uuid
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import (
    DecimalValidator,
    MaxValueValidator,
    MinValueValidator,
    ValidationError,
)
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
import random
from django.core.validators import URLValidator


# Create your models here.

CATEGORY_CHOICES = (
    ('Motherboard','Motherboard'),
    ('Processor','Processor'),
    ('Hard Disk Drive','Hard Disk Drive'),
    ('Solid State Drive','Solid State Drive'),
    ('Graphic Card','Graphic Card'),
    ('Ram Memory','Ram Memory'),
    ('DVD/CD Recorder','DVD/CD Recorder'),
    ('Sound Card','Sound Card'),
    ('Computer Cases','Computer Cases'),
    ('Ventilation','Ventilation'),
    ('Power Supply','Power Supply'),
    ('Mouses','Mouses'),
    ('Keyboards', 'Keyboards'),
    ('Speakers','Speakers'),
    ('Headphones','Headphones'),
    ('Gaming Chairs','Gaming Chairs'),
    ('Webcam','Webcam'),
    ('Printers','Printers'),
    ('Games','Games'),
    ('Consoles','Consoles'),
    ('Console Accessories','Console Accessories'),
    ('Controls','Controls')
    
)

DEPARTMENT_CHOICES = (
    ('Components', 'Components'),
    ('Peripherals','Peripherals'),
    ('Consoles and Videogames','Consoles and Videogames')
)

PRODUCER_CHOICES = (
    ('Asus','Asus'),
    ('Lenovo','Lenovo'),
    ('HP','HP'),
    ('Sony','Sony'),
    ('Xbox','Xbox'),
    ('Nintendo','Nintendo'),
    ('New Skill','New Skill'),
    ('MSI','MSI'),
    ('Philips','Philips'),
    ('Gigabyte','Gigabyte'),
    ('Evga','Evga'),
    ('Nvidia','Nvidia'),
    ('Ubisoft','Ubisoft'),
    ('Santa Monica','Santa Monica'),
    ('Intel','Intel'),
    ('AMD','AMD'),
    ('Zotac','Zotac')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class Product(models.Model):
            
    title = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=20, validators=[MinValueValidator(0.0)])
    discount_price = models.DecimalField(decimal_places=2, max_digits=20,blank=True, null=True, validators=[MinValueValidator(0.0)])
    section = models.CharField(choices=CATEGORY_CHOICES, max_length=30)
    description = models.TextField(max_length= 400)
    image = models.URLField()
    department = models.CharField(choices=DEPARTMENT_CHOICES, max_length=30)
    producer = models.CharField(choices=PRODUCER_CHOICES, max_length=30)
    inventory = models.IntegerField(default=5)

    def save(self, *args, **kwargs):
        self.clean()
        if len(self.title)>100:
            raise ValidationError("El titulo es demasiado largo")
        if self.title is None or self.title=="":
            raise ValidationError("El titulo no puede estar vacio")
        if self.price is None:
            raise ValidationError("El precio no puede estar vacio")
        if self.description is None or self.description=="":
            raise ValidationError("La descripcion no puede estar vacia")
        if self.image is None:
            raise ValidationError("La imagen no puede estar vacia")
        if self.price < 0:
            raise ValidationError("El precio no puede ser negativo")
        if self.discount_price is not None:
            if self.discount_price < 0:
                raise ValidationError("El descuento no puede ser negativo")
        if self.inventory < 0:
            raise ValidationError("El inventario no puede ser negativo")
        categories = [x[0] for x in CATEGORY_CHOICES]
        if self.section not in categories:
            raise ValidationError("La categoria no es valida")
        departments = [x[0] for x in DEPARTMENT_CHOICES]
        if self.department not in departments:
            raise ValidationError("El departamento no es valido")
        producers = [x[0] for x in PRODUCER_CHOICES]
        if self.producer not in producers:
            raise ValidationError("El productor no es valido")
        val = URLValidator()
        val(self.image)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def is_sold_out(self):

        order_products = OrderProduct.objects.filter(product=self)
        total_ordered = 0
        for order_product in order_products:
            total_ordered += order_product.quantity
        if total_ordered >= self.inventory:
            return True
        return False

    def get_stock(self):

        order_products = OrderProduct.objects.filter(product=self)
        total_ordered = 0
        for order_product in order_products:
            total_ordered += order_product.quantity
        return self.inventory - total_ordered 
            

    def get_price(self):
        return self.price
    
    def clean(self):
        if self.discount_price is not None:
            if self.discount_price > self.price:
                raise ValidationError("El descuento tiene que ser menor que el precio original")
class OrderProduct(models.Model):
    session_id = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    
    class Meta:
        unique_together = ('session_id', 'product',)
    
    def __str__(self):
        return f"{self.quantity} of {self.product.title}"
    
    def get_total_product_price(self):
        return self.quantity * self.product.price
    
    def get_total_discount_product_price(self):
        return self.quantity * self.product.discount_price
    
    def get_amount_saved(self):
        return self.get_total_product_price() - self.get_total_discount_product_price()
    
    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount_product_price()
        return self.get_total_product_price()
    
    def add_products(self, quantity):
        self.quantity += quantity
        self.save()
      
class Order(models.Model):       
    
    ref_id = models.AutoField(primary_key=True)
    products = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)

    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_final_price()
        return total
    
    @property
    def ref_code(self):
        number = random.randint(1000000,9999999)
        return str(self.start_date.date())+"/"+ str(number) + str(self.ref_id)
class Payment(models.Model):
    purcharse_id = models.AutoField(primary_key=True)
    amount = models.FloatField(validators=[MinValueValidator(0.0)])
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.amount < 0:
            raise ValidationError("El pago no puede ser negativo")
        super().save(*args, **kwargs)

    
    @property
    def stripe_charge_id(self):
        number = random.randint(1000000,9999999)
        return str(self.timestamp.time())+"/"+ str(number) + str(self.purcharse_id)
class Address(models.Model):
    name = models.CharField(max_length=100, blank=True, null = True)
    surname = models.CharField(max_length=100, blank=True, null = True)
    email = models.EmailField(primary_key=True)
    phone = PhoneNumberField(unique = True, null = True, blank = False)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    

    class Meta:
        verbose_name_plural = 'Addresses'

