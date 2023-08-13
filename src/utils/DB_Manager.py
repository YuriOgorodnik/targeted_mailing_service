import psycopg2

# Создаем класс DBManager, который будет подключаться к базе данных и работать с данными
class DBManager:
    def __init__(self, host, database, user, password):
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        self.cur = self.conn.cursor()

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def get_companies_and_vacancies_count(self) -> list:
        """
         Метод получения списка всех компаний
         и количества вакансий у каждой компании
        """
        query = '''
            SELECT employers.employer_name, COUNT(vacancies.vacancy_id)
            FROM employers
            LEFT JOIN vacancies ON employers.employer_id = vacancies.employer_id
            GROUP BY employers.employer_name
        '''
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_all_vacancies(self) -> list:
        """
        Метод получения списка всех вакансий
        с указанием названия компании,
        названия вакансии, зарплаты по вакансии
        и ссылки на вакансию
        """
        query = '''
            SELECT employers.employer_name, vacancies.vacancy_name, vacancies.salary, vacancies.vacancy_link
            FROM employers
            INNER JOIN vacancies ON employers.employer_id = vacancies.employer_id
        '''
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_avg_salary(self) -> float:
        """
        Метод получения средней зарплаты
        по всем имеющимся вакансиям
        """
        query = '''
            SELECT AVG(salary)
            FROM vacancies
        '''
        self.cur.execute(query)
        return float(self.cur.fetchone()[0])

    def get_vacancies_with_higher_salary(self) -> list:
        """
        Метод получения списка всех вакансий,
        у которых зарплата выше средней по всем вакансиям
        """
        avg_salary = self.get_avg_salary()
        query = '''
            SELECT vacancies.vacancy_name, vacancies.salary, vacancies.vacancy_link
            FROM vacancies
            WHERE vacancies.salary > %s
        '''
        self.cur.execute(query, (avg_salary,))
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword) -> list:
        """
        Метод получения списка всех вакансий,
        в названии которых содержатся переданные в метод слова (например менеджер)
        """
        query = '''
            SELECT employers.employer_name, vacancies.vacancy_name, vacancies.salary, vacancies.vacancy_link
            FROM employers
            INNER JOIN vacancies ON employers.employer_id = vacancies.employer_id
            WHERE vacancies.vacancy_name ILIKE %s
        '''
        self.cur.execute(query, ('%' + keyword + '%',))
        return self.cur.fetchall()
