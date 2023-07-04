from django import forms
from .models import Progrmpost,Progrmcomments

class ProgrmPostAddForm(forms.ModelForm):

    title = forms.CharField(label="title",max_length=30,min_length=5,
    widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                'multiple':True
            }
        )
    )
    file = forms.FileField(required=False,label='Upload PDF',help_text='max. 42 megabytes',
    widget=forms.ClearableFileInput(
        attrs={
            'multiple':True
        }
    )
    )
    class Meta:
        model   = Progrmpost
        fields  = ['title','content','file']
        widgets = {
            'content_Text': forms.Textarea(attrs={'class':'form-control','rows':10, 'col':20}),
        }

class ProgrmCommentAddForm(forms.ModelForm):

    widget=forms.TextInput(attrs={'class': 'form-control'})
    class Meta:
        model = Progrmcomments
        fields = ['content',]
        widgets = {
            'content_Text': forms.Textarea(attrs={'class':'form-control','rows':2, 'col':20}),
        }
