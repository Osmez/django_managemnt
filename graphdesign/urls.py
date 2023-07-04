from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns=[
    path('',views.graphic_home , name='graph-home'),
    path('graphic/forbidden',views.not_allowed , name='graph-forbidden'),
    path('graphic/<int:gpost_id>/',views.graphic_detail_view , name='graph-detail'),
    path('graphic/<int:user_id>',views.AddUserToGroupView , name='graph-admin'),
    path('graph/remove/<int:user_id>',views.RemoveUserFromGroupView , name='graph-remove-admin'),    
    path('graphic/new/', views.graphic_add , name='graph-new'),
    path('graphic/edit/<int:pk>/', views.GraphPostEditView.as_view() , name='graph-edit'),
    path('graphic/delete/<int:pk>/', views.GraphPostDeleteView.as_view() , name='graph-delete'),
    path('graphic/<int:post_id>/comment/<int:pk>/reply', views.GraphCommentReplyView.as_view() ,name='gcomment-reply'),
    path('graphic/<int:post_id>/comment/delete/<int:pk>/', views.GraphCommentDelete.as_view() ,name='gcomment-delete'),

]