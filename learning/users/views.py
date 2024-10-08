from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from learning import settings
from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, \
    UserPasswordChangeForm


class LoginUser(LoginView):
    """Отображение страницы входа для пользователя"""

    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': "Авторизация"}


class RegisterUser(CreateView):
    """Отображение страницы регистрации для нового пользователя"""

    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    """Отображение страницы редактирования профиля пользователя"""

    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': "Профиль пользователя",
                     'default_image': settings.DEFAULT_USER_IMAGE}

    def get_success_url(self):
        """Ссылка на страницу профиля"""
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        """Пользователь"""
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    """Отображение страницы смены пароля для пользователя"""

    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    extra_context = {'title': "Изменение пароля"}
    success_url = reverse_lazy('users:password_change_done')
