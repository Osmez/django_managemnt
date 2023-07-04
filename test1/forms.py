from django import forms
from .models import post


class PostCreateForm(forms.ModelForm):
    title=forms.CharField(label='عنوان المنشور')
    content=forms.CharField(label='نص المنشور' , widget=forms.Textarea)
    image = forms.ImageField(required=False)
    class Meta:
        model=post
        fields=['title' ,'content']
