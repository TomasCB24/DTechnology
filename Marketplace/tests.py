from django.test import TestCase

from Marketplace.models import OrderProduct, Product

# Create your tests here.
class OrderProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(title="titlePrueba", description="description", price=4.89, discount_price=3, section="Motherboard", image="https://www.google.com", department="Components", producer="Nvidia", inventory=5)
        Product.objects.create(title="titlePrueba2", description="description2", price=4.89, discount_price=3, section="Motherboard", image="https://www.google.com", department="Components", producer="Nvidia", inventory=5)
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
            