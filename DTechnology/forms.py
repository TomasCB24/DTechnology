from django import forms
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class AddressForm(forms.Form):
    name = forms.CharField(label ='Nombre', max_length=100, required = False)
    surname = forms.CharField(label = 'Apellidos', max_length=100, required = False)
    email = forms.EmailField(label = 'Email')
    phone = PhoneNumberField().formfield(label = 'Número de teléfono', required = False)
    street_address = forms.CharField(label = 'Calle', max_length=100, required = True)
    apartment_address = forms.CharField(label = 'Dirección', max_length=100, required=True)
    country = CountryField().formfield(label = 'País', required = False)
    address_type = forms.ChoiceField(label ='Tipo de dirección', choices=ADDRESS_CHOICES, required=True)