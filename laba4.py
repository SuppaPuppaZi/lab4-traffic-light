from traffic_light_history import *
from traffic_light_iterator import *

history = SmartTrafficLightHistory.load_file('data.csv')

if len(history) == 0:
    print("Нет данных для работы.")
    exit()

while True:
    print("1. Показать все данные")
    print("2. Сортировка по дате/времени включения (строковое поле)")
    print("3. Сортировка по количеству проехавших автомобилей (числовое поле)")
    print("4. Фильтрация (ожидало меньше 10 автомобилей)")
    print("5. Добавить новую запись")
    print("6. Сохранить данные в файл")
    print("7. Доступ по индексу (__getitem__)")
    print("8. Итерация по записям (итератор)")
    print("9. Генератор информации о машинах(ожидающих, проехавших)")
    print("0. Выход")
    
    choice = input("\nВыберите опцию: ")
    
    if choice == '1':
        history.print_info()
        
    elif choice == '2':
        sorted_records = history.get_sorted_by_start_datetime()
        history.print_info(records=sorted_records, title="Сортировка по полю: start_datetime")
        
    elif choice == '3':
        sorted_records = history.get_sorted_by_cars_passed()
        history.print_info(records=sorted_records, title="Сортировка по полю: cars_passed")
        
    elif choice == '4':
        filtered = history.filter_by_waiting_cars()
        history.print_info(records=filtered, title="Фильтрация: cars_waiting < 10")
        
    elif choice == '5':
        print("\nФормат даты и времени: ГГГГ-ММ-ДД ЧЧ:ММ:СС")
        start = input("Дата и время включения: ")
        end = input("Дата и время выключения: ")
        
        if not SmartTrafficLightHistory.validate_datetime(start):
            print("Ошибка: Неверный формат даты/времени включения")
            continue
        if not SmartTrafficLightHistory.validate_datetime(end):
            print("Ошибка: Неверный формат даты/времени выключения")
            continue
        
        try:
            passed = int(input("Количество проехавших автомобилей: "))
            waiting = int(input("Количество автомобилей в ожидании: "))
            
            if passed < 0 or waiting < 0:
                print("Ошибка. Значения не могут быть отрицательными")
                continue
            
            new_id = len(history) + 1
            new_record = TrafficLightRecord(new_id, start, end, passed, waiting)
            history.add_record(new_record)
            print(f"Запись #{new_id} успешно добавлена")
        except ValueError:
            print("Ошибка. Введите корректные числовые значения")
            
    elif choice == '6':
        SmartTrafficLightHistory.save_file(history)
        
    elif choice == '7':
        try:
            print(f"\nВсего записей: {len(history)}")
            index = int(input(f"Введите индекс: от 0 до {len(history)-1}:"))
            print(f"\nЗапись по индексу {index}:")
            print(history.__getitem__(index))
        except IndexError:
            print("Ошибка: Индекс вне диапазона")
        except ValueError:
            print("Ошибка: Введите целое число")
                    
    elif choice == '8':
        print("\nИтерация по записям:")
        iterator = TrafficLightIterator(history.get_all_records())
        for record in iterator:
            print(record)
            
    elif choice == '9':
        print("\nГенератор информации о машинах:")
        for line in history.generate_car_info():
            print(f"  {line}")
            
    elif choice == '0':
        break
    else:
        print("Такой опции нет.")
