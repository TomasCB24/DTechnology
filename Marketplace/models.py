import uuid
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image
from io import BytesIO
from django import forms

from django.core.validators import (
    DecimalValidator,
    MaxValueValidator,
    MinValueValidator,
    ValidationError,
    EmailValidator,
    MaxLengthValidator,
    RegexValidator,
)
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
import random
from django.core.validators import URLValidator
import requests
import urllib3


# Create your models here.
PAYMENT_METHODS = (
    ('Contrareembolso', 'Contrareembolso'),
    ('Online', 'Online'),
)


CATEGORY_CHOICES = (
    ('Placa base','Placa base'),
    ('Procesador','Procesador'),
    ('Disco duro mecánico','Disco duro mecánico'),
    ('Disco duro sólido','Disco duro sólido'),
    ('Tarjeta gráfica','Tarjeta gráfica'),
    ('Memoria ram','Memoria ram'),
    ('Grabadora DVD/CD','Grabadora DVD'),
    ('Tarjeta de sonido','Tarjeta de sonido'),
    ('Torres de ordenador','Torres de ordenador'),
    ('Ventilación','Ventilación'),
    ('Alimentación','Alimentación'),
    ('Ratones','Ratones'),
    ('Teclados', 'Teclados'),
    ('Altavoces','Altavoces'),
    ('Auriculares','Auriculares'),
    ('Sillas gaming','Sillas gaming'),
    ('Cámara web','Cámara web'),
    ('Impresoras','Impresoras'),
    ('Juegos','Juegos'),
    ('Consolas','Consolas'),
    ('Accesorios de Consolas','Accesorios de Consolas'),
    ('Controles','Controles')
    
)

DEPARTMENT_CHOICES = (
    ('Componentes', 'Componentes'),
    ('Periféricos','Periféricos'),
    ('Consolas y Videojuegos','Consolas y Videojuegos')
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

def validate_image_quality(value):
    MIN_HEIGHT = 720
    MIN_WIDTH = 720
    try:
        response = requests.get(value, timeout=10)
        try:
            picture  = Image.open(BytesIO(response.content))
            width, height = picture.size
            if width < MIN_WIDTH or height < MIN_HEIGHT:
                raise ValidationError("La imagen no cumple con el requisito de calidad. Debe ser mayor que " + str(MIN_WIDTH) + " de ancho x " + str(MIN_HEIGHT) + " de alto y la actual es de " + str(width) + " de ancho x "+str(height)+" de alto.")
            else:
                return value
        except OSError:
            raise ValidationError("La URL proporcionada no es una imagen válida. Intente de nuevo proporcionando una URL válida diferente.")
    except requests.exceptions.Timeout:
        raise ValidationError("No se ha podido acceder a la imagen en el tiempo requerido. Intente de nuevo proporcionando una URL válida diferente.")

class Product(models.Model):
            
    title = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=20, validators=[MinValueValidator(0.0)])
    discount_price = models.DecimalField(decimal_places=2, max_digits=20,blank=True, null=True, validators=[MinValueValidator(0.0)])
    section = models.CharField(choices=CATEGORY_CHOICES, max_length=30)
    description = models.TextField(max_length= 400)
    image = models.URLField(validators=[URLValidator(), validate_image_quality])
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
        if self.discount_price is not None and self.discount_price < 0:
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



    def get_stock(self):

        order_products = OrderProduct.objects.filter(product=self).filter(ordered=False)
        total_ordered = 0
        for order_product in order_products:
            total_ordered += order_product.quantity
        return self.inventory - total_ordered 
            
    def is_sold_out(self):

        stock = self.get_stock()
        if stock <= 0:
            return True
        return False
            
    def get_price(self):
        return self.price

    def get_actual_price(self):
        if self.discount_price is not None:
            return self.discount_price
        return self.price
    
    def clean(self):
        if self.discount_price is not None and self.discount_price > self.price:
                raise ValidationError("El descuento tiene que ser menor que el precio original")
class OrderProduct(models.Model):
    session_id = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    ordered = models.BooleanField(default=False)
    
    
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
    
    def save(self, *args, **kwargs):
        if self.quantity is None:
            raise ValueError('La cantidad no puede estar vacía')
        if self.quantity <= 0:
            raise ValueError('La cantidad no puede ser negativa')
        if self.session_id is None:
            raise ValueError('El id de la sesión no puede estar vacío')
        if self.session_id == '':
            raise ValueError('El id de la sesión no puede estar vacío')
        if len(self.session_id)>100:
            raise ValueError('El id de la sesión no puede tener más de 100 caracteres')
        if hasattr(self, 'product') is False:
            raise ValueError('El producto no puede ser nulo')
        super().save(*args, **kwargs)
      
class Order(models.Model):       
    
    ref_id = models.AutoField(primary_key=True)
    products = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)

    random_id =models.IntegerField(default=random.randint(1000000,9999999))

    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_final_price()
        return total
    
    @property
    def ref_code(self):
        return str(self.start_date.date())+"/"+ str(self.random_id) + str(self.ref_id)

    def __str__(self):
        return self.ref_code


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
    email = models.EmailField()
    phone = PhoneNumberField( null = True, blank = True)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField()
    payment = models.CharField(choices=PAYMENT_METHODS, max_length=50)

    def save(self, *args, **kwargs):
        val1 = EmailValidator()
        val1(self.email)
        # TODO: validar el número de teléfono sólo en caso de no ser nulo o vacío
        # val2 = RegexValidator(regex='^(\+34|0034|34)?[ -]*(6|7)[ -]*([0-9][ -]*){8}$')
        # val2(self.phone)
        val3 = MaxLengthValidator(100)
        val3(self.name)
        val3(self.surname)
        val3(self.street_address)
        val3(self.apartment_address)
        val4 = MaxLengthValidator(50)
        val4(self.payment)

        if self.payment != 'Contrareembolso' and self.payment != 'Online':
            raise ValidationError("El tipo de pago no es válido, debe ser Contrareembolso u Online")

        super(Address, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.email + " " + self.street_address

    class Meta:
        verbose_name_plural = 'Addresses'
        unique_together = (('email', 'street_address'),)  

    def get_address(self):
        return f"{self.street_address}, {self.apartment_address}, {self.country}"

