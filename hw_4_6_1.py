from __future__ import annotations
from abc import ABC, abstractmethod
from random import choice

def deal_attack(obj1, obj2):
    obj1.attack(obj2)

class Hero(ABC):
    name: str
    __health: int
    __shot_power: int
    
    def __init__(self, health = 100, shot_power = 20):
        self.__health = health
        self.__shot_power = shot_power

    @property
    def health(self):   
        return self.__health

    @property
    def shot_power(self):
        return self.__shot_power

    @property
    def is_alive(self) -> bool:
        return self.__health > 0

    def attack(self, other: Hero):
        other.take_damage(self.__shot_power)    

    def take_damage(self, shot_power: int) -> None:
        self.__health -= shot_power

class Player(Hero):
    def __init__(self, health = 100, shot_power = 20):
        super().__init__(health, shot_power)
        self.name = "Player"

class Computer(Hero):
    def __init__(self, health = 100, shot_power = 20):
        super().__init__(health, shot_power)
        self.name = "Computer"

class GameUI(ABC):
    @abstractmethod
    def show_attack(self, attacker_name: str, victim_name: str, damage: int, victim_health: int):
        pass

    @abstractmethod
    def show_winner(self, winner_name: str):
        pass

class GameConsoleUI(GameUI):
    def show_attack(self, attacker_name, victim_name, damage, victim_health):
        print(f"⚔️ {attacker_name} бахнул {victim_name} на {damage} урона!")
        print(f"❤️ У {victim_name} осталось {victim_health} HP")
        print("-" * 20)

    def show_winner(self, winner_name):
        print(f"🏆 Ура! Победил {winner_name}!")

class Game:
    __player: Player
    __computer: Computer
    _healf_list = [100, 90, 80, 70, 60, 50]
    _power_list = [30, 25, 20, 15, 10]
    
    def __init__(self):
        self.__player = Player(
            choice(self._healf_list), choice(self._power_list)
            )
        self.__computer = Computer(
            choice(self._healf_list), choice(self._power_list)
            )
    @property
    def player(self):   
        return self.__player

    @property
    def computer(self):
        return self.__computer    

    def start(self, printer: GameUI):
        attacking = choice([self.__player, self.__computer])
        if attacking == self.__player:
            attacked = self.__computer
        else:
            attacked = self.__player

        while self.__player.is_alive and self.__computer.is_alive:
            deal_attack(attacking, attacked)

            printer.show_attack(    
                attacking.name, attacked.name, attacking.shot_power, attacked.health)

            attacking = attacked
            if attacking == self.__player:
                attacked = self.__computer
            else:
                attacked = self.__player  
        else:
            printer.show_winner(attacking.name)


game = Game()
print(f"На ринге:\n\nКомьютер: \n Здоровье - {game.computer.health} \n Сила удара - {game.computer.shot_power}\n\nИгрок: \n Здоровье - {game.player.health}\n Сила удара - {game.player.shot_power}")
game.start(GameConsoleUI())                
                
