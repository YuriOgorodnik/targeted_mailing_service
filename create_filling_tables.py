import psycopg2
from config import host, database, user, password
from src.api.hh_api import HeadHunterAPI, employers

# Устанавливаем соединение с базой данных
conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password
)

# Создаем курсор для выполнения SQL-запросов
cur = conn.cursor()

# Создаем таблицу для работодателей
cur.execute("""
    CREATE TABLE employers (
        employer_id SERIAL PRIMARY KEY,
        employer_name VARCHAR(255) NOT NULL
    )
""")

# Создаем таблицу для вакансий
cur.execute("""
    CREATE TABLE vacancies (
        vacancy_id SERIAL PRIMARY KEY,
        employer_id INT NOT NULL,
        vacancy_name VARCHAR(255) NOT NULL,
        salary INT NOT NULL,
        vacancy_link VARCHAR(255) NOT NULL,
        FOREIGN KEY (employer_id) REFERENCES employers (employer_id)
    )
""")

# С помощью метода класса  HeadHunterAPI заполняем таблицы employers и vacancies данными
hh = HeadHunterAPI()
employer_data = hh.get_employer_data(employers)

for employer, vacancies in employer_data.items():
    # Вставка данных работодателя в таблицу employers
    cur.execute('''
        INSERT INTO employers (employer_name)
        VALUES (%s)
        RETURNING employer_id
    ''', (employer,))
    employer_id = cur.fetchone()[0]  # получаем ID добавленного работодателя

    for vacancy in vacancies:
        vacancy_name = vacancy.get('name')
        salary = vacancy.get('salary', {}).get('from', 0) if vacancy.get('salary') else 0
        vacancy_link = vacancy.get('alternate_url')

        # Вставка данных вакансии в таблицу vacancies
        cur.execute('''
                INSERT INTO vacancies (employer_id, vacancy_name, salary, vacancy_link)
                VALUES (%s, %s, %s, %s)
            ''', (employer_id, vacancy_name, salary, vacancy_link))

# Фиксируем сделанные нами изменения в базе данных
conn.commit()

# Закрываем соединения
cur.close()
conn.close()
