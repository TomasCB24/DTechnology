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


# Create your models here.

CATEGORY_CHOICES = (
    ('MB','Motherboard'),
    ('CPU','Processor'),
    ('HDD', 'Hard Disk Drive'),
    ('SSD', 'Solid State Drive'),
    ('GPU', 'Graphic Card'),
    ('RAM','Ram Memory'),
    ('RC', 'DVD/CD Recorder'),
    ('SC','Sound Card'),
    ('CC', 'Computer Cases'),
    ('V', 'Ventilation'),
    ('PS', 'Power Supply'),
    ('MS', 'Mouses'),
    ('KB', 'Keyboards'),
    ('SP','Speakers'),
    ('HP','Headphones'),
    ('GC','Gaming Chairs'),
    ('WC','Webcam'),
    ('PT','Printers'),
    ('GS','Games'),
    ('CS','Consoles'),
    ('CA','Console Accessories'),
    ('CT','Controls')
    
)

DEPARTMENT_CHOICES = (
    ('CM', 'Components'),
    ('PP','Peripherals'),
    ('VG','Consoles and Videogames')
)

PRODUCER_CHOICES = (
    ('AS','Asus'),
    ('LV','Lenovo'),
    ('HP','HP'),
    ('SY','Sony'),
    ('XB','Xbox'),
    ('NT','Nintendo'),
    ('NS','New Skill'),
    ('MSI','MSI'),
    ('PH','Philips'),
    ('GB','Gigabyte'),
    ('EV','Evga'),
    ('NV','Nvidia'),
    ('UB','Ubisoft'),
    ('SM','Santa Monica'),
    ('IT','Intel'),
    ('AMD','AMD'),
    ('ZT','Zotac')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class Product(models.Model):
            
    title = models.CharField(max_length=100)
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    discount_price = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0.0)])
    section = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    description = models.TextField(max_length= 400)
    image = models.URLField()
    department = models.CharField(choices=DEPARTMENT_CHOICES, max_length=10)
    producer = models.CharField(choices=PRODUCER_CHOICES, max_length=10)
    
    def get_price(self):
        return self.price
    
    def clean(self):
        if self.discount_price > self.price:
            raise ValidationError("El descuento tiene que ser menor que el precio original")
 
    
class OrderProduct(models.Model):
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
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
    
    @property
    def stripe_charge_id(self):
        number = random.randint(1000000,9999999)
        return str(self.timestamp.time())+"/"+ str(number) + str(self.purcharse_id)
    
class Address(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(primary_key=True)
    phone = PhoneNumberField(unique = True, null = True, blank = False)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Addresses'

