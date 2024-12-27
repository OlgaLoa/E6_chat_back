from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [

   path('login/', LoginUser.as_view(), name='login'),
   path('logout/', LogoutView.as_view(), name='logout'),
   path('registration/',  UserRegistration.as_view(), name='registration'),
   path('account/', views.account, name='account'),
   path('updating/<int:pk>/', UpdateUser.as_view(), name='updating'),
   path('list/', UserList.as_view(), name='user_list'),
]