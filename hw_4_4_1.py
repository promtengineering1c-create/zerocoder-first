# Задание: Применение Принципа Открытости/Закрытости (Open/Closed Principle) в Разработке Простой Игры

# Цель: Цель этого домашнего задание - закрепить понимание и навыки применения принципа открытости/закрытости (Open/Closed Principle), одного из пяти SOLID принципов объектно-ориентированного программирования. Принцип гласит, что программные сущности (классы, модули, функции и т.д.) должны быть открыты для расширения, но закрыты для модификации.

# Задача: Разработать простую игру, где игрок может использовать различные типы оружия для борьбы с монстрами. Программа должна быть спроектирована таким образом, чтобы легко можно было добавлять новые типы оружия, не изменяя существующий код бойцов или механизм боя.

# Исходные данные:

# Есть класс Fighter, представляющий бойца.
# Есть класс Monster, представляющий монстра.
# Игрок управляет бойцом и может выбирать для него одно из вооружений для боя.
# Шаг 1: Создайте абстрактный класс для оружия

# Создайте абстрактный класс Weapon, который будет содержать абстрактный метод attack().
# Шаг 2: Реализуйте конкретные типы оружия

# Создайте несколько классов, унаследованных от Weapon, например, Sword и Bow. Каждый из этих классов реализует метод attack() своим уникальным способом.
# Шаг 3: Модифицируйте класс Fighter

# Добавьте в класс Fighter поле, которое будет хранить объект класса Weapon.
# Добавьте метод change_weapon(), который позволяет изменить оружие бойца.
# Шаг 4: Реализация боя

# Реализуйте простой механизм для демонстрации боя между бойцом и монстром, исходя из выбранного оружия.
# Требования к заданию:

# Код должен быть написан на Python.
# Программа должна демонстрировать применение принципа открытости/закрытости: новые типы оружия можно легко добавлять, не изменяя существующие классы бойцов и механизм боя.
# Программа должна выводить результат боя в консоль.

from __future__ import annotations
from abc import ABC, abstractmethod

def deal_damage(damage: int, monster: Monster):
        monster.health -= damage
        if monster.health <= 0:
            print(f"{monster.name} убит")
        else:
            print(f"{monster.name} осталось {monster.health} здоровья")

class Fighter():
    name: str
    weapon: Weapon
    def __init__(self, name):
        self.name = name
        self.weapon = None
    def change_weapon(self, weapon: Weapon):
        self.weapon = weapon

class Monster():
    name: str
    health: int
    def __init__(self, name, health = 100):
        self.name = name
        self.health = health

class Weapon(ABC):
    name: str
    damage: int
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

    @abstractmethod
    def attack(self):
        pass

class Sling(Weapon):
    def __init__(self, name = "праща", damage = 1):        
        super().__init__(name, damage)

    def attack(self, fighter: Fighter, monster: Monster):
        print(f"{fighter.name} взмахнул {self.name} и нанес {monster.name} урон {self.damage}") 
        deal_damage(self.damage, monster)
        
class Mace(Weapon):
    def __init__(self, name = "палица", damage = 2):        
        super().__init__(name, damage)

    def attack(self, fighter: Fighter, monster: Monster):
        print(f"{fighter.name} ударил {self.name} и наносит {monster.name} урон {self.damage}") 
        deal_damage(self.damage, monster)

class Sword(Weapon):
    def __init__(self, name = "меч", damage = 5):        
        super().__init__(name, damage)

    def attack(self, fighter: Fighter, monster: Monster):
        print(f"{fighter.name} вонзил свой {self.name} в {monster.name} и наносит урон {self.damage}") 
        deal_damage(self.damage, monster)

class Bow(Weapon):
    def __init__(self, name = "лук", damage = 2):        
        super().__init__(name, damage)

    def attack(self, fighter: Fighter, monster: Monster):
        print(f"{fighter.name} выстрелил из {self.name} и {monster.name} получил урон {self.damage}") 
        deal_damage(self.damage, monster)

robin = Fighter("Робин")
print(f"Боец {robin.name} готов к бою")

robin.change_weapon(Sword("Меч кладенец", 10))
print(f"Боец {robin.name} выбрал {robin.weapon.name}с силой {robin.weapon.damage}")

shrek = Monster("Шрек")
print(f"Появился {shrek.name}")
robin.weapon.attack(robin, shrek)
robin.weapon.attack(robin, shrek)

robin.change_weapon(Mace())
print(f"Боец {robin.name} выбрал {robin.weapon.name}  с силой {robin.weapon.damage}")
robin.weapon.attack(robin, shrek)
robin.weapon.attack(robin, shrek)
robin.weapon.attack(robin, shrek)

robin.change_weapon(Bow())
print(f"Боец {robin.name} выбрал {robin.weapon.name}с силой {robin.weapon.damage}")
robin.weapon.attack(robin, shrek)