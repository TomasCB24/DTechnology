# Generated by Django 4.1.2 on 2022-12-08 12:24

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('surname', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('street_address', models.CharField(max_length=100)),
                ('apartment_address', models.CharField(max_length=100)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('payment', models.CharField(choices=[('Contrareembolso', 'Contrareembolso'), ('Online', 'Online')], max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Addresses',
                'unique_together': {('email', 'street_address')},
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('purcharse_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=20, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('section', models.CharField(choices=[('Placa base', 'Placa base'), ('Procesador', 'Procesador'), ('Disco duro mecánico', 'Disco duro mecánico'), ('Disco duro sólido', 'Disco duro sólido'), ('Tarjeta gráfica', 'Tarjeta gráfica'), ('Memoria ram', 'Memoria ram'), ('Grabadora DVD/CD', 'Grabadora DVD'), ('Tarjeta de sonido', 'Tarjeta de sonido'), ('Torres de ordenador', 'Torres de ordenador'), ('Ventilación', 'Ventilación'), ('Alimentación', 'Alimentación'), ('Ratones', 'Ratones'), ('Teclados', 'Teclados'), ('Altavoces', 'Altavoces'), ('Auriculares', 'Auriculares'), ('Sillas gaming', 'Sillas gaming'), ('Cámara web', 'Cámara web'), ('Impresoras', 'Impresoras'), ('Juegos', 'Juegos'), ('Consolas', 'Consolas'), ('Accesorios de Consolas', 'Accesorios de Consolas'), ('Controles', 'Controles')], max_length=30)),
                ('description', models.TextField(max_length=400)),
                ('image', models.URLField()),
                ('department', models.CharField(choices=[('Componentes', 'Componentes'), ('Periféricos', 'Periféricos'), ('Consolas y Videojuegos', 'Consolas y Videojuegos')], max_length=30)),
                ('producer', models.CharField(choices=[('Asus', 'Asus'), ('Lenovo', 'Lenovo'), ('HP', 'HP'), ('Sony', 'Sony'), ('Xbox', 'Xbox'), ('Nintendo', 'Nintendo'), ('New Skill', 'New Skill'), ('MSI', 'MSI'), ('Philips', 'Philips'), ('Gigabyte', 'Gigabyte'), ('Evga', 'Evga'), ('Nvidia', 'Nvidia'), ('Ubisoft', 'Ubisoft'), ('Santa Monica', 'Santa Monica'), ('Intel', 'Intel'), ('AMD', 'AMD'), ('Zotac', 'Zotac')], max_length=30)),
                ('inventory', models.IntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(blank=True, max_length=100, null=True)),
                ('quantity', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Marketplace.product')),
            ],
            options={
                'unique_together': {('session_id', 'product')},
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('ref_id', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('ordered_date', models.DateTimeField(blank=True, null=True)),
                ('ordered', models.BooleanField(default=False)),
                ('being_delivered', models.BooleanField(default=False)),
                ('received', models.BooleanField(default=False)),
                ('random_id', models.IntegerField(default=9380275)),
                ('billing_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='billing_address', to='Marketplace.address')),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Marketplace.payment')),
                ('products', models.ManyToManyField(to='Marketplace.orderproduct')),
                ('shipping_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shipping_address', to='Marketplace.address')),
            ],
        ),
    ]
