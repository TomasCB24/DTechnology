from django import forms
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

PAYMENT_METHODS = (
    ('Contra reembolso', 'Contra reembolso'),
    ('Online', 'Online'),
)

class AddressForm(forms.Form):
    name = forms.CharField(label ='Introduce tu nombre (Opcional)', max_length=100, required = False)
    surname = forms.CharField(label = 'Introduce tus apellidos (Opcional)', max_length=100, required = False)
    email = forms.EmailField(label = 'Introduce tu email')
    phone = PhoneNumberField().formfield(label = 'Introduce un número de telefono (Opcional)', required = False)
    street_address = forms.CharField(label = 'Calle', max_length=100, required = True)
    apartment_address = forms.CharField(label = 'Dirección', max_length=100, required=True)
    country = CountryField().formfield(label = 'País', required = True)
    payment = forms.ChoiceField(label ='Introduce tu tipo de pago', choices=PAYMENT_METHODS, required=True)
