from django.test import TestCase

from Marketplace.models import Product

# Create your tests here.
class ProductTestCase(TestCase):
    def setUp(self):
        self.product1 = Product.objects.create(title='test', price=1, inventory=1, description='test', section='Motherboard', department='Components', producer='Asus', image="https://www.google.com")
        self.product2 = Product.objects.create(title='testUpdate', price=1, inventory=1, description='test', section='Motherboard', department='Components', producer='Asus', image="https://www.google.com")
        
    def test_product_create(self):
        product = self.product1
        self.assertEqual(product.title, 'test')
        self.assertEqual(product.price, 1)
        self.assertEqual(product.inventory, 1)
        self.assertEqual(product.description, 'test')
        self.assertEqual(product.section, 'Motherboard')
        self.assertEqual(product.department, 'Components')
        self.assertEqual(product.producer, 'Asus')
    
    def test_product_update(self):
        product = self.product2
        product.title = 'testUpdate2'
        product.description = 'testUpdate2'
        product.price = 2
        product.inventory = 2
        product.section = 'Keyboards'
        product.department = 'Components'
        product.producer = 'Intel'
        product.save()
        self.assertEqual(product.title, 'testUpdate2')
        self.assertEqual(product.price, 2)
        self.assertEqual(product.inventory, 2)
        self.assertEqual(product.description, 'testUpdate2')
        self.assertEqual(product.section, 'Keyboards')
        self.assertEqual(product.department, 'Components')
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
            Product.objects.create(title='AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', price=1, inventory=1, description='test', section='Motherboard', department='Components', producer='Asus', image="https://www.google.com")
    
    def test_product_create_title_null(self):
        with self.assertRaises(Exception):
            Product.objects.create(price=1, inventory=1, description='test', section='Motherboard', department='Components', producer='Asus', image="https://www.google.com")
    def test_product_create_price_incorrect(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', price=-1, inventory=1, description='test', section='Motherboard', department='Components', producer='Asus', image="https://www.google.com")
   
    def test_product_create_price_null(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', inventory=1, description='test', section='Motherboard', department='Components', producer='Asus', image="https://www.google.com")
   
    def test_product_create_discount_price_negative(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', price=1, discount_price=-1, inventory=1, description='test', section='Motherboard', department='Components', producer='Asus', image="https://www.google.com")

    def test_product_create_discount_price_greater_than_price(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', price=1, discount_price=2, inventory=1, description='test', section='Motherboard', department='Components', producer='Asus', image="https://www.google.com")
    
    def test_product_create_section_incorrect(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', price=1, inventory=1, description='test', section='Motherboard1', department='Components', producer='Asus', image="https://www.google.com")
    def test_product_create_section_null(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', price=1, inventory=1, description='test', department='Components', producer='Asus', image="https://www.google.com")
    def test_product_create_description_null(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', price=1, inventory=1, section='Motherboard', department='Components', producer='Asus', image="https://www.google.com")
   
    def test_create_image_incorrect(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', price=1, inventory=1, description='test', section='Motherboard', department='Components', producer='Asus', image="hola")
        
    def test_create_image_null(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', price=1, inventory=1, description='test', section='Motherboard', department='Components', producer='Asus')
    
    def test_create_department_incorrect(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', price=1, inventory=1, description='test', section='Motherboard', department='Components1', producer='Asus', image="https://www.google.com")
    
    def test_create_department_null(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', price=1, inventory=1, description='test', section='Motherboard', producer='Asus', image="https://www.google.com")
        
    def test_create_producer_incorrect(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', price=1, inventory=1, description='test', section='Motherboard', department='Components', producer='Asus1', image="https://www.google.com")
        
    def test_create_producer_null(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', price=1, inventory=1, description='test', section='Motherboard', department='Components', image="https://www.google.com")
        
    def test_create_inventory_incorrect(self):
        with self.assertRaises(Exception):
            Product.objects.create(title='test', price=1, inventory=-1, description='test', section='Motherboard', department='Components', producer='Asus', image="https://www.google.com")


   
   
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
            product.section = 'Motherboard1'
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
            product.department = 'Components1'
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
    
    
