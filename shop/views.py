import datetime
from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseRedirect
from .forms import ProductForm
from django.utils import timezone
from django.conf import settings
from django.core.paginator import Paginator
from django.urls.base import reverse_lazy
from django.views.generic.edit import UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum 
from .models import Product, Contact, Orders, OrderUpdate,Consumer
from django.contrib.auth.models import User
from django.contrib import messages
from math import ceil
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt


MERCHANT_KEY = 'kbzk1DSbJiV_O3p5';   # Your-Merchant-Key-Here



def index(request):
    
    urls = settings.STATIC_ROOT
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}

    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    
    cont = {'allProds': allProds , "cats":cats , "urls":urls}

    all_posts = Product.objects.all()
    search_term = ''

    if 'search' in request.GET:
        search_term = request.GET['search']
        all_posts = all_posts.filter(title__icontains=search_term)  

        pagin = Paginator(all_posts, 5)
        page = request.GET.get('page')
        pposts = pagin.get_page(page)

        get_dict_copy = request.GET.copy()
        params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
        print(params)
        
        cont = {'allProds': allProds , "cats":cats , "urls":urls,'pposts': pposts,'params': params,'search_term': search_term,}
        return render(request, 'shop/search.html', cont)

    return render(request, 'shop/index.html', cont)
    # return HttpResponse("<h1 align='center'> <font color='#FF0000' size='9' > Welcome Our Restaurant </font> </h1>")


def about(request):
    return render(request, 'shop/about.html')

def getProduct(request):
    if request.is_ajax and request.method == 'POST':
        pass


def contact(request):
    thank = False
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
        return render(request, 'shop/contact.html', {'thank': thank})
    return render(request, 'shop/contact.html', {'thank': thank})


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        phone = request.POST.get('tphone','')
        current_user = request.user
        
        if current_user is not None:
            try:
                order = Orders.objects.filter(order_id=orderId, phone=phone)
                if len(order) > 0:
                    update = OrderUpdate.objects.filter(order_id=orderId)
                    updates = []
                    for item in update:
                        updates.append({'text': item.update_desc, 'time': item.timestamp})
                        response = json.dumps({"status": "success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                    return HttpResponse(response)
                else:
                    return HttpResponse('{"status":"noitem"}')
            except Exception as e:
                return HttpResponse('{"status":"error"}')
        else:
            return HttpResponse('{"status":"هل استخدمت تطبيقنا سابقا؟"}')
    return render(request, 'shop/tracker.html')


def orderView(request):
    if request.user.is_authenticated:
        current_user = request.user
        orderHistory = Orders.objects.filter(userId=current_user.id)

        if len(orderHistory) == 0:
            messages.info(request, ".لايوجد طلبات")
            return render(request, 'shop/orderView.html')
        return render(request, 'shop/orderView.html', {'orderHistory': orderHistory})
        

    return render(request, 'shop/orderView.html')


def searchMatch(query, item):
    print(query)
    print(item.product_name.lower())
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower() or query in item.desc or query in item.product_name or query in item.category or query in item.desc.upper() or query in item.product_name.upper() or query in item.category.upper():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    print(query)
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    search = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query) < 1:
        search = {'msg': "No item available. Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', search)


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        message = request.POST.get('mess', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        u_phone = request.POST.get('phone', '')

        try:
            user = User.objects.get(username=u_phone)
            userd = authenticate(username=u_phone, password='')
            if userd is not None:
                login(request, user)
            order = Orders(items_json=items_json, userId=user.id, name=name, phone=u_phone, amount=amount)
            order.save()
            update = OrderUpdate(order_id=order.order_id, update_desc="The Order has been Placed")
            update.save()
            id = order.order_id
            mess = message + '\u200E' + '\n العنوان: ' + '\u200E'+ address + '\n' + '\u200E' + str(id) + '\u200E' + ' رمز الطلب :' + '\n'
            wurl = 'https://api.whatsapp.com/send?text='+ mess + '&phone=971509011761';
            
            return redirect(wurl);

        except User.DoesNotExist:
            # Create the user
            myuser = User.objects.create_user(username=u_phone, password='')
            myuser.phone = u_phone
            myuser.save()
            user = authenticate(username=u_phone, password='')
            login(request, user)
            order = Orders(items_json=items_json, userId=myuser.id, name=name, phone=u_phone, amount=amount)
            order.save()
            update = OrderUpdate(order_id=order.order_id, update_desc="The Order has been Placed")
            update.save()
            id = order.order_id
            mess = message + '\u200E' + '\n العنوان: ' + '\u200E'+ address + '\n' + '\u200E' + str(id) + '\u200E' + ' رمز الطلب :' + '\n'
            wurl = 'https://api.whatsapp.com/send?text='+ mess + '&phone=971509011761';
            
            return redirect(wurl);        
            
    return render(request, 'shop/checkout.html')


def productView(request, myid):
    product = Product.objects.filter(id=myid)
    # print(product)
    return render(request, 'shop/prodView.html', {'product': product[0]})


def handeLogin(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, "Invalid credentials! Please try again")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return HttpResponse("404- Not found")


def handleSignUp(request):
    print('loginPhone')
    if request.method == "POST":
        loginPhone = request.POST['lphone']
        
        try:
            user = User.objects.get(username=loginPhone)
            userd = authenticate(username=loginPhone, password='')
            
            if userd is not None:
                login(request, user)
            return redirect('index')

        except User.DoesNotExist:
            myuser = User.objects.create_user(username=loginPhone,password='')
            myuser.phone = loginPhone
            myuser.save()
            user = authenticate(username=loginPhone, password='')
            login(request, user)
            messages.success(request, " Your Account has been successfully created")
            return redirect('index')
    else:
        return HttpResponse("404 - Not found")


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




def dashboard(request):
    current_year = datetime.datetime.now()
    year_date = current_year.date()
    the_year = year_date.year
    the_month = year_date.month
    the_day = year_date.day
    
    all_orders = Orders.objects.all()
    all_orders = all_orders.order_by('-timestamp')
    
    pagin = Paginator(all_orders,5)
    page = request.GET.get('page')
    items = pagin.get_page(page)
    
    day_amount = Orders.objects.filter(timestamp__year = the_year,timestamp__month = the_month,timestamp__day = the_day).aggregate(Sum('amount'))
    day_orders = Orders.objects.filter(timestamp__year = the_year,timestamp__month = the_month,timestamp__day = the_day).count()

    mon_amount = Orders.objects.filter(timestamp__year = the_year,timestamp__month = the_month).aggregate(Sum('amount'))
    mon_orders = Orders.objects.filter(timestamp__year = the_year,timestamp__month = the_month).count()

    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.pub_date = timezone.now()
            post.save()
            
            return redirect('index')
    else:
        form = ProductForm()
        
    contxt = {
    'form':form,
    'orders':all_orders,
    'today_revenue':day_amount,
    'today_orders':day_orders,
    'new_orders':items,
    'mon_a':mon_amount,
    'mon_o':mon_orders,
    }

    return render(request, 'shop/dashboard.html',context=contxt)
    
def ordersPage(request):
    all_orders = Orders.objects.all()
    all_orders = all_orders.order_by('-timestamp')
    
    if 'search' in request.GET:
        search_term = request.GET['search']
        all_orders = all_orders.filter(pk=search_term) 

    pagin = Paginator(all_orders,10)
    page = request.GET.get('page')
    orders = pagin.get_page(page)

    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()

    cont = {
        'orders':orders,
        'params':params
    }

    return render(request,'shop/orders-page.html',cont)

def orderDetail(request, order_id):
    ord = Orders.objects.get(pk=order_id)

    cont = {
        'order':ord
    }
    return render(request, 'shop/order-detail.html',cont)

class orderDelete(LoginRequiredMixin,DeleteView):
    model  = Orders
    template_name = 'shop/order-delete.html'
    success_url = reverse_lazy('orders-page')
    
def itemsPage(request):
    all_items = Product.objects.all()
    all_items = all_items.order_by('-pub_date')

    if 'search' in request.GET:
        search_term = request.GET['search']
        all_items = all_items.filter(product_name__icontains=search_term) 

    pagin = Paginator(all_items,10)
    page = request.GET.get('page')
    items = pagin.get_page(page)

    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()

    cont = {
        'items':items,
        'params':params
    }

    return render(request,'shop/items-page.html',cont)

class itemDelete(LoginRequiredMixin,DeleteView):
    model  = Product
    template_name = 'shop/order-delete.html'
    success_url = reverse_lazy('items-page')
    
def addItem(request):
    if request.method == 'POST':
        name = request.POST.get('prodName', '')
        cat = request.POST.get('category', '')
        subc = request.POST.get('subcategory', '')
        desc = request.POST.get('desc', '')
        price = request.POST.get('price', '')
        img = request.FILES['img']
        dt = datetime.datetime.now()

        item = Product(product_name=name,category=cat,subcategory=subc,price=price,desc=desc,pub_date=dt,image=img)
        item.save() 

        return redirect('add-prod')

    form = ProductForm()

    return render(request, 'shop/add-form.html', {'form':form})
    
def getMonths(request):
    current_year = datetime.datetime.now()
    year_date = current_year.date()
    the_year = year_date.year
    the_month = year_date.month
    the_day = year_date.day

    #request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":        
        month_bucks = []
        ords = []
        months = [i.month for i in Orders.objects.values_list('timestamp', flat=True)]
        rel = set(months)
        ms = list(rel)
    
        for month in rel:
            mb = Orders.objects.filter(timestamp__year = the_year,timestamp__month = month).aggregate(Sum('amount'))
            the_ords = Orders.objects.filter(timestamp__year = the_year,timestamp__month = month).count()
            month_bucks.append(mb)
            ords.append(the_ords)

        return JsonResponse({"months":ms,"bucks":month_bucks,"ords":ords}, status = 200)

def getDayInfo(request):
    current_year = datetime.datetime.now()
    year_date = current_year.date()
    the_year = year_date.year
    the_month = year_date.month
    the_day = year_date.day

    if request.is_ajax and request.method == "GET":
        sums = []
        d_orders = []

        days = [i.day for i in Orders.objects.filter(timestamp__month = the_month).values_list('timestamp', flat=True)]
        rel = set(days)
        ms = list(rel)

        for day in rel:
            day_sum = Orders.objects.filter(timestamp__month = the_month,timestamp__day = day).aggregate(Sum('amount'))
            day_ord = Orders.objects.filter(timestamp__month = the_month,timestamp__day = day).count()
            sums.append(day_sum)
            d_orders.append(day_ord)
            
        day_amount = Orders.objects.filter(timestamp__year = the_year,timestamp__month = the_month,timestamp__day = the_day).aggregate(Sum('amount'))
        day_orders = Orders.objects.filter(timestamp__year = the_year,timestamp__month = the_month,timestamp__day = the_day).count()

        
    return JsonResponse({"days":ms,"bucks":sums,"days_orders":d_orders,"same_day_amount":day_amount,"same_day_orders":day_orders}, status = 200)
