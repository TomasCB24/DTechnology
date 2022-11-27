from django.test import TestCase

from Marketplace.models import Payment

# Create your tests here.
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
