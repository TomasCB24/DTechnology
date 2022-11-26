from django import forms
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class AddressForm(forms.Form):
    name = forms.CharField(label ='Introduce tu nombre (Opcional)', max_length=100, required = False)
    surname = forms.CharField(label = 'Introduce tu apellido (Opcional)', max_length=100, required = False)
    email = forms.EmailField(label = 'Introduce tu email')
    phone = PhoneNumberField().formfield(required = False)
    street_address = forms.CharField(max_length=100, required = True)
    apartment_address = forms.CharField(max_length=100, required=True)
    country = CountryField().formfield()
    address_type = forms.ChoiceField(label ='Introduce tu tipo de dirección', choices=ADDRESS_CHOICES, required=True)