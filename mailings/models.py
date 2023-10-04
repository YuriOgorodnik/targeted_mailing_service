from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='электронная почта')
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    comment = models.TextField(verbose_name='комментарий', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='пользователь', null=True, blank=True)

    def __str__(self):
        return (f'{self.full_name} ({self.email})')

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class MailingList(models.Model):
    start_date = models.DateTimeField(verbose_name='Дата и время начала рассылки')
    end_date = models.DateTimeField(verbose_name='Дата и время окончания рассылки')
    frequency_choices = (
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    )
    frequency = models.CharField(max_length=15, choices=frequency_choices, verbose_name='периодичность рассылки')
    status_choices = (
        ('completed', 'Завершена'),
        ('created', 'Создана'),
        ('started', 'Запущена'),
    )
    status = models.CharField(max_length=10, choices=status_choices, default='created', verbose_name='статус рассылки')
    recipients = models.ManyToManyField(Client, verbose_name='получатели')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return f'{self.get_frequency_display()} рассылка ({self.get_status_display()})'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class MailingMessage(models.Model):
    mailing = models.ForeignKey(MailingList, on_delete=models.CASCADE, verbose_name='рассылка')
    subject = models.CharField(max_length=255, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='пользователь', null=True, blank=True)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class MailingLog(models.Model):
    last_attempt_datetime = models.DateTimeField(verbose_name='дата и время последней попытки', auto_now_add=True)
    status = models.CharField(max_length=20, verbose_name='статус попытки')
    server_response = models.TextField(verbose_name='ответ почтового сервера', null=True, blank=True)

    message = models.ForeignKey(MailingMessage, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.message} - {self.status}'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
