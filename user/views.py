from asyncio.windows_events import NULL
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .forms import UserCreationForm,UserRequest,UserUpdateForm,ProfileUpdateForm,LoginForm
from django.contrib import messages
from test1.models import post
from user.models import Profile
from django.contrib.auth import authenticate ,login ,logout
from django.core.paginator import Paginator ,PageNotAnInteger ,EmptyPage
from django.contrib.auth.decorators import login_required
from .models import Requests
from django.views.generic.edit import DeleteView
from django.urls.base import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView,DeleteView
from django.http import HttpResponse


def register(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            new_user=form.save(commit=False)
           # username=form.cleaned_data['username']
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            messages.success(
               request, f'تهانينا {new_user} لقد تمت عملية تسجيل الدخول بنجاح.')
            
            d = form.get_grop()
            g = Group.objects.get(name=d)
            new_user.groups.add(g)
            
            return redirect('login')

    else:
        form=UserCreationForm()
    return render(request, 'user/register.html',{
        'title':'التسجيل',
        'form':form,
    })

def employ_register(request):
    if request.method=='POST':
        form=UserRequest(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('start')

    else:
        form=UserRequest()
    return render(request, 'user/employ.html',{'form':form})

@login_required(login_url='login')
def to_accept(request):
    theres = Requests.objects.all()
    count = Requests.objects.count()
    #form = UserCreationForm(request.POST)
    if request.method=='POST':
        print('dfd')

    return render(request, 'user/toaccept.html',{'req':theres,'count':count})

@login_required(login_url='login')
def aview(request,pk):
    instance = Requests.objects.get(id=pk)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
                new_user=form.save(commit=False)
            # username=form.cleaned_data['username']
                new_user.set_password(form.cleaned_data['password2'])
                new_user.save()
                messages.success(
                request, f' {new_user} لقد تمت عملية تسجيل  بنجاح.')
                
                d = form.get_grop()
                g = Group.objects.get(name=d)
                new_user.groups.add(g)
                instance.accepted = True
                instance.save()
                return redirect('accept-register')

    else:
        form=UserCreationForm(instance=instance)

    return render(request,'user/thereq.html',{'form':form})

@login_required
def userVIew(request,pk):
    instance = User.objects.get(id=pk)
    g = instance.groups.all()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

    else:
        form = UserCreationForm(instance = instance)
        

    return render(request,'user/user-detail.html',{'form':form,'g':g[0]})



def login_user(request):
    if request.user.is_authenticated:
        return redirect('profile')
        
    if request.method=='POST':
        form=LoginForm()
        username=request.POST['username']
        password=request.POST['password']
        
        user= authenticate(request, username=username ,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('profile')
        else:
            messages.warning(request, 'هناك خطأ في اسم المستخدم أو كلمة المرور.') 
              
    else:
        form=LoginForm()

    return render (request, 'user/login.html' ,{
        'title':'تسجيل الدخول',
        'form':form,
    })

def logout_user(request):
    logout(request)
    return render(request, 'test1/start.html' ,{
        'title':'تسجيل الخروج',
    })
@login_required(login_url='login')
def profile(request):
    posts1= post.objects.filter(author=request.user)
    post_list= post.objects.filter(author=request.user)
    count = Requests.objects.count()

    paginator=Paginator(post_list,5)
    page=request.GET.get('page')
    try:
        post_list=paginator.page(page)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_page)
    return render(request , 'user/profile.html'
       ,{'title':' الملف الشخصي',
        'posts':posts1,
        'page':page,
        'post_list':post_list,
        'count':count
        })
@login_required(login_url='login')
def profile_update(request):
    if request.method=='POST':
        user_form=UserUpdateForm(request.POST,instance=request.user)
        profile_form=ProfileUpdateForm(request.POST,request.FILES, instance=request.user.profile)
        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            profile_form.save()
            messages.success(
               request, 'تم تحديث الملف الشخصي ')
            return redirect('profile')
    else:
        user_form=UserUpdateForm(instance=request.user)
        profile_form=ProfileUpdateForm(instance=request.user.profile)
   

    context={
        'title':'تعديل الملف الشخصي',
        'user_form': user_form,
        'profile_form':profile_form,
    }
    return render(request , 'user/profile_update.html' ,context)

@login_required(login_url='login')
def get_users(request):
    the_usres = User.objects.all()
    profiles = Profile.objects.all()
    context = {'users':the_usres,'profiles':profiles}
    return render(request, 'user/users.html', context)

class RegisterReqDeleteView(LoginRequiredMixin,DeleteView):
    model = Requests
    template_name = 'programming/progrm-delete.html'
    success_url = reverse_lazy('home')
    
