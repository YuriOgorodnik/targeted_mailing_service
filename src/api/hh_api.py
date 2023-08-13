# Импортируем библиотеку requests
import requests

# Выбираем десять компаний с hh.ru, от которых будем получать данные об имеющихся у них вакансиях по API.
employers = ['ООО Замок-Сервис', 'ООО ДАКС-Драйв', 'ООО Омега', 'ООО АЛАНТЕРА', 'ООО Компания Интерлогистика',
             'ООО Сити Логистик', 'Performance Group', 'ООО СДЭК 21 Век', 'АО НВБС', 'ООО AVPOWER'
             ]

# Создаем класс HeadHunterAPI для работы с API сайта hh.ru
class HeadHunterAPI:
    def __init__(self):
        self.base_url = "https://api.hh.ru"  # Базовый URL для работы с API

    def get_vacancies(self, employer):
        """
        Метод для получения вакансий по заданному работодателю.
        :param employer: Название работодателя.
        :return: Список вакансий.
        """

        url = f"{self.base_url}/vacancies?employer={employer}"
        response = requests.get(url)
        data = response.json()
        vacancies = data.get('items', [])  # Получаем список вакансий из ответа API
        return vacancies

    def get_employer_data(self, employers):
        """
        Метод для получения данных о работодателях и их вакансиях.
        :param employers: Список работодателей.
        :return: Словарь с данными о работодателях и их вакансиях.
        """

        employer_data = {}
        for employer in employers:
            vacancies = self.get_vacancies(employer)  # Получаем вакансии для каждого работодателя
            employer_data[employer] = vacancies  # Сохраняем данные о работодателе и его вакансиях в словарь
        return employer_data
