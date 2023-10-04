from random import sample

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import ModelForm
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from pytils.translit import slugify

from blogs.models import Blog
from mailings.models import Client, MailingList, MailingLog, MailingMessage
from mailings.utils import send_mailing, schedule_mailing


def index(request):
    """
    Главная страница приложения mailings.
    """
    count_mailing = len(MailingList.objects.all())
    active_mailing_count = len(MailingList.objects.filter(status__in=['started', 'created']))
    unic_client_count = len(Client.objects.all())
    all_posts = list(Blog.objects.all())
    random_blog_posts = sample(all_posts, min(3, len(all_posts)))
    context = {
        'count_mailing': count_mailing,
        'active_mailing_count': active_mailing_count,
        'unic_client_count': unic_client_count,
        'random_blog_posts': random_blog_posts
    }
    return render(request, 'mailings/index.html', context)


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Класс представления для создания клиента.
    """
    model = Client
    fields = ('full_name', 'email',)
    permission_required = 'mailings.add_client'
    success_url = reverse_lazy('clients:list')

    def form_valid(self, form):
        """
        Переопределение метода form_valid для обработки данных формы.
        """
        response = super().form_valid(form)
        if form.is_valid():
            self.object.slug = slugify(self.object.full_name)
            self.object.save()
        return response


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Класс представления для обновления клиента.
    """
    model = Client
    fields = ('full_name', 'email',)
    permission_required = 'mailings.change_client'
    success_url = reverse_lazy('clients:list')

    def form_valid(self, form):
        """
        Переопределение метода form_valid для обработки данных формы.
        """
        response = super().form_valid(form)
        if form.is_valid():
            self.object.slug = slugify(self.object.full_name)
            self.object.save()
        return response

    def get_success_url(self):
        """
        Возвращает URL страницы клиента после успешного обновления.
        """
        return reverse('clients:clients_view', args=[self.kwargs.get('pk')])


class ClientListView(LoginRequiredMixin, ListView):
    """
    Класс представления для отображения списка клиентов.
    """
    model = Client


class ClientDetailView(LoginRequiredMixin, DetailView):
    """
    Класс представления для отображения клиента.
    """
    model = Client

    def get_object(self, queryset=None):
        """
        Получает объект клиента.
        Перед возвратом объекта клиента, сохраняет его в базе данных.
        """
        self.object = super().get_object(queryset)
        self.object.save()
        return self.object


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Класс представления для удаления клиента.
    """
    model = Client
    permission_required = 'mailings.delete_client'
    success_url = reverse_lazy('clients:list')


class MailingListCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Класс представления для создания рассылки.
    """
    model = MailingList
    fields = ('start_date', 'end_date', 'frequency', 'status', 'recipients',)
    permission_required = 'mailings.add_mailinglist'

    def form_valid(self, form):
        """
        Проверяет, что форма допустима, сохраняет объект рассылки
        и устанавливает текущего пользователя в качестве владельца списков рассылки.
        """
        mailing_list = form.save(commit=False)
        mailing_list.user = self.request.user
        mailing_list.save()
        return super().form_valid(form)

    def get_success_url(self):
        """
        Возвращает URL перехода после успешного создания рассылки.
        """
        return reverse_lazy('mailings:message_create', kwargs={'mailing_pk': self.object.pk})


class MailingListListView(LoginRequiredMixin, ListView):
    """
    Класс представления для просмотра списка рассылок.
    """
    model = MailingList


class MailingListDetailView(LoginRequiredMixin, DetailView):
    """
    Класс представления для просмотра конкретной рассылки.
    """
    model = MailingList

    def get_success_url(self):
        """
        Возвращает URL перехода после успешного просмотра рассылки.
        """
        return reverse_lazy('mailings:message_view')


class MailingLogListView(LoginRequiredMixin, ListView):
    """
    Класс представления для просмотра статистики рассылки.
    """
    model = MailingLog


class MailingMessageForm(LoginRequiredMixin, ModelForm):
    """
    Форма для создания рассылки.
    """

    class Meta:
        model = MailingMessage
        fields = ('subject', 'body')


class MailingMessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Класс для создания новых сообщений рассылки.
    """

    model = MailingMessage
    form_class = MailingMessageForm
    permission_required = 'mailings.add_mailingmessage'
    success_url = reverse_lazy('mailings:list')

    def form_valid(self, form):
        """
        Функция вызывается, когда форма валидна. Сохраняет сообщение рассылки и выполняет соответствующие действия в зависимости от даты рассылки.
        """

        # Получение объекта рассылки по переданному идентификатору (mailing_pk)
        mailing = get_object_or_404(MailingList, pk=self.kwargs['mailing_pk'])

        # Сохранение сообщения рассылки, связывание рассылки с текущим пользователем
        mailing_message = form.save(commit=False)
        mailing_message.mailing = mailing
        mailing_message.user = self.request.user
        mailing_message.save()

        # Получение текущего времени
        current_time = timezone.now()

        # Если текущее время находится в диапазоне между датой начала и окончания рассылки,
        # вызываем функцию отправки сообщения рассылки
        if mailing.start_date <= current_time <= mailing.end_date:
            send_mailing(mailing_message.pk)

        # Если дата начала рассылки больше текущего времени,
        # вызываем функцию планирования отправки сообщения рассылки
        if mailing.start_date > current_time:
            schedule_mailing(mailing_message.pk, mailing.start_date)

        return super().form_valid(form)


class MailingMessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Класс представления для обновления рассылки.
    """

    model = MailingMessage
    fields = ('subject', 'body',)
    permission_required = 'mailings.change_mailingmessage'
    success_url = reverse_lazy('mailings:list')

    def form_valid(self, form):
        pk = self.kwargs['pk']
        mailing = get_object_or_404(MailingList, pk=pk)
        message = form.save(commit=False)
        message.mailing = mailing
        message.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        """
        Метод возвращает параметры для создания формы.
        Устанавливает начальное значение поля user равным текущему пользователю.
        """

        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'user': self.request.user}
        return kwargs

    def get_object(self, queryset=None):
        """
        Метод возвращает сообщение рассылки, которое будет редактироваться.
        Если пользователь не автор сообщения и не является менеджером,
        вызывается исключение.
        """

        message = super().get_object(queryset)
        message = get_object_or_404(MailingMessage, id=message.pk)
        user_groups = [group.name for group in self.request.user.groups.all()]
        if message.user != self.request.user and 'manager' not in user_groups:
            raise Http404
        return message


class MailingMessageDetailView(LoginRequiredMixin, DetailView):
    """
    Класс представления для просмотра деталей сообщения рассылки.
    """
    model = MailingMessage

class MailingMessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Класс представления для удаления сообщения рассылки..
    """
    model = MailingMessage
    permission_required = 'mailings.delete_mailingmessage'
    success_url = reverse_lazy('mailings:list')

    def delete(self, request, *args, **kwargs):
        """
        Переопределение метода delete() для удаления сообщения рассылки.
        """
        mailing_pk = self.kwargs['pk']
        mailing = self.get_object()
        mailing.delete()
        return super().delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """
        Переопределение метода get_object() для получения объекта сообщения рассылки.
        """
        message = super().get_object(queryset)
        message = get_object_or_404(MailingMessage, id=message.pk)
        user_groups = [group.name for group in self.request.user.groups.all()]
        if message.user != self.request.user and 'manager' not in user_groups:
            raise Http404
        print(message.user)
        return message
