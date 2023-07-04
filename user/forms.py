from asyncio.windows_events import NULL
from django import forms
from django.contrib.auth.models import User,Group
from .models import Profile,Sections,Requests



class UserRequest(forms.ModelForm):
    username=forms.CharField(label='اسم المستخدم',max_length=30 ,help_text='اسم المستخدم يجب ألا يحوي على مسافات ')
    email=forms.EmailField(label='البريد الالكتروني')
    first_name=forms.CharField(label='الاسم الأول')
    last_name=forms.CharField(label='الاسم الأخير')
    Specialization=forms.CharField(label=' التخصص')
    password1=forms.CharField(label='كلمة المرور' ,widget=forms.PasswordInput(),min_length=8)
    password2=forms.CharField(label='تأكيد كلمة المرور' ,widget=forms.PasswordInput(),min_length=8)
    
    class Meta:
        model= Requests
        fields = ('username','email','first_name','last_name','Specialization','password1','password2')
    
    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password1']!=cd['password2']:
           raise forms.ValidationError('كلمة المرور غير متطابقة')
        return cd['password2']
        
    def clean_username(self):
        cd=self.cleaned_data
        if Requests.objects.filter(username=cd['username']).exists():
           raise forms.ValidationError('يوجد طلب اخر بنفس الاسم') 
        if User.objects.filter(username=cd['username']).exists():
           raise forms.ValidationError('يوجد مستخدم اخر بنفس الاسم .اختر اسم مميز') 
        return cd['username']
         
         





class UserCreationForm(forms.ModelForm):
      username=forms.CharField(label='اسم المستخدم',max_length=30 ,help_text='اسم المستخدم يجب ألا يحوي على مسافات ')
      email=forms.EmailField(label='البريد الالكتروني')
      first_name=forms.CharField(label='الاسم الأول')
      last_name=forms.CharField(label='الاسم الأخير')
      Specialization=forms.CharField(label=' التخصص')
      
      password2=forms.CharField(label='تأكيد كلمة المرور' ,min_length=8)
     
      sections = forms.CharField(label="اختر القسم",widget=forms.Select(choices=Sections.SECTIONS_CHOICES))   

      class Meta:
         model= User
         fields = ('username','email','first_name','last_name','Specialization','password2','sections')

      def clean_password2(self):
         cd=self.cleaned_data
         return cd['password2']

      def clean_username(self):
         cd=self.cleaned_data
         if User.objects.filter(username=cd['username']).exists():
               raise forms.ValidationError('يوجد مستخدم مسجل بهذا الاسم') 
         return cd['username']  

      def get_grop(self):
          cd = self.cleaned_data
          return cd['sections']
       


class LoginForm(forms.ModelForm):
    username=forms.CharField(label='اسم المستخدم')
    password=forms.CharField(label='كلمة المرور' ,widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=('username','password')
   
class UserUpdateForm(forms.ModelForm):
    first_name=forms.CharField(label='الاسم الأول')
    last_name=forms.CharField(label='الاسم الأخير')
    email=forms.EmailField(label='البريد الالكتروني')

    class Meta:
        model=User
        fields=('first_name','last_name','email')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=('image',)
