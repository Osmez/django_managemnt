from graphdesign.views import not_allowed
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns=[
    path('',views.programming_home , name='progrm-home'),
    path('programming/forbidden', views.not_allowed ,name ='progrm-forbidden'),
    path('programming/<int:ppost_id>/',views.programming_detail_view , name='progrm-detail'),
    path('programming/<int:ppost_id>/<int:reply_id>',views.programming_detail_view_reply , name='progrm-detail-reply'),
    path('programming/<int:user_id>',views.AddUserToGroupView , name='progrm-admin'),
    path('programming/remove/<int:user_id>',views.RemoveUserFromGroupView , name='progrm-remove-admin'),
    path('programming/new/', views.programmingpost_add , name='progrm-new'),
    path('programming/edit/<int:pk>/', views.ProgPostEditView.as_view() , name='progrm-edit'),
    path('programming/delete/<int:pk>/', views.ProgPostDeleteView.as_view() , name='progrm-delete'),
    path('programming/<int:post_id>/comment/<int:pk>/reply', views.ProgCommentReplyView.as_view() ,name='pcomment-reply'),
    path('programming/<int:post_id>/comment/<int:pk>/<int:rk>/reply', views.ProgReplyReplyView.as_view() ,name='preply-reply'),
    path('programming/<int:post_id>/comment/delete/<int:pk>/', views.ProgCommentDelete.as_view() ,name='pcomment-delete'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)