from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseRedirect

# I have created this file - Darshan
# from django.http import HttpResponse
from .models import Ecom_Product, Ecom_Contact, Ecom_Orders, Ecom_OrderUpdate
from django.contrib.auth.models import User
from django.contrib import messages
from math import ceil
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls.base import reverse_lazy
from django.http import JsonResponse
from django.db.models import Sum 
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import UpdateView,DeleteView
from django.contrib.auth import authenticate, login, logout
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime
import random
from urllib.parse import unquote

MERCHANT_KEY = 'kbzk1DSbJiV_O3p5';   # Your-Merchant-Key-Here


def index(request):
    items = []
    obj= Ecom_Product.objects.order_by('id')[0]
    objo= Ecom_Product.objects.order_by('id')[1]
    objt= Ecom_Product.objects.order_by('id')[2]

    items.append(obj)
    items.append(objo)
    items.append(objt)
    
    prices = []

    pr = Ecom_Product.objects.order_by('price')[0]
    pro = Ecom_Product.objects.order_by('price')[1]
    prt = Ecom_Product.objects.order_by('price')[2]

    max = Ecom_Product.objects.count()
    option1, option2, option3 = random.sample(range(1, max), 3)
    
    ran = []
    ran.append(Ecom_Product.objects.get(pk=option1))
    ran.append(Ecom_Product.objects.get(pk=option2))
    ran.append(Ecom_Product.objects.get(pk=option3))
    
    prices.append(pr)
    prices.append(pro)
    prices.append(prt)

    allProds = []
    catprods = Ecom_Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Ecom_Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    darshan = {'allProds': allProds,'items':items,'prices':prices,'ran':ran}

    return render(request, 'ecommerce/indexn.html', darshan)
    
def categorys(request):
    allProds = []
    catprods = Ecom_Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Ecom_Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    darshan = {'allProds': allProds,'cats':cats}

    return render(request, 'ecommerce/categorys.html', darshan)    

def category(request,cate):
    
    category = unquote(cate)
    
    prods = Ecom_Product.objects.all()
   

    darshan = {'cate':category,'prods':prods}

    return render(request, 'ecommerce/category.html', darshan)
    
def about(request):
    return render(request, 'ecommerce/about.html')
    
def newArrivals(request):
    current_year = datetime.now()
    year_date = current_year.date()
    the_year = year_date.year
    the_month = year_date.month
    the_day = year_date.day
    
    day_prods = Ecom_Product.objects.filter(pub_date__year = the_year,pub_date__month = the_month,pub_date__day = the_day)
    mon_prods = Ecom_Product.objects.filter(pub_date__year = the_year,pub_date__month = the_month)
    
    contxt = {
    'day_prods':day_prods,
    'month_prods':mon_prods,
    }
    
    return render(request, 'ecommerce/newArrivals.html/',context=contxt)
    
def edashboard(request):
    
    current_year = datetime.now()
    year_date = current_year.date()
    the_year = year_date.year
    the_month = year_date.month
    the_day = year_date.day

    all_orders = Ecom_Orders.objects.all()
    all_orders = all_orders.order_by('-timestamp')

    pagin = Paginator(all_orders,5)
    page = request.GET.get('page')
    items = pagin.get_page(page)

    day_amount = Ecom_Orders.objects.filter(timestamp__year = the_year,timestamp__month = the_month,timestamp__day = the_day).aggregate(Sum('amount'))
    day_orders = Ecom_Orders.objects.filter(timestamp__year = the_year,timestamp__month = the_month,timestamp__day = the_day).count()

    mon_amount = Ecom_Orders.objects.filter(timestamp__year = the_year,timestamp__month = the_month).aggregate(Sum('amount'))
    mon_orders = Ecom_Orders.objects.filter(timestamp__year = the_year,timestamp__month = the_month).count()

    if request.method == 'POST' and request.FILES['prod_img']:
        img = request.FILES['prod_img']
        fss = FileSystemStorage()
        file = fss.save(img.name,img)
        file_url = fss.url()
        return render(request, 'ecommerce/dashboard.html')
    
    contxt = {
    'orders':all_orders,
    'today_revenue':day_amount,
    'today_orders':day_orders,
    'new_orders':items,
    'mon_a':mon_amount,
    'mon_o':mon_orders,
    }
    
    return render(request, 'ecommerce/edashboard.html/',context=contxt)


def contact(request):
    thank = False
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Ecom_Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
        return render(request, 'shop/contact.html', {'thank': thank})
    return render(request, 'shop/contact.html', {'thank': thank})


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        name = request.POST.get('name', '')
        password = request.POST.get('password')
        user = authenticate(username=name, password=password)
        if user is not None:
            try:
                order = Ecom_Orders.objects.filter(order_id=orderId, email=email)
                if len(order) > 0:
                    update = Ecom_OrderUpdate.objects.filter(order_id=orderId)
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
            return HttpResponse('{"status":"Invalid"}')
    return render(request, 'shop/tracker.html')


def orderView(request):
    if request.user.is_authenticated:
        current_user = request.user
        orderHistory = Ecom_Orders.objects.filter(userId=current_user.id)
        if len(orderHistory) == 0:
            messages.info(request, "You have not ordered.")
            return render(request, 'shop/orderView.html')
        return render(request, 'shop/orderView.html', {'orderHistory': orderHistory})
    return render(request, 'shop/orderView.html')


def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower() or query in item.desc or query in item.product_name or query in item.category or query in item.desc.upper() or query in item.product_name.upper() or query in item.category.upper():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Ecom_Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Ecom_Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    darshan = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query) < 3:
        darshan = {'msg': "No item available. Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', darshan)


def echeckout(request):
    if request.method == "POST":
        
        items_json = request.POST.get('itemsJson', '')
        user_id = request.POST.get('user_id', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Ecom_Orders(items_json=items_json, userId=user_id, name=name, email=email, address=address, city=city, state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = Ecom_OrderUpdate(order_id=order.order_id, update_desc="The Order has been Placed")
        update.save()
        thank = True
        id = order.order_id
        if 'onlinePay' in request.POST:
            # Request paytm to transfer the amount to your account after payment by user
            darshan_dict = {

                'MID': 'WorldP64425807474247',  # Your-Merchant-Id-Here
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',

            }
            
            return render(request, 'ecommerce/paytm.html', {'darshan_dict': darshan_dict})
        elif 'cashOnDelivery' in request.POST:
            return render(request, 'ecommerce/echeckout.html', {'thank': thank, 'id': id})
    return render(request, 'ecommerce/echeckout.html')


    
def detailView(request, myid, cat):
    product = Ecom_Product.objects.filter(id=myid)
    
    allProds = Ecom_Product.objects.all()
    
    return render(request, 'ecommerce/prodView.html', {'product': product[0],'allProds':allProds,'cat':cat})
    
    
def eproductView(request, myid):
    product = Ecom_Product.objects.filter(id=myid)
    return render(request, 'ecommerce/adprodView.html', {'product': product[0]})


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
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        email = request.POST['email1']
        phone = request.POST['phone']
        password = request.POST['password']
        password1 = request.POST['password1']

        # check for errorneous input
        if (password1 != password):
            messages.warning(request, " Passwords do not match")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        try:
            user = User.objects.get(username=username)
            messages.warning(request, " Username Already taken. Try with different Username.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except User.DoesNotExist:
            # Create the user
            myuser = User.objects.create_user(username=username, email=email, password=password)
            myuser.first_name = f_name
            myuser.last_name = l_name
            myuser.phone = phone
            myuser.save()
            messages.success(request, " Your Account has been successfully created")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse("404 - Not found")


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class orderDelete(DeleteView):
    model  = Ecom_Orders
    template_name = 'ecommerce/order-delete.html'
    success_url = reverse_lazy('orders-page')

def addItem(request):
    
    if request.method == 'POST':
        name = request.POST.get('prodName', '')
        cat = request.POST.get('category', '')
        subc = request.POST.get('subcategory', '')
        desc = request.POST.get('desc', '')
        price = request.POST.get('price', '')
        img = request.FILES['img']
        getsale = request.POST.get('salev','')
        sale = False
        if(getsale):
            sale = True
        else:
            slae = False
    
        salea = request.POST.get('price', '')
        dt = datetime.now()

        item = Ecom_Product(product_name=name,category=cat,subcategory=subc,desc=desc,price=price,pub_date=dt,image=img,in_sale=sale,sale_amount=salea)
        item.save() 

        return redirect('add-prod')


    return render(request, 'ecommerce/add-form.html')

def ordersPage(request):
    all_orders = Ecom_Orders.objects.all()
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

    return render(request,'ecommerce/orders-page.html',cont)


def itemsPage(request):
    all_items = Ecom_Product.objects.all()
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

    return render(request,'ecommerce/items-page.html',cont)

def orderDetail(request, order_id):
    ord = Ecom_Orders.objects.get(pk=order_id)


    cont = {
        'order':ord
    }
    return render(request, 'shop/order-detail.html',cont)

class itemDelete(DeleteView):
    model  = Ecom_Product
    template_name = 'ecommerce/order-delete.html'
    success_url = reverse_lazy('items-page')

def getMonths(request):
    current_year = datetime.now()
    year_date = current_year.date()
    the_year = year_date.year
    the_month = year_date.month
    the_day = year_date.day

    #request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":        
        month_bucks = []
        ords = []
        months = [i.month for i in Ecom_Orders.objects.values_list('timestamp', flat=True)]
        rel = set(months)
        ms = list(rel)
    
        for month in rel:
            mb = Ecom_Orders.objects.filter(timestamp__year = the_year,timestamp__month = month).aggregate(Sum('amount'))
            the_ords = Ecom_Orders.objects.filter(timestamp__year = the_year,timestamp__month = month).count()
            month_bucks.append(mb)
            ords.append(the_ords)

        return JsonResponse({"months":ms,"bucks":month_bucks,"ords":ords}, status = 200)

def getDayInfo(request):
    current_year = datetime.now()
    year_date = current_year.date()
    the_year = year_date.year
    the_month = year_date.month
    the_day = year_date.day

    if request.is_ajax and request.method == "GET":
        sums = []
        d_orders = []

        days = [i.day for i in Ecom_Orders.objects.filter(timestamp__month = the_month).values_list('timestamp', flat=True)]
        rel = set(days)
        ms = list(rel)

        for day in rel:
            day_sum = Ecom_Orders.objects.filter(timestamp__month = the_month,timestamp__day = day).aggregate(Sum('amount'))
            day_ord = Ecom_Orders.objects.filter(timestamp__month = the_month,timestamp__day = day).count()
            sums.append(day_sum)
            d_orders.append(day_ord)
            
        day_amount = Ecom_Orders.objects.filter(timestamp__year = the_year,timestamp__month = the_month,timestamp__day = the_day).aggregate(Sum('amount'))
        day_orders = Ecom_Orders.objects.filter(timestamp__year = the_year,timestamp__month = the_month,timestamp__day = the_day).count()

        
    return JsonResponse({"days":ms,"bucks":sums,"days_orders":d_orders,"same_day_amount":day_amount,"same_day_orders":day_orders}, status = 200)

