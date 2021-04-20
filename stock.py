import json
import os

class Stock:

    STOCK_FILE = 'stock.json'
    FIELDS = ['type', 'stock']
    INITIAL_STOCK = 10
    TYPES = ['black_none', 'black_edge', 'black_curved', 'white_none', 'white_edge', 'white_curved', 'blue_none', 'blue_edge', 'blue_curved']

    def __init__(self):
        if not os.path.isfile(self.STOCK_FILE):
            self.__create_stock()

    def __create_stock(self):
        stock = {type_: self.INITIAL_STOCK for type_ in self.TYPES}

        with open(self.STOCK_FILE, 'w') as f:
            f.write(json.dumps(stock,indent=4))

    def __get_stock(self):
        with open(self.STOCK_FILE, 'r') as f:
            return json.loads(f.read())

    def __update_stock(self, stock: json):
        with open(self.STOCK_FILE, 'w') as f:
            f.write(json.dumps(stock, indent=4))

    def get(self, type_: str):
        stock_ = self.__get_stock()
        return stock_[type_]

    def update(self, type_: str, count: int):
        stock_ = self.__get_stock()
        stock_[type_] = count
        self.__update_stock(stock_)