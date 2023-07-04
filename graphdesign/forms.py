from django import forms
from .models import Graphpost, GraphComments

class GraphicForm(forms.ModelForm):
    title = forms.CharField(label="title",max_length=30,min_length=5)
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                'multiple':True
            }
        )
    )
    file = forms.FileField(
        required=False,
        label='Upload PDF',
        help_text='max. 42 megabytes',
                widget=forms.ClearableFileInput(
            attrs={
                'multiple':True
            }
        )
    )
    widget = forms.TextInput(attrs={'class': 'form-control'})
    class Meta:
        model = Graphpost
        fields = ['title','content']
        widgets = {
            'content_Text': forms.Textarea(attrs={'class':'form-control','rows':5, 'col':20}),
        }

class GraphcommentAddForm(forms.ModelForm):

    widget=forms.TextInput(attrs={'class': 'form-control'})
    class Meta:
        model = GraphComments
        fields = ['content',]
        widgets = {
            'content_Text': forms.Textarea(attrs={'class':'form-control','rows':3, 'col':20}),
        }