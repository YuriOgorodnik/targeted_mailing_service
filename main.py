from src.utils.DB_Manager import DBManager
from config import host, database, user, password

# Создаем экземпляр класса DBManager
db_manager = DBManager(host, database, user, password)

# Прописываем интерактив с пользователем для выборки данных из созданной нами базы данных
print("ДОБРОГО ВРЕМЕНИ СУТОК, УВАЖАЕМЫЙ ПОЛЬЗОВАТЕЛЬ!!!\nВас приветствует платформа получения информации из базы данных\n"
    "о десяти компаниях с сайта hh.ru и имеющихся у них вакансиях")
print("--------------------------------------------------------------")
print("Нажмите 1: Для получения списка всех компаний и количества вакансий у каждой компании;")
print("Нажмите 2: Для получения списка всех вакансий с названием компании, названием вакансии, зарплаты и ссылки на вакансию;")
print("Нажмите 3: Для получения средней зарплаты по всем имеющимся вакансиям;")
print("Нажмите 4: Для получения списка всех вакансий, у которых зарплата выше средней по всем имеющимся вакансиям;")
print("Нажмите 5: Для получения списка всех вакансий, в названии которых содержатся переданные в метод слова (например менеджер);")
print("Нажмите 0: Для ВЫХОДА из программы")
print()
choice = int(input("Пожалуйста, сделайте Ваш выбор путем ввода необходимой цифры: "))
print()

# В зависимости от выбора пользователя выводим необходимую информацию из базы данных на экран
if choice == 1:
    companies_and_vacancies = db_manager.get_companies_and_vacancies_count()
    print(companies_and_vacancies)
elif choice == 2:
    all_vacancies = db_manager.get_all_vacancies()
    print(all_vacancies)
elif choice == 3:
    avg_salary = db_manager.get_avg_salary()
    print(avg_salary)
elif choice == 4:
    vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
    print(vacancies_with_higher_salary)
elif choice == 5:
    vacancies_with_keyword = db_manager.get_vacancies_with_keyword('менеджер')
    print(vacancies_with_keyword)
elif choice == 0:
    exit()
else:
    print("Вами введены не верные данные!")
