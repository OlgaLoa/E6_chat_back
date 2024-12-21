from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import *
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from .models import *
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse


# РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ
class UserRegistration(CreateView):
    model = get_user_model()
    template_name = 'users/registration.html'
    success_url = reverse_lazy('login')
    fields = ['username', 'password', 'photo']


# АВТОРИЗАЦИЯ ПОЛЬЗОВАТЕЛЯ
class LoginUser(LoginView):#без отдельной формы
    form_class = AuthenticationForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('account')


# ОБНОВЛЕНИЕ СТРАНИЧКИ ПОЛЬЗОВАТЕЛЯ
class UpdateUser(UpdateView): #без отдельной формы
    model = get_user_model()
    fields = ['username', 'photo']
    template_name_suffix = 'update'

    def get_success_url(self):
        return reverse_lazy('account')



# class LoginUser(LoginView):
#     form_class = LoginUserForm  # стандартный класс формы фреймворка Django с набором определенных методов и атрибутов, кот. работает в связке с LoginView
#     template_name = 'users/login.html'
#
#
#     def get_success_url(self):
#         return reverse_lazy('account')  # при успешной авторизации перенаправление на страницу всех постов
#
#
# # РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ И ОТПРАВКА КОДА НА ПОЧТУ
# def registration(request):
#     if request.method == 'POST':
#         form = RegistrationUserForm(request.POST) #создаем форму с переданными в нее данными через POST
#         if form.is_valid():#если корректно заполнена форма, то
#             form.save()#создаем юзера без занесения в бд
#             return redirect('login')
#     else:
#         form = RegistrationUserForm()#если GET, то формируем пустую форму
#         return render(request, 'users/registration.html', {'form': form})
#
#
def account(request):
    return render(request, 'users/account.html')