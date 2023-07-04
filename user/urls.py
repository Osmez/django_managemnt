from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
#
from django.contrib.auth import views as auth_views
#
from django.contrib.auth.views import LoginView , LogoutView


urlpatterns=[
        path('register/', views.register , name='register'),

        path('reset_password/',auth_views.PasswordResetView.as_view(template_name="user/password-reset.html"),name="reset_password"),
        path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="user/passwordreset-done.html"),name="passowrd_reset_done"),
        path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="user/password-reset.html"),name="password_reset_confirm"),
        path('reset_password_complete/',auth_views.PasswordResetView.as_view(),name="password_reset_complete"),

        path('the/<int:pk>', views.aview , name='thereq'),
        path('emregister/', views.employ_register , name='employ-register'),
        path('acceptregister/', views.to_accept , name='accept-register'),
        path('req/delete/<int:pk>/', views.RegisterReqDeleteView.as_view() , name='reg-delete'),

        # path('login/',LoginView.as_view(template_name='user/login.html'), name='login'),
        path('login/',views.login_user, name='login'),
        path('logout/',views.logout_user, name='logout'),
        path('profile/', views.profile , name='profile'),
        path('profile_update/', views.profile_update , name='profile_update'),
        path('users/', views.get_users , name='users'),
        path('user-detail/<int:pk>', views.userVIew , name='user-detail'),

]+ static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)