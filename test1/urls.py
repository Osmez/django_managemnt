from django.urls import path 
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('' , views.start, name='start'),
    path('home/', views.home , name='home'),
    path('detail/<int:post_id>/', views.post_detail , name='detail'),
    path('new_post/' ,views.PostCreateView.as_view(), name='new_post'), 
    path('detail/<slug:pk>/update/',views.PostUpdateView.as_view(),name='post-update'),
    path('detail/<slug:pk>/delete/',views.PostDeleteView.as_view(),name='post-delete'),
    path('notification/<int:n_pk>/post/<int:post_pk>',views.ProgNotifi.as_view(),name="p-not"),
    path('mnotification/<int:n_pk>/post/<int:post_pk>',views.MarkNotifi.as_view(),name="m-not"),
    path('gnotification/<int:n_pk>/post/<int:post_pk>',views.GraphNotifi.as_view(),name="g-not"),
    path('notification/delete/<int:n_pk>',views.RemoveNotifi.as_view(),name='notification-delete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)