from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import *
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.password_validation import validate_password


# РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ
class UserRegistration(CreateView): #дополнительно хешировать пароль (преобразование информации с помощью особых математических формул)
    model = get_user_model()
    template_name = 'users/registration.html'
    fields = ['username', 'password', 'photo']
    success_url = reverse_lazy('login')

    # CreateView с полем password. Это напрямую сохраняет пароль в базе данных без хеширования, что нарушает процесс аутентификации. Django ожидает, что пароль будет хеширован через .set_password().
    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data['password']
        validate_password(password, user)  # Проверка сложности пароля (станд. валидатор Django для проверки сложности пароля)

        user.set_password(form.cleaned_data['password'])  # Хешируем пароль
        user.save()
        return super().form_valid(form)


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
    template_name = 'users/update.html'
    success_url = reverse_lazy('account')

# ФУНКЦИЯ ПРЕДСТАВЛЕНИЯ СТРАНИЧКИ ПОЛЬЗОВАТЕЛЯ
def account(request):
    return render(request, 'users/account.html')


class UserList(ListView):
    model = get_user_model()
    template_name = 'user_list.html'
    context_object_name = 'user_list'


#
#
