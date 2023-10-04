import json

from django.contrib.auth.models import Group
from django.core.management import BaseCommand

from config.settings import BASE_DIR
from users.models import User


class Command(BaseCommand):
    """
    Пользовательская команда управления Django для создания администратора
    и импорта групп из JSON-фикстуры.
    """
    def handle(self, *args, **options):
        """
        Выполняет логику команды управления.
        """
        # Создание администратора
        user = User.objects.create(
            email='admin@yuri.com',
            first_name='Admin',
            last_name='SkyPro',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('123')  # Установка пароля для пользователя
        user.save()  # Сохранение пользователя в базе данных

        # Импорт групп из JSON-фикстуры
        with open(BASE_DIR / 'users/fixtures/groups_fixture.json', 'r', encoding='cp1251') as file:
            group_data = json.load(file)  # Загрузка данных JSON из файла
            for item in group_data:
                # Создание объекта группы и установка ее атрибутов
                group = Group.objects.create(
                    pk=item['pk'],
                    name=item['fields']['name'],
                )
                group.permissions.set(item['fields']['permissions'])  # Установка прав доступа для группы

