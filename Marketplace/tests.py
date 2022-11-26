from django.test import TestCase
from Marketplace.models import Product, OrderProduct, Order
from datetime import datetime, timezone

# Create your tests here.

class OrderTestCase(TestCase):

    def setUp(self):
        
        product_1 = Product.objects.create(title="Producto 1", price=100, section="Mouses", description="Descripción 1", image="https://cdn-icons-png.flaticon.com/512/1554/1554591.png", department="Components", producer="Asus", inventory=10)
        product_2 = Product.objects.create(title="Producto 2", price=100, section="Mouses", description="Descripción 2", image="https://cdn-icons-png.flaticon.com/512/1554/1554591.png", department="Components", producer="Asus", inventory=10)
        product_3 = Product.objects.create(title="Producto 3", price=100, section="Mouses", description="Descripción 3", image="https://cdn-icons-png.flaticon.com/512/1554/1554591.png", department="Components", producer="Asus", inventory=10)

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
        product_3 = Product.objects.get(id=3)

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