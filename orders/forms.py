from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    pickup_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local'
        }),
        required=True,
        label="Pickup date & time"
    )

    class Meta:
        model  = Order
        fields = ['first_name','last_name','email','address','pickup_datetime']


