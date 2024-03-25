from .models import Product, Country
from django.forms import ModelForm, Form, ModelChoiceField
from django.forms import DateField, CharField, ChoiceField, TextInput, Select


class ProductAdvancedSearch(Form):
    name = CharField(required=False)
    country = ModelChoiceField(
        queryset=Country.objects.all(),
        to_field_name='id',
        required=True,
        widget=Select(attrs={'class': 'form-control'})
    )
    # created_at = DateField(required=False, widget=TextInput(
    #     attrs={
    #         'filter_method': '__gte',
    #     }
    # ))
class CallDetailsAdvancedSearch(Form):
    customer_id = CharField(required=False)
    call_type = CharField(max_length=100, required=False)