from django import forms
from django.db import models
from .models import Product

class ProductForm(forms.ModelForm):
    product_name = forms.CharField( max_length=30, required=True)

    class Meta:
        model = Product
        fields = ['product_name','price','category','subcategory','desc','image']