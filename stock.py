# The following file contains code made by ROB2 - B223
# 2. Semester AAU 2021.
# The following file has no copyright and can be used freely
# Credit is expected when used commercially

# Necessary imports for the class Stock
import json
import os

# Begin Class definition
class Stock:
    STOCK_FILE = 'stock.json'  # The stock file
    FIELDS = ['type', 'stock']  # The fields that are inserted into the file
    INITIAL_STOCK = 10  # Initial stock
    TYPES = ['black_none', 'black_edge', 'black_curved', 'white_none', 'white_edge', 'white_curved', 'blue_none', 'blue_edge', 'blue_curved']  # List of allowed types types of covers

    # Constructor definition:
    # Always called __init__.
    # Checks if there is an existing file named
    # 'stock.json', if not, then creates one

    def __init__(self):  # Contructor definition
        if not os.path.isfile(self.STOCK_FILE):  # If there isn't a file
            self.__create_stock()  # Call method __create_stock

    # Method definition:
    # __create_stock.
    # Opens the json file, writes the current stock into
    # it.

    def __create_stock(self):  # Method definition
        stock = {type_: self.INITIAL_STOCK for type_ in self.TYPES}  # Create a variable to contain the initial stock

        with open(self.STOCK_FILE, 'w') as f:  # Open the file
            f.write(json.dumps(stock, indent=4))  # Write the object 'stock' into the file with an indent of 4

    # Method definition:
    # __get_stock.
    # Opens the file and loads the contents and returns them

    def __get_stock(self):  # Method definition
        with open(self.STOCK_FILE, 'r') as f:  # Open the file
            return json.loads(f.read())  # Read the file and return it

    # Method definition
    # __update_stock.
    # Takes in parameters stock of type hint json
    # and writes it to the file

    def __update_stock(self, stock: json):  # Method definition with parameter stock with type hint json
        with open(self.STOCK_FILE, 'w') as f:  # Open the file
            f.write(json.dumps(stock, indent=4))  # Write the data from the stock object into the file

    # Method definition:
    # get.
    # takes in a type and returns the
    # value that it represents

    def get(self, type_: str):  # Method definition
        stock_ = self.__get_stock()  # Creates an variable 'stock' and assigns the return value from the method __get_stock to it
        return stock_[type_]  # Returns the value of the type

    # Method definition
    # update
    # Takes in a type and a count and writes that to the stock file

    def update(self, type_: str, count: int):  # Method definition with two parameters type_ and count of type hint string and int respectively
        stock_ = self.__get_stock()  # Creates a variable and assigns the return value of the method __get_stock to it
        stock_[type_] = count  # Sets the value count to stock_[type_]
        self.__update_stock(stock_)  # Writes it to the file

    # Class method definition
    # get_init.
    # Class methods are static, and has access to class methods
    # without having to create an instance of an object first.
    # Returns the capacity or initial stock value from the class

    @classmethod  # Decorator
    def get_init(cls):  # Method definition
        return cls.INITIAL_STOCK  # Return the value in the variable INITIAL_STOCK
