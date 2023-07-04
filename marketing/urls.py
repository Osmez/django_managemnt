from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns=[
    path('',views.marketing_home , name='marketing-home'),
    path('forbidden',views.not_allowed,name='mark-forbidden'),
    path('marketing/<int:mpost_id>/',views.marketing_detail_view , name='mark-detail'),
    path('marketing/new/', views.marketingpost_add , name='mark-new'),
    path('marketing/edit/<int:pk>/', views.MarkPostEditView.as_view() , name='mark-edit'),
    path('marketing/delete/<int:pk>/', views.MarkPostDeleteView.as_view() , name='mark-delete'),
    path('marketing/<int:user_id>',views.AddUserToGroupView , name='mark-admin'),
    path('marketing/remove/<int:user_id>',views.RemoveUserFromGroupView , name='mark-remove-admin'),
    path('marketing/<int:post_id>/comment/<int:pk>/reply', views.MarkCommentReplyView.as_view() ,name='mcomment-reply'),
    path('marketing/<int:post_id>/comment/delete/<int:pk>/', views.MarkCommentDelete.as_view() ,name='mcomment-delete'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)