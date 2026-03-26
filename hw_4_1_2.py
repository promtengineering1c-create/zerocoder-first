# Ты разрабатываешь программное обеспечение для сети магазинов. Каждый магазин в этой сети имеет свои особенности, но также существуют общие характеристики, такие как адрес, название и ассортимент товаров. Ваша задача — создать класс Store, который можно будет использовать для создания различных магазинов.

# Шаги:

# 1. Создай класс Store:

# -Атрибуты класса:

# name: название магазина.

# address: адрес магазина.

# items: словарь, где ключ - название товара, а значение - его цена. Например, {'apples': 0.5, 'bananas': 0.75}.

# Методы класса:

# __init__ - конструктор, который инициализирует название и адрес, а также пустой словарь дляitems`.

# -  метод для добавления товара в ассортимент.

# метод для удаления товара из ассортимента.

# метод для получения цены товара по его названию. Если товар отсутствует, возвращайте None.

# метод для обновления цены товара.

# 2. Создай несколько объектов класса Store:

# Создай не менее трех различных магазинов с разными названиями, адресами и добавь в каждый из них несколько товаров.

# 3. Протестировать методы:

# Выбери один из созданных магазинов и протестируй все его методы: добавь товар, обнови цену, убери товар и запрашивай цену.

stores = []

class Store:
    name: str
    address: str
    items: dict

    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.items = {}

    def add_item(self, item_name, price):
        self.items[item_name] = price

    def remove_item(self, item_name):
        if item_name in self.items:
            del self.items[item_name]

    def get_price(self, item_name):
        try:
            return self.items[item_name]
        except KeyError:
            return None
        
    def update_price(self, item_name, new_price):
        try:
            self.items[item_name] = new_price
        except KeyError:
            print(f"Товар {item_name} не найден в ассортименте.")

store1 = Store("Магазин 1", "ул. Ленина, 1")
store2 = Store("Магазин 2", "ул. Пушкина, 2")
store3 = Store("Магазин 3", "ул. Гагарина, 3")

stores = [store1, store2, store3]

store1.add_item("яблоки", 0.5)  
store1.add_item("бананы", 0.75)

store2.add_item("груши", 1.0)
store2.add_item("ананас", 1.5)

store3.add_item("бананы", 0.5)
store3.add_item("ананас", 1.0)  

print(store1.get_price("яблоки"))  # Вывод: 0.5     
store1.update_price("яблоки", 0.6)
print(store1.get_price("яблоки"))  # Вывод: 0.6
store1.remove_item("бананы")
print(store1.get_price("бананы"))  # Вывод: None  
store1.remove_item("яблоки")
print(store1.get_price("яблоки"))  # Вывод: None
