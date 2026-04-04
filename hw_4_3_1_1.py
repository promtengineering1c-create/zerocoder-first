# 1. Создайте базовый класс `Animal`, который будет содержать общие атрибуты (например, `name`, `age`) и методы (`make_sound()`, `eat()`) для всех животных.
# 2. Реализуйте наследование, создав подклассы `Bird`, `Mammal`, и `Reptile`, которые наследуют от класса `Animal`. Добавьте специфические атрибуты и переопределите методы, если требуется (например, различный звук для `make_sound()`).
# 3. Продемонстрируйте полиморфизм: создайте функцию `animal_sound(animals)`, которая принимает список животных и вызывает метод `make_sound()` для каждого животного.
# 4. Используйте композицию для создания класса `Zoo`, который будет содержать информацию о животных и сотрудниках. Должны быть методы для добавления животных и сотрудников в зоопарк.
# 5. Создайте классы для сотрудников, например, `ZooKeeper`, `Veterinarian`, которые могут иметь специфические методы (например, `feed_animal()` для `ZooKeeper` и `heal_animal()` для `Veterinarian`).
# Дополнительно:
# Попробуйте добавить дополнительные функции в вашу программу, такие как сохранение информации о зоопарке в файл и возможность её загрузки, чтобы у вашего зоопарка было "постоянное состояние" между запусками программы.

from __future__ import annotations
from typing import Protocol, runtime_checkable
import pickle
import json as jo

# region Протоколы
@runtime_checkable
class SoundMaker(Protocol):
    def make_sound(self) -> None:
        ...

@runtime_checkable
class Feeder(Protocol):
    def feed_animal(self, animal: Animals) -> None:
        ...

@runtime_checkable
class Healer(Protocol):
    def heal_animal(self, animal: Animals) -> None:
        ...    
                    
def activate_sound(obj: SoundMaker):
    obj.make_sound()

def feeding(obj: Feeder, animal: Animals):
    obj.feed_animal(animal)

def healing(obj: Healer, animal: Animals):
    obj.heal_animal(animal)
# endregion

# region Биологические типы и виды животныхё
class Bio_type:
    _name: str
    _kinds: list
    def __init__(self, name: str):
        self._name = name
        self._kinds = []

    class Bio_kind:
        _name: str
        _b_type: Bio_type
        def __init__(self, name: str, b_type: Bio_type):
            self._name = name
            self._b_type = b_type
            b_type._kinds.append(self)

type_birds = Bio_type("Птицы")
type_mammals = Bio_type("Млекопитающие")
type_reptiles = Bio_type("Пресмыкающиеся")

kind_nightingales = Bio_type.Bio_kind("Соловей", type_birds)
white_storks = Bio_type.Bio_kind("Белый журавль", type_birds)

kind_lions = Bio_type.Bio_kind("Лев", type_mammals)
kind_giraffes = Bio_type.Bio_kind("Жираф", type_mammals)

kind_turtles = Bio_type.Bio_kind("Черепаха", type_reptiles)
kind_gekkons = Bio_type.Bio_kind("Геккон", type_reptiles)
# endregion

# region Животные
class Animals:
    _b_type: Bio_type = None
    _b_kind: Bio_type.Bio_kind = None
    name: str
    age: int

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def eat(self) -> None:
        print(f"{self.name} is eating.")

class Birds(Animals):
    def __init__(self, name, age):
        super().__init__(name, age)
        self._bio_type = type_birds

class Mammals(Animals):
    def __init__(self, name, age):
        super().__init__(name, age)
        self._bio_type = type_mammals

class Reptiles(Animals):
    def __init__(self, name, age):
        super().__init__(name, age)
        self._bio_type = type_reptiles

class Nightingales(Birds):    
    def __init__(self, name, age):
        super().__init__(name, age)
        self._bio_kind = kind_nightingales

    def make_sound(self) -> None:
        print(f"{self.name} красиво поет.")   

class White_storks(Birds):
    def __init__(self, name, age):
        super().__init__(name, age)
        self._bio_kind = white_storks

class Lions(Mammals):    
    def __init__(self, name, age):
        super().__init__(name, age)
        self._bio_kind = kind_lions

    def make_sound(self) -> None:
        print(f"{self.name} рычит.")

class Giraffes(Mammals):
    def __init__(self, name, age):
        super().__init__(name, age)
        self._bio_kind = kind_giraffes

class Turtles(Reptiles):
    def __init__(self, name, age):
        super().__init__(name, age)
        self._bio_kind = kind_turtles

class Gekkons(Reptiles):
    def __init__(self, name, age):
        super().__init__(name, age)
        self._bio_kind = kind_gekkons

    def make_sound(self) -> None:
        print(f"{self.name} издает тихий звук.")            
# endregion

# region Зоопарк
class Employees:
    name: str
    position: str    
    def __init__(self, name: str):
        self.name = name

class ZooKeeper(Employees):
    def __init__(self, name: str):
        super().__init__(name)
        self.position = "Смотритель зоопарка"
    
    def feed_animal(self, animal: Animals) -> None:
        print(f"{self.name} кормит {animal.name}.")

class Veterinarian(Employees):
    def __init__(self, name: str):
        super().__init__(name)
        self.position = "Ветеринар"

    def heal_animal(self, animal: Animals) -> None:
        print(f"{self.name} лечит {animal.name}.")

class Zoo:
    _employees: list
    _animals: list
    def __init__(self):
        self._animals = []
        self._employees = []

    def add_animal(self, animal: Animals) -> None:
        self._animals.append(animal)

    def add_employee(self, employee: Employees) -> None:
        self._employees.append(employee)

    def get_animals(self) -> list:
        return self._animals
    
    def get_employees(self) -> list:
        return self._employees
    
    # def to_dict(self) -> dict:

class ZooDisplay(Protocol):
    def print_zoo_info(self, zoo: 'Zoo') -> None:
        ...

class ZooPrinter:
    def print_zoo_info(self, zoo: Zoo) -> None:
        print(f"Животные в зоопарке: {len(zoo.get_animals())}")
        for animal in zoo.get_animals():
            print(f"{animal.name} ({animal._bio_kind._name}) - {animal.age} лет")
        print(f"\nСотрудники зоопарка: {len(zoo.get_employees())}") 
        for employee in zoo.get_employees():
            print(f"{employee.name} - {employee.position}")  

class SaveData(Protocol):
    def save_zoo_data(self, zoo: 'Zoo') -> None:
        ...

    def load_zoo_data(self, zoo: 'Zoo') -> None:
        ...

class ZooFileDataManager:
    def __init__(self, filename: str):
        self.filename = filename

    def save_zoo_data(self, zoo: Zoo) -> None:
        with open(self.filename, "wb") as file:
            pickle.dump(zoo, file)

    def load_zoo_data(self) -> Zoo:
        with open(self.filename, "rb") as file:
            return pickle.load(file)            

# class ZooJsonManadgerData:
#     def __init__(self, filename: str):
#         self.filename = filename

#     def save_zoo_data(self, zoo: Zoo) -> None:
#         with open(self.filename, "w") as file:
#             jo.dump(zoo.to_dict(), file)

#     def load_zoo_data(self) -> Zoo:
#         with open(self.filename, "r") as file:
#             return jo.load(file)   
          
# endregion

# data_manager = ZooJsonManadgerData("zoo_data.json")
data_manager = ZooFileDataManager("zoo_data.pkl")
try:
    zoo = data_manager.load_zoo_data()
    print("Данные зоопарка загружены.")

except FileNotFoundError: 
    print("Данные зоопарка не найдены. Создан новый зоопарк.")

    zoo = Zoo()

    nightingale_1 = Nightingales("Соловей 1", 2)
    lion_alex = Lions("Алекс", 5)   
    gekkon_1 = Gekkons("Геккон 1", 1)

    zoo.add_animal(nightingale_1)
    zoo.add_animal(lion_alex)
    zoo.add_animal(gekkon_1)

    zoo_keeper = ZooKeeper("Гена")
    veterinarian = Veterinarian("Айболит")

    zoo.add_employee(zoo_keeper)
    zoo.add_employee(veterinarian)

    data_manager.save_zoo_data(zoo)
else:
    nightingale_1 = next(filter(lambda x: x.name == "Соловей 1", zoo._animals), None)
    lion_alex = next(filter(lambda x: x.name == "Алекс", zoo._animals), None)
    gekkon_1 = next(filter(lambda x: x.name == "Геккон 1", zoo._animals), None)

    zoo_keeper = next(filter(lambda x: x.name == "Гена", zoo._employees), None)
    veterinarian = next(filter(lambda x: x.name == "Айболит", zoo._employees), None)        

printer = ZooPrinter()
printer.print_zoo_info(zoo)

activate_sound(nightingale_1)
activate_sound(lion_alex)
activate_sound(gekkon_1)

feeding(zoo_keeper, nightingale_1)
healing(veterinarian, lion_alex)
