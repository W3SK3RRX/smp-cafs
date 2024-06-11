from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('logout/', views.sair, name='sair'),

    #reset
    path('usuarios/reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('usuarios/reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('usuarios/reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('usuarios/reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
