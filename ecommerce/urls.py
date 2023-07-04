from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categorys/', views.categorys, name='categorys'),
    path('categorys/<str:cate>', views.category, name='category'),
    path('newArrivals/', views.newArrivals, name='newArrivals'),
    path('signup/', views.handleSignUp, name='handleSignUp'),
    path('login/', views.handeLogin, name="handleLogin"),
    path('logout/', views.handleLogout, name="handleLogout"),
    path('about/', views.about, name="AboutUs"),
    path('contact/', views.contact, name="ContactUs"),
    path('tracker/', views.tracker, name="TrackingStatus"),
    path('search/', views.search, name="Search"),
    path('ecom-checkout/', views.echeckout, name="ecom-Checkout"),
    path('detailView/<int:myid>/<str:cat>', views.detailView, name="detailView"),
    path('eaproductView/<int:myid>', views.eproductView, name="eaproductView"),
    path('orderView/', views.orderView, name="orderView"),
    path('addProduct/', views.addItem, name="add-prod"),
    path('itemspage/', views.itemsPage, name="items-page"),
    path('items/delete/<int:pk>/', views.itemDelete.as_view(), name="item-delete"),
    path('orderspage/', views.ordersPage, name="orders-page"),
    path('order/<int:order_id>',views.orderDetail, name="order-detail"),
    path('order/delete/<int:pk>/', views.orderDelete.as_view(), name="order-delete"),
    path('ecom-dashboard', views.edashboard, name='ecom-dashboard'),
    path('get/ajax/months', views.getMonths, name = "ajax_months"),
    path('get/ajax/days', views.getDayInfo, name = "ajax_days"),
]