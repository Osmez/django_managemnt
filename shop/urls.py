from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='add-item'),
    path('signup/', views.handleSignUp, name='handleSignUp'),
    path('login/', views.handeLogin, name="handleLogin"),
    path('logout/', views.handleLogout, name="handleLogout"),
    path('about/', views.about, name="AboutUs"),
    path('contact/', views.contact, name="ContactUs"),
    path('tracker/', views.tracker, name="TrackingStatus"),
    path('search/', views.search, name="Shop-Search"),
    path('checkout/', views.checkout, name="Checkout"),
    path('productView/<int:myid>', views.productView, name="productView"),
    path("addProduct/", views.addItem, name="add-prod"),

    path('orderView/', views.orderView, name="orderView"),
    path('itemspage/', views.itemsPage, name="items-page"),
    path('items/delete/<int:pk>/', views.itemDelete.as_view(), name="item-delete"),
    path('orderspage/', views.ordersPage, name="orders-page"),
    path('order/<int:order_id>',views.orderDetail, name="order-detail"),
    path('order/delete/<int:pk>/', views.orderDelete.as_view(), name="order-delete"),
    path('get/ajax/months', views.getMonths, name = "ajax_months"),
    path('get/ajax/days', views.getDayInfo, name = "ajax_days"),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)