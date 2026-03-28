# Разработай систему управления учетными записями пользователей для небольшой компании. Компания разделяет сотрудников на обычных работников и администраторов. У каждого сотрудника есть уникальный идентификатор (ID), имя и уровень доступа. Администраторы, помимо обычных данных пользователей, имеют дополнительный уровень доступа и могут добавлять или удалять пользователя из системы.

# Требования:

# 1.Класс `User*: Этот класс должен инкапсулировать данные о пользователе: ID, имя и уровень доступа ('user' для обычных сотрудников).

# 2.Класс `Admin`: Этот класс должен наследоваться от класса `User`. Добавь дополнительный атрибут уровня доступа, специфичный для администраторов ('admin'). Класс должен также содержать методы `add_user` и `remove_user`, которые позволяют добавлять и удалять пользователей из списка (представь, что это просто список экземпляров `User`).

# 3.Инкапсуляция данных: Убедись, что атрибуты классов защищены от прямого доступа и модификации снаружи. Предоставь доступ к необходимым атрибутам через методы (например, get и set методы).

class User:
    _id: int
    __name: str
    _is_admin: bool = False
    _users_list = []

    def __init__(self, __name):  
        self.__name = __name
        self._id = len(User._users_list) + 1
        User._users_list.append(self)

    @property
    def id(self):
        return self._id
    
    @property
    def is_admin(self):
        return self._is_admin
    
    def get_name(self):
        return self.__name

    @classmethod
    def remove_user(cls, name):
        for user in cls._users_list:
            if user.get_name() == name:
                cls._users_list.remove(user)
                return True
        return False        

class Admin(User):
    def __init__(self, name):
        super().__init__(name)
        self._is_admin = True

    def add_user(self, __name):
        return User(__name)
    
    def remove_user(self, name):
        return User.remove_user(name)
