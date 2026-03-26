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
