from django.test import TestCase
from Marketplace.models import Product, OrderProduct, Order, Payment, Address
from datetime import datetime, timezone

# Create your tests here.

class OrderTestCase(TestCase):

    def setUp(self):

        PRODUCT_IMAGE = "https://cdn-icons-png.flaticon.com/512/1554/1554591.png"
        product_1 = Product.objects.create(title="Producto 1", price=100, section="Ratones", description="Descripción 1", image=PRODUCT_IMAGE, department="Componentes", producer="Asus", inventory=10)
        product_2 = Product.objects.create(title="Producto 2", price=100, section="Ratones", description="Descripción 2", image=PRODUCT_IMAGE, department="Componentes", producer="Asus", inventory=10)
        product_3 = Product.objects.create(title="Producto 3", price=100, section="Ratones", description="Descripción 3", image=PRODUCT_IMAGE, department="Componentes", producer="Asus", inventory=10)

        order_p_1 = OrderProduct.objects.create(session_id="123", product=product_1, quantity=1)
        order_p_2 = OrderProduct.objects.create(session_id="123", product=product_2, quantity=2)
        order_p_3 = OrderProduct.objects.create(session_id="123", product=product_3, quantity=3)
        order_p_4 = OrderProduct.objects.create(session_id="124", product=product_1, quantity=4)
        order_p_5 = OrderProduct.objects.create(session_id="124", product=product_2, quantity=5)
        order_p_6 = OrderProduct.objects.create(session_id="124", product=product_3, quantity=6)

        order_1 = Order.objects.create(ordered_date="2021-05-01")
        order_2 = Order.objects.create(ordered_date="2021-05-02")

        order_1.products.add(order_p_1, order_p_2, order_p_3)
        order_2.products.add(order_p_4, order_p_5, order_p_6)

    def test_order_create(self):
        order = Order.objects.get(ref_id=1)
        self.assertIsNotNone(order)
        self.assertEqual(order.get_total(), 600)
        self.assertEqual(order.ordered_date, datetime(2021,5,1,0,0,0,0,timezone.utc))
        self.assertEqual(order.products.count(), 3)
        order = Order.objects.get(ref_id=2)
        self.assertIsNotNone(order)
        self.assertEqual(order.get_total(), 1500)
        self.assertEqual(order.ordered_date, datetime(2021,5,2,0,0,0,0,timezone.utc))
        self.assertEqual(order.products.count(), 3)


    def test_order_delete(self):
        
        order = Order.objects.get(ref_id=2)
        self.assertIsNotNone(order)

        order.delete()
        self.assertEqual(Order.objects.count(), 1)

    def test_order_update(self):

        product_1 = Product.objects.get(id=1)
        product_2 = Product.objects.get(id=2)

        product_1.price = 200
        product_2.price = 200

        product_1.save()
        product_2.save()

        order_product_1 = OrderProduct.objects.get(id=1)
        order_product_2 = OrderProduct.objects.get(id=2)
        order_product_3 = OrderProduct.objects.get(id=3)

        order_product_1.quantity = 2
        order_product_2.quantity = 2

        order_product_1.save()
        order_product_2.save()

        order = Order.objects.get(ref_id=1)
        self.assertIsNotNone(order)

        order.ordered_date = datetime(2021,5,3,0,0,0,0,timezone.utc)
        order.products.remove(order_product_3)
        order.save()

        self.assertEqual(order.get_total(), 800)
        self.assertEqual(order.ordered_date, datetime(2021,5,3,0,0,0,0,timezone.utc))
        self.assertEqual(order.products.count(), 2)

class OrderProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(title="titlePrueba", description="description", price=4.89, discount_price=3, section="Placa base", image="https://www.google.com", department="Componentes", producer="Nvidia", inventory=5)
        Product.objects.create(title="titlePrueba2", description="description2", price=4.89, discount_price=3, section="Placa base", image="https://www.google.com", department="Componentes", producer="Nvidia", inventory=5)
        product = Product.objects.get(title="titlePrueba")
        self.order_product = OrderProduct.objects.create(session_id="36794cfc-f122-401a-bfb5-47b27d772708", product=product, quantity=2)
    
    def test_order_product_create(self):
        order_product = self.order_product
        self.assertEqual(order_product.quantity, 2)
        self.assertEqual(order_product.product.title, "titlePrueba")
    
    def test_order_product_delete(self):
        order_product = self.order_product
        order_product.delete()
        self.assertEqual(OrderProduct.objects.count(), 0)
    
    def test_order_product_update(self):
        order_product = self.order_product
        order_product.quantity = 3
        product2 = Product.objects.get(title="titlePrueba2")
        order_product.product = product2
        self.assertEqual(order_product.quantity, 3)
        self.assertEqual(order_product.product.title, "titlePrueba2")
    
    #Create test:
    def test_order_product_create_quantity_incorrect(self):
        with self.assertRaises(ValueError):
            order_product= OrderProduct(session_id="36794cfc-f122-401a-bfb5-47b27d772708", product=Product.objects.get(title="titlePrueba"), quantity=-1)
            order_product.save()
    
    def test_order_product_create_quantity_null(self):
        with self.assertRaises(ValueError):
            order_product= OrderProduct(session_id="36794cfc-f122-401a-bfb5-47b27d772708", product=Product.objects.get(title="titlePrueba"), quantity=None)
            order_product.save()
    
    def test_order_product_create_session_id_incorrect(self):
        with self.assertRaises(ValueError):
            order_product= OrderProduct(session_id="36794cfc-f122-401a-bfb5-47b27d77270836794cfc-f122-401a-bfb5-47b27d77270836794cfc-f122-401a-bfb5-47b27d77270836794cfc-f122-401a-bfb5-47b27d77270836794cfc-f122-401a-bfb5-47b27d77270836794cfc-f122-401a-bfb5-47b27d77270836794cfc-f122-401a-bfb5-47b27d77270836794cfc-f122-401a-bfb5-47b27d77270836794cfc-f122-401a-bfb5-47b27d77270836794cfc-f122-401a-bfb5-47b27d772708", product=Product.objects.get(title="titlePrueba"), quantity=1)
            order_product.save()
    
    def test_order_product_create_session_id_null(self):
        with self.assertRaises(ValueError):
            order_product= OrderProduct(session_id=None, product=Product.objects.get(title="titlePrueba"), quantity=1)
            order_product.save()
    
    def test_order_product_create_product_null(self):
        with self.assertRaises(ValueError):
            order_product= OrderProduct(session_id="36794cfc-f122-401a-bfb5-47b27d772708", product=None, quantity=1)
            order_product.save()
    
    #Update test:
    def test_order_product_update_quantity_incorrect(self):
        with self.assertRaises(ValueError):
            order_product= self.order_product
            order_product.quantity=-1
            order_product.save()
    
    def test_order_product_update_quantity_null(self):
        with self.assertRaises(ValueError):
            order_product= self.order_product
            order_product.quantity=None
            order_product.save()

    def test_order_product_update_session_id_incorrect(self):
        with self.assertRaises(ValueError):
            order_product= self.order_product
            order_product.session_id="36794cfc-f122-401a-bfb5-47b27d77270836794cfc-f122-401a-bfb5-47b27d77270836794cfc-f122-401a-bfb5-47b27d77270836794cfc-f122-401a-bfb5-47b27d77270836794cfc-f122-401a-bfb5-47b27d77270836794cfc-f122-401a-bfb5-47b27d77270836794cfc-f122-401a-bfb5-47b27d77270836794cfc-f122-401a-bfb5-47b27d77270836794cfc-f122-401a-bfb5-47b27d772708"
            order_product.save()
        
    def test_order_product_update_session_id_null(self):
        with self.assertRaises(ValueError):
            order_product= self.order_product
            order_product.session_id=None
            order_product.save()
    
    def test_order_product_update_product_null(self):
        with self.assertRaises(ValueError):
            order_product= self.order_product
            order_product.product=None
            order_product.save()


class AddressTestCase(TestCase):

    def setUp(self):
        Address.objects.create(name="Jesús",surname="Luque", email="jluque@gmail.com", phone="678985456", street_address="Avda. Reina Mercedes - 51", apartment_address="1º A", country="ES", payment="Contrareembolso")
        Address.objects.create(name="Marcos",surname="Torrecilla", email="marcost@gmail.com", phone="654875695", street_address="Avda. Reina Mercedes - 27", apartment_address="6º B", country="ES", payment="Online")

    def test_address_create(self):
        address = Address.objects.get(email = "jluque@gmail.com")
        self.assertIsNotNone(address)
        self.assertEqual(address.name,"Jesús")
        self.assertEqual(address.surname,"Luque")
        self.assertEqual(address.email,"jluque@gmail.com")
        self.assertEqual(address.phone,"678985456")
        self.assertEqual(address.street_address,"Avda. Reina Mercedes - 51")
        self.assertEqual(address.apartment_address,"1º A")
        self.assertEqual(address.country,"ES")
        self.assertEqual(address.payment,"Contrareembolso")

    def test_address_delete(self):
        address = Address.objects.get(email = "jluque@gmail.com")
        address.delete()
        self.assertEqual(1,Address.objects.count())

    def test_address_update(self):
        address = Address.objects.get(email = "jluque@gmail.com")
        address.name = "Prueba"
        address.surname = "Prueba"
        address.email = "prueba@gmail.com"
        address.phone = "654987321"
        address.street_address = "Calle Prueba - 1"
        address.apartment_address = "2º C"
        address.country = "FR"
        address.payment = "Online"
        address.save()
        new_address = Address.objects.get(email = "prueba@gmail.com")
        self.assertIsNotNone(new_address)
        self.assertEqual(new_address.name,"Prueba")
        self.assertEqual(new_address.surname,"Prueba")
        self.assertEqual(new_address.email,"prueba@gmail.com")
        self.assertEqual(new_address.phone,"654987321")
        self.assertEqual(new_address.street_address,"Calle Prueba - 1")
        self.assertEqual(new_address.apartment_address,"2º C")
        self.assertEqual(new_address.country,"FR")
        self.assertEqual(new_address.payment,"Online")

    #Create tests

    def test_address_create_name_incorrect(self):
        with self.assertRaises(Exception):
            Address.objects.create(name="Nombrenombrenombrenombrenombrenombrenombrenombrenombrenombrenombrenombrenombrenombrenombrenombrenombr", surname="Luque", email="joseluque@gmail.com", phone="672299956", street_address="Avda. Reina Mercedes - 59", apartment_address="5º D", country="ES", payment="Online")

    def test_address_create_surname_incorrect(self):
        with self.assertRaises(Exception):
            Address.objects.create(name="José", surname="Apellidoapellidoapellidoapellidoapellidoapellidoapellidoapellidoapellidoapellidoapellidoapellidoapell", email="joseluque@gmail.com", phone="672299956", street_address="Avda. Reina Mercedes - 59", apartment_address="5º D", country="ES", payment="Online")

    def test_address_create_street_address_incorrect(self):
        with self.assertRaises(Exception):
            Address.objects.create(name="José", surname="Luque", email="joseluque@gmail.com", phone="672299956", street_address="Direccióndireccióndireccióndireccióndireccióndireccióndireccióndireccióndireccióndireccióndireccióndi", apartment_address="5º D", country="ES", payment="Online")

    def test_address_create_apartment_address_incorrect(self):
        with self.assertRaises(Exception):
            Address.objects.create(name="José", surname="Luque", email="joseluque@gmail.com", phone="672299956", street_address="Avda. Reina Merceder - 59", apartment_address="Direccióndireccióndireccióndireccióndireccióndireccióndireccióndireccióndireccióndireccióndireccióndi", country="ES", payment="Online")

    def test_address_create_email_incorrect(self):
        with self.assertRaises(Exception):
            Address.objects.create(name="José", surname="Luque", email="joseluquegmail.com", phone="672299956", street_address="Avda. Reina Mercedes - 59", apartment_address="5º D", country="ES", payment="Online")

    def test_address_create_payment_blank(self):
        with self.assertRaises(Exception):
            Address.objects.create(name="José", surname="Luque", email="joseluque@gmail.com", phone="672299956", street_address="Avda. Reina Mercedes - 59", apartment_address="5º D", country="España", payment="")

    def test_address_create_payment_incorrect(self):
        with self.assertRaises(Exception):
            Address.objects.create(name="José", surname="Luque", email="joseluque@gmail.com", phone="672299956", street_address="Avda. Reina Mercedes - 59", apartment_address="5º D", country="España", payment="Tarjeta")

    #Update tests
    

    def test_address_update_name_incorrect(self):
        with self.assertRaises(Exception):
            address = Address.objects.get(email = "jluque@gmail.com")
            address.name = "Nombrenombrenombrenombrenombrenombrenombrenombrenombrenombrenombrenombrenombrenombrenombrenombrenombr"
            address.save()

    def test_address_update_surname_incorrect(self):
        with self.assertRaises(Exception):
            address = Address.objects.get(email = "jluque@gmail.com")
            address.surname = "Apellidoapellidoapellidoapellidoapellidoapellidoapellidoapellidoapellidoapellidoapellidoapellidoapell"
            address.save()
    
    def test_address_update_street_address_incorrect(self):
        with self.assertRaises(Exception):
            address = Address.objects.get(email = "jluque@gmail.com")
            address.street_address = "Direccióndireccióndireccióndireccióndireccióndireccióndireccióndireccióndireccióndireccióndireccióndi"
            address.save()
    
    def test_address_update_apartment_address_incorrect(self):
        with self.assertRaises(Exception):
            address = Address.objects.get(email = "jluque@gmail.com")
            address.apartment_address = "Direccióndireccióndireccióndireccióndireccióndireccióndireccióndireccióndireccióndireccióndireccióndi"
            address.save()

    def test_address_update_email_incorrect(self):
        with self.assertRaises(Exception):
            address = Address.objects.get(email = "jluque@gmail.com")
            address.email = "jluquegmail.com"
            address.save()

    def test_address_update_address_type_blank(self):
        with self.assertRaises(Exception):
            address = Address.objects.get(email = "jluque@gmail.com")
            address.payment = ""
            address.save()
    
    def test_address_update_address_type_incorrect(self):
        with self.assertRaises(Exception):
            address = Address.objects.get(email = "jluque@gmail.com")
            address.payment = "Shipping"
            address.save()

class PaymentTestCase(TestCase):
    def setUp(self):
        self.payment = Payment.objects.create(amount=3.00)
    
    def test_payment_create(self):
        payment = self.payment
        self.assertEqual(payment.amount, 3.00)
    
    def test_payment_update(self):
        payment = self.payment
        payment.amount = 4.00
        payment.save()
        self.assertEqual(payment.amount, 4.00)
    
    def test_payment_delete(self):
        payment = self.payment
        payment.delete()
        self.assertEqual(Payment.objects.count(), 0)
    
    #create test

    def test_payment_create_amount_incorrect(self):
        with self.assertRaises(Exception):
            Payment.objects.create(amount=-1)
    
    def test_payment_create_amount_null(self):
        with self.assertRaises(Exception):
            Payment.objects.create()
    
    #update test
    def test_payment_update_amount_incorrect(self):
        payment = self.payment
        with self.assertRaises(Exception):
            payment.amount = -1
            payment.save()
    
    def test_payment_update_amount_null(self):
        payment = self.payment
        with self.assertRaises(Exception):
            payment.amount = None
            payment.save()

class ProductTestCase(TestCase):
    def setUp(self):
        self.product1 = Product.objects.create(title='test', price=1, inventory=1, description='test', section='Placa base', department='Componentes', producer='Asus', image="https://www.google.com")
        self.product2 = Product.objects.create(title='testUpdate', price=1, inventory=1, description='test', section='Placa base', department='Componentes', producer='Asus', image="https://www.google.com")
        
    def test_product_create(self):
        product = self.product1
        self.assertEqual(product.title, 'test')
        self.assertEqual(product.price, 1)
        self.assertEqual(product.inventory, 1)
        self.assertEqual(product.description, 'test')
        self.assertEqual(product.section, 'Placa base')
        self.assertEqual(product.department, 'Componentes')
        self.assertEqual(product.producer, 'Asus')
    
    def test_product_update(self):
        product = self.product2
        product.title = 'testUpdate2'
        product.description = 'testUpdate2'
        product.price = 2
        product.inventory = 2
        product.section = 'Teclados'
        product.department = 'Componentes'
        product.producer = 'Intel'
        product.save()
        self.assertEqual(product.title, 'testUpdate2')
        self.assertEqual(product.price, 2)
        self.assertEqual(product.inventory, 2)
        self.assertEqual(product.description, 'testUpdate2')
        self.assertEqual(product.section, 'Teclados')
        self.assertEqual(product.department, 'Componentes')
        self.assertEqual(product.producer, 'Intel')

    def test_product_delete(self):
        product = self.product1
        product.delete()
        product = self.product2
        product.delete()
        self.assertEqual(len(Product.objects.all()), 0)

    #create test:
    def test_product_create_title_incorrect(self):
        with self.assertRaises(Exception): 
            Product.objects.create(title='AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', price=1, inventory=1, description='test', section='Placa base', department='Componentes', producer='Asus', image="https://www.google.com")
    
    def test_product_create_title_null(self):
        with self.assertRaises(Exception):
            Product.objects.create(price=1, inventory=1, description='test', section='Placa base', department='Componentes', producer='Asus', image="https://www.google.com")
    def test_product_create_price_incorrect(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', price=-1, inventory=1, description='test', section='Placa base', department='Componentes', producer='Asus', image="https://www.google.com")
   
    def test_product_create_price_null(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', inventory=1, description='test', section='Placa base', department='Componentes', producer='Asus', image="https://www.google.com")
   
    def test_product_create_discount_price_negative(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', price=1, discount_price=-1, inventory=1, description='test', section='Placa base', department='Componentes', producer='Asus', image="https://www.google.com")

    def test_product_create_discount_price_greater_than_price(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', price=1, discount_price=2, inventory=1, description='test', section='Placa base', department='Componentes', producer='Asus', image="https://www.google.com")
    
    def test_product_create_section_incorrect(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', price=1, inventory=1, description='test', section='Placa base1', department='Componentes', producer='Asus', image="https://www.google.com")
    def test_product_create_section_null(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', price=1, inventory=1, description='test', department='Componentes', producer='Asus', image="https://www.google.com")
    def test_product_create_description_null(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', price=1, inventory=1, section='Placa base', department='Componentes', producer='Asus', image="https://www.google.com")
   
    def test_create_image_incorrect(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', price=1, inventory=1, description='test', section='Placa base', department='Componentes', producer='Asus', image="hola")
        
    def test_create_image_null(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', price=1, inventory=1, description='test', section='Placa base', department='Componentes', producer='Asus')
    
    def test_create_department_incorrect(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', price=1, inventory=1, description='test', section='Placa base', department='Componentes1', producer='Asus', image="https://www.google.com")
    
    def test_create_department_null(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', price=1, inventory=1, description='test', section='Placa base', producer='Asus', image="https://www.google.com")
        
    def test_create_producer_incorrect(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', price=1, inventory=1, description='test', section='Placa base', department='Componentes', producer='Asus1', image="https://www.google.com")
        
    def test_create_producer_null(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', price=1, inventory=1, description='test', section='Placa base', department='Componentes', image="https://www.google.com")
        
    def test_create_inventory_incorrect(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', price=1, inventory=-1, description='test', section='Placa base', department='Componentes', producer='Asus', image="https://www.google.com")


   
   
    # #update test:
    def test_product_update_title_incorrect(self):
        with self.assertRaises(Exception):
            product = self.product2
            product.title = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
            product.save()
        
    def test_product_update_title_null(self):
        with self.assertRaises(Exception):
            product = self.product2
            product.title = ''
            product.save()
    
    def test_product_update_price_incorrect(self):
        with self.assertRaises(Exception):
            product = self.product2
            product.price = -1
            product.save()
    
    def test_product_update_price_null(self):
        with self.assertRaises(Exception):
            product = self.product2
            product.price = None
            product.save()
    
    def test_product_update_discount_price_negative(self):
        with self.assertRaises(Exception):
            product = self.product2
            product.discount_price = -1
            product.save()
    
    def test_product_update_discount_price_greater_than_price(self):
        with self.assertRaises(Exception):
            product = self.product2
            product.discount_price = 2
            product.save()
    
    def test_product_update_section_incorrect(self):
        with self.assertRaises(Exception):
            product = self.product2
            product.section = 'Placa base1'
            product.save()
        
    def test_product_update_section_null(self):
        with self.assertRaises(Exception):
            product = self.product2
            product.section = None
            product.save()
    
    def test_product_update_description_null(self):
        with self.assertRaises(Exception):
            product = self.product2
            product.description = None
            product.save()
        
    def test_update_image_incorrect(self):
        with self.assertRaises(Exception):
            product = self.product2
            product.image = 'hola'
            product.save()
    
    def test_update_image_null(self):
        with self.assertRaises(Exception):
            product = self.product2
            product.image = None
            product.save()
    
    def test_update_department_incorrect(self):
        with self.assertRaises(Exception):
            product = self.product2
            product.department = 'Componentes1'
            product.save()
    
    def test_update_department_null(self):
        with self.assertRaises(Exception):
            product = self.product2
            product.department = None
            product.save()
    
    def test_update_producer_incorrect(self):
        with self.assertRaises(Exception):
            product = self.product2
            product.producer = 'Asus1'
            product.save()
    
    def test_update_producer_null(self):
        with self.assertRaises(Exception):
            product = self.product2
            product.producer = None
            product.save()
    
    def test_update_inventory_incorrect(self):
        with self.assertRaises(Exception):
            product = self.product2
            product.inventory = -1
            product.save()
