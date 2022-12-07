from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('accounts/',views.AccountView.as_view()),
    path('login/',obtain_auth_token),
    path('accounts/newest/<int:num>/',views.NewestAccountView.as_view()),
    path('accounts/<pk>/',views.PatchAccountView.as_view()),
    path('accounts/<pk>/management/',views.SoftDeleteView.as_view()),

]