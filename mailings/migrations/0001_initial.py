# Generated by Django 4.2.5 on 2023-10-02 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='электронная почта')),
                ('full_name', models.CharField(max_length=100, verbose_name='ФИО')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='комментарий')),
            ],
            options={
                'verbose_name': 'клиент',
                'verbose_name_plural': 'клиенты',
            },
        ),
        migrations.CreateModel(
            name='MailingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(verbose_name='Дата и время начала рассылки')),
                ('end_date', models.DateTimeField(verbose_name='Дата и время окончания рассылки')),
                ('frequency', models.CharField(choices=[('daily', 'Раз в день'), ('weekly', 'Раз в неделю'), ('monthly', 'Раз в месяц')], max_length=15, verbose_name='периодичность рассылки')),
                ('status', models.CharField(choices=[('completed', 'Завершена'), ('created', 'Создана'), ('started', 'Запущена')], default='created', max_length=10, verbose_name='статус рассылки')),
                ('recipients', models.ManyToManyField(to='mailings.client', verbose_name='получатели')),
            ],
            options={
                'verbose_name': 'рассылка',
                'verbose_name_plural': 'рассылки',
            },
        ),
        migrations.CreateModel(
            name='MailingMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255, verbose_name='тема письма')),
                ('body', models.TextField(verbose_name='тело письма')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailings.mailinglist', verbose_name='рассылка')),
            ],
            options={
                'verbose_name': 'сообщение',
                'verbose_name_plural': 'сообщения',
            },
        ),
        migrations.CreateModel(
            name='MailingLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_attempt_datetime', models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')),
                ('status', models.CharField(max_length=20, verbose_name='статус попытки')),
                ('server_response', models.TextField(blank=True, null=True, verbose_name='ответ почтового сервера')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailings.mailingmessage')),
            ],
            options={
                'verbose_name': 'лог',
                'verbose_name_plural': 'логи',
            },
        ),
    ]
