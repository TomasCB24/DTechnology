from django.test import TestCase
from Marketplace.models import Address

# Create your tests here.

class AddressTestCase(TestCase):

    def setUp(self):
        Address.objects.create(name="Jesús",surname="Luque", email="jluque@gmail.com", phone="678985456", street_address="Avda. Reina Mercedes - 51", apartment_address="1º A", country="ES", address_type="B")
        Address.objects.create(name="Marcos",surname="Torrecilla", email="marcost@gmail.com", phone="654875695", street_address="Avda. Reina Mercedes - 27", apartment_address="6º B", country="ES", address_type="S")

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
        self.assertEqual(address.address_type,"B")

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
        address.address_type = "S"
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
        self.assertEqual(new_address.address_type,"S")

    #Create tests

    def test_address_create_email_duplicated(self):
        with self.assertRaises(Exception):
            Address.objects.create(name="José", surname="Luque", email="jluque@gmail.com", phone="672299956", street_address="Avda. Reina Mercedes - 59", apartment_address="5º D", country="ES", address_type="S")

    def test_address_create_phone_duplicated(self):
        with self.assertRaises(Exception):
            Address.objects.create(name="José", surname="Luque", email="joseluque@gmail.com", phone="654875695", street_address="Avda. Reina Mercedes - 59", apartment_address="5º D", country="ES", address_type="S")

    def test_address_create_name_incorrect(self):
        with self.assertRaises(Exception):
            Address.objects.create(name="Nombrenombrenombrenombrenombrenombrenombrenombrenombrenombrenombrenombrenombrenombrenombrenombrenombr", surname="Luque", email="joseluque@gmail.com", phone="672299956", street_address="Avda. Reina Mercedes - 59", apartment_address="5º D", country="ES", address_type="S")

    def test_address_create_surname_incorrect(self):
        with self.assertRaises(Exception):
            Address.objects.create(name="José", surname="Apellidoapellidoapellidoapellidoapellidoapellidoapellidoapellidoapellidoapellidoapellidoapellidoapell", email="joseluque@gmail.com", phone="672299956", street_address="Avda. Reina Mercedes - 59", apartment_address="5º D", country="ES", address_type="S")

    def test_address_create_street_address_incorrect(self):
        with self.assertRaises(Exception):
            Address.objects.create(name="José", surname="Luque", email="joseluque@gmail.com", phone="672299956", street_address="Direccióndireccióndireccióndireccióndireccióndireccióndireccióndireccióndireccióndireccióndireccióndi", apartment_address="5º D", country="ES", address_type="S")

    def test_address_create_apartment_address_incorrect(self):
        with self.assertRaises(Exception):
            Address.objects.create(name="José", surname="Luque", email="joseluque@gmail.com", phone="672299956", street_address="Avda. Reina Merceder - 59", apartment_address="Direccióndireccióndireccióndireccióndireccióndireccióndireccióndireccióndireccióndireccióndireccióndi", country="ES", address_type="S")

    def test_address_create_email_incorrect(self):
        with self.assertRaises(Exception):
            Address.objects.create(name="José", surname="Luque", email="joseluquegmail.com", phone="672299956", street_address="Avda. Reina Mercedes - 59", apartment_address="5º D", country="ES", address_type="S")

    def test_address_create_phone_blank(self):
        with self.assertRaises(Exception):
            Address.objects.create(name="José", surname="Luque", email="joseluque@gmail.com", phone="", street_address="Avda. Reina Mercedes - 59", apartment_address="5º D", country="ES", address_type="S")

    def test_address_create_phone_incorrect(self):
        with self.assertRaises(Exception):
            Address.objects.create(name="José", surname="Luque", email="joseluque@gmail.com", phone="6722999956", street_address="Avda. Reina Mercedes - 59", apartment_address="5º D", country="ES", address_type="")

    def test_address_create_address_type_blank(self):
        with self.assertRaises(Exception):
            Address.objects.create(name="José", surname="Luque", email="joseluque@gmail.com", phone="672299956", street_address="Avda. Reina Mercedes - 59", apartment_address="5º D", country="España", address_type="Shipping")

    def test_address_create_address_type_incorrect(self):
        with self.assertRaises(Exception):
            Address.objects.create(name="José", surname="Luque", email="joseluque@gmail.com", phone="672299956", street_address="Avda. Reina Mercedes - 59", apartment_address="5º D", country="España", address_type="Shipping")

    #Update tests

    def test_address_update_email_duplicated(self):
        with self.assertRaises(Exception):
            address = Address.objects.get(email = "jluque@gmail.com")
            address.email = "marcost@gmail.com"
            address.save()
    
    def test_address_update_phone_duplicated(self):
        with self.assertRaises(Exception):
            address = Address.objects.get(email = "jluque@gmail.com")
            address.phone = "654875695"
            address.save()

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

    def test_address_update_phone_blank(self):
        with self.assertRaises(Exception):
            address = Address.objects.get(email = "jluque@gmail.com")
            address.phone = ""
            address.save()

    def test_address_update_phone_incorrect(self):
        with self.assertRaises(Exception):
            address = Address.objects.get(email = "jluque@gmail.com")
            address.phone = "6722999956"
            address.save()
    
    def test_address_update_address_type_blank(self):
        with self.assertRaises(Exception):
            address = Address.objects.get(email = "jluque@gmail.com")
            address.address_type = ""
            address.save()
    
    def test_address_update_address_type_incorrect(self):
        with self.assertRaises(Exception):
            address = Address.objects.get(email = "jluque@gmail.com")
            address.address_type = "Shipping"
            address.save()