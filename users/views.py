import random
import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse

from django.views import View
from django.views.generic import CreateView, UpdateView

from config import settings
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class RegisterView(CreateView):
    """
    Отображение для регистрации нового пользователя.
    """
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        """
        Проверка валидности формы регистрации пользователя.
        Если форма валидна, сохраняется новый пользователь.
        Затем генерируется новый ключ для верификации,
        отправляется письмо с ключом и устанавливается активность пользователя в False.
        """
        self.object = form.save(commit=False)
        verification_key = str(uuid.uuid4())  # Генерация нового ключа
        self.object.verification_key = verification_key  # Сохранение ключа в поле "verification_key" у пользователя
        subject = 'Подтверждение регистрации'
        message = f'Привет! Вот твой ключ для верификации: {verification_key}'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [self.object.email])  # Отправка письма с ключом
        self.object.is_verified = False
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        """
        Получение URL-адреса успешного завершения регистрации.
        """
        return reverse('users:verify', args=(self.object.verification_key,))


class VerifyView(View):
    """
    Отображение для верификации пользователя по ключу.
    """

    def get(self, request, verification_key):
        """
        Проверка ключа верификации. Если ключ совпадает с ключом у пользователя,
        активируется аккаунт пользователя и ключ верификации удаляется.
        В противном случае выводится соответствующее сообщение.
        """
        user = get_object_or_404(User, verification_key=verification_key)
        if user.verification_key == verification_key:
            user.is_active = True
            user.verification_key = None
            user.save()
            return HttpResponse('Пользователь успешно верифицирован!')
        else:
            return HttpResponse('Неправильный ключ верификации. Попробуйте еще раз.')


class ProfileView(LoginRequiredMixin, UpdateView):
    """
    Отображение профиля пользователя.
    """
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('mailings:list')

    def get_object(self, queryset=None):
        """
        Получение объекта пользователя для отображения профиля.
        Если пользователь аутентифицирован, возвращается текущий пользователь.
        В противном случае осуществляется перенаправление на страницу списка рассылок.
        """
        if self.request.user.is_authenticated:
            return self.request.user
        else:
            return redirect(reverse('mailings:list'))


def generate_new_password(request):
    """
    Генерация нового пароля, отправка его на электронную почту пользователя
    и обновление пароля пользователя.
    """
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])  # генерируем новый пароль
    # из случайных цифр от 0 до 9 длинной в 12 символов
    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('mailings:list'))
