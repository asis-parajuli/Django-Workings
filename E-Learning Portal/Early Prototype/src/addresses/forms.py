from django import forms

from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'fullname',
            'address_line_1',
            'address_line_2',
            'province',
            'city',
            'phone_number'
            ]
