import json
from datetime import datetime

class Record:
    def __init__(self, date, time, description):
        self.date = date
        self.time = time
        self.description = description

class NotebookModel:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_records_for_day(self, date):
        return [record for record in self.records if record.date == date]

    def delete_record(self, date, time, description):
        self.records = [record for record in self.records if not (
            record.date == date and record.time == time and record.description == description
        )]

    def sort_records(self):
        self.records.sort(key=lambda x: (x.date, x.time))

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            records_data = [record.__dict__ for record in self.records]
            json.dump(records_data, file)

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            records_data = json.load(file)
            self.records = [Record(record['date'], record['time'], record['description']) for record in records_data]

class NotebookView:
    def show_records(self, records):
        if not records:
            print("Записей нет")
        else:
            for record in records:
                print(f"Дата: {record.date}, Время: {record.time}, Описание: {record.description}")

    def get_user_input(self, prompt):
        return input(prompt)

class NotebookPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def add_record(self, date, time, description):
        record = Record(date, time, description)
        self.model.add_record(record)

    def show_records_for_day(self, date):
        records = self.model.get_records_for_day(date)
        self.view.show_records(records)

    def delete_record(self, date, time, description):
        self.model.delete_record(date, time, description)

    def sort_records(self):
        self.model.sort_records()

    def save_to_file(self, filename):
        self.model.save_to_file(filename)

    def load_from_file(self, filename):
        self.model.load_from_file(filename)

class NotebookController:
    def __init__(self):
        self.model = NotebookModel()
        self.view = NotebookView()
        self.presenter = NotebookPresenter(self.model, self.view)

    def run(self):
        while True:
            print("\n1. Добавить запись")
            print("2. Показать записи на день")
            print("3. Удалить запись")
            print("4. Сортировать записи")
            print("5. Сохранить в файл")
            print("6. Загрузить из файла")
            print("7. Выход")
            choice = self.view.get_user_input("Выберите действие: ")

            if choice == "1":
                date = self.view.get_user_input("Введите дату (ГГГГ-ММ-ДД): ")
                time = self.view.get_user_input("Введите время (ЧЧ:ММ): ")
                description = self.view.get_user_input("Введите описание: ")
                self.presenter.add_record(date, time, description)
            elif choice == "2":
                date = self.view.get_user_input("Введите дату (ГГГГ-ММ-ДД): ")
                self.presenter.show_records_for_day(date)
            elif choice == "3":
                date = self.view.get_user_input("Введите дату (ГГГГ-ММ-ДД) записи для удаления: ")
                time = self.view.get_user_input("Введите время (ЧЧ:ММ) записи для удаления: ")
                description = self.view.get_user_input("Введите описание записи для удаления: ")
                self.presenter.delete_record(date, time, description)
            elif choice == "4":
                self.presenter.sort_records()
            elif choice == "5":
                filename = self.view.get_user_input("Введите имя файла для сохранения: ")
                self.presenter.save_to_file(filename)
            elif choice == "6":
                filename = self.view.get_user_input("Введите имя файла для загрузки: ")
                self.presenter.load_from_file(filename)
            elif choice == "7":
                break
            else:
                print("Некорректный ввод. Пожалуйста, выберите существующий пункт меню.")

if __name__ == "__main__":
    controller = NotebookController()
    controller.run()
