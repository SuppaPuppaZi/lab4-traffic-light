import csv
import os
from datetime import datetime

class TrafficLightRecord:
    def __init__(self, record_id, start_datetime, end_datetime, cars_passed, cars_waiting):
        self.__setattr__('_id', record_id)
        self.__setattr__('_start_datetime', start_datetime)
        self.__setattr__('_end_datetime', end_datetime)
        self.__setattr__('_cars_passed', cars_passed)
        self.__setattr__('_cars_waiting', cars_waiting)
    
    @property
    def id(self):
        return self._id
    
    @property
    def start_datetime(self):
        return self._start_datetime
    
    @property
    def end_datetime(self):
        return self._end_datetime
    
    @property
    def cars_passed(self):
        return self._cars_passed
    
    @property
    def cars_waiting(self):
        return self._cars_waiting
    
    def __repr__(self):
        return (f"TrafficLightRecord(id={self._id}, start='{self._start_datetime}', "
                f"end='{self._end_datetime}', passed={self._cars_passed}, "
                f"waiting={self._cars_waiting})")
    
    def __str__(self):
        return (f"{self._id:<4} {self._start_datetime:<25} {self._end_datetime:<25} "
                f"{self._cars_passed:<10} {self._cars_waiting:<10}")

class TrafficLightHistory:
    
    def __init__(self):
        self._records = []
    
    def add_record(self, record):
        self._records.append(record)
    
    def __len__(self):
        return len(self._records)
    
    def __getitem__(self, index):
        return self._records[index]
    
    def __iter__(self):
        return TrafficLightIterator(self._records)
    
    def get_all_records(self):
        return self._records
    
    @staticmethod
    def validate_datetime(datetime_str):
        try:
            datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            return True
        except ValueError:
            return False


class SmartTrafficLightHistory(TrafficLightHistory):
    
    def get_sorted_by_start_datetime(self):
		print("Сортировка\n")
        return sorted(self._records, key=lambda x: x.start_datetime)
    
    def get_sorted_by_cars_passed(self):
        return sorted(self._records, key=lambda x: x.cars_passed)
    
    def filter_by_waiting_cars(self):
        return [record for record in self._records if record.cars_waiting < 10]
    
    def generate_car_info(self):
        for record in self._records:
            yield f"Запись #{record.id}: Проехало: {record.cars_passed}, Ожидало: {record.cars_waiting}"
    
    def print_info(self, records=None, title="Данные"):
        if records is None:
            records = self._records
        
        if not records:
            print("Нет данных для отображения.")
            return
        
        print(f'\n{title}\n')
        print(f"{'ID':<4} {'Дата/время включения':<25} {'Дата/время выключения':<25} "
              f"{'Проехало':<10} {'В ожидании':<10}")
        
        for record in records:
            print(record)
    
    @staticmethod
    def load_file(filename):
        history = SmartTrafficLightHistory()
        
        if not os.path.exists(filename):
            print(f"Файл {filename} не найден.")
            return history
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=',')
                for row in reader:
                    record = TrafficLightRecord(
                        record_id=int(row['id']),
                        start_datetime=row['start_datetime'],
                        end_datetime=row['end_datetime'],
                        cars_passed=int(row['cars_passed']),
                        cars_waiting=int(row['cars_waiting'])
                    )
                    history.add_record(record)
            print(f"Загружено {len(history)} записей из файла {filename}")
        except Exception as e:
            print(f"Ошибка при загрузке файла: {e}")
        
        return history
    
    @staticmethod
    def save_file(history, filename='data.csv'):
        try:
            with open(filename, 'w', encoding='utf-8', newline='') as file:
                fieldnames = ['id', 'start_datetime', 'end_datetime', 'cars_passed', 'cars_waiting']
                writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=',')
                writer.writeheader()
                for record in history.get_all_records():
                    writer.writerow({
                        'id': record.id,
                        'start_datetime': record.start_datetime,
                        'end_datetime': record.end_datetime,
                        'cars_passed': record.cars_passed,
                        'cars_waiting': record.cars_waiting
                    })
            print(f"Данные успешно сохранены в файл {filename}")
            return True
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")
            return False
