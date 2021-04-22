# The following file contains code made by ROB2 - B223
# 2. Semester AAU 2021.

import os  # Import os for checking paths

from configparser import ConfigParser  # Import the configprser for reading the config file


class CaseConfig:
    # Global variables
    # Set allowed values for covers
    _ALLOWED_COLOURS = ['white', 'blue', 'black']  # List of allowed colors white, blue and black
    _ALLOWED_CURVES = ['none', 'edge', 'curved']  # List of allowed curve types none, edge and curved

    # Class method definition:
    # __open_config.
    # Class methods are static, and has access to class methods
    # without having to create an instance of an object first.
    # This method accesses the config file and returns a parser to
    # the file

    @classmethod  # Decorator
    def __open_config(cls) -> ConfigParser:  # Method definition with return type hint ConfigParser
        cfg = ConfigParser()  # Initialize object cfg with ConfigParser object
        cfg.read('config.ini')  # Read the config file
        return cfg  # return the cfg object

    # Class method definition
    # colour.
    # Class methods are static, and has access to class methods
    # without having to create an instance of an object first.
    # This method accesses and reads the "colour" data from customer
    # checks whether it corresponds to one of the values in _ALLOWED_COLOURS
    # and returns the value if it is.

    @classmethod
    def colour(cls, type_='customer'):  # Method definition with parameter default 'customer'
        colour_id = cls.__open_config().get(type_, 'colour')  # Open the file and read the value at identifier colour in type_

        # if we decide to use hex strings instead of colour names, use re to ensure it is valid
        # import re
        #
        # if not re.match('[a-fA-F0-9]', colour_id'):
        #     raise KeyError('Error, colour code not valid.')
        #
        # and append the # when returning
        # return f'#{colour_id}'

        if colour_id not in cls._ALLOWED_COLOURS:  # If the value is not in the list
            raise KeyError('Error, colour is not available.')  # Raise the exception KeyError with fitting text

        # ... other error handling, validation, or mutation

        return colour_id  # Return the value

    # Class method definition
    # curve_style.
    # Class methods are static, and has access to class methods
    # without having to create an instance of an object first.
    # This method accesses and reads the "curve_style" data from type_
    # checks whether it corresponds to one of the values in _ALLOWED_CURVES
    # and returns the value if it is.

    @classmethod
    def curve_style(cls, type_='customer'):  # Method definition with parameter default 'customer'
        curve_style_id = cls.__open_config().get(type_, 'curve_style')  # Open the file and read the value at identifier curve_style in type_

        if curve_style_id not in cls._ALLOWED_CURVES:  # If the value is not in the list
            raise KeyError('Error, curve style is not available.')  # Raise the exception  KeyError with fitting text

        # ... other error handling, validation, or mutation

        return curve_style_id  # Return the value

    # Class method definition
    # curve_style.
    # Class methods are static, and has access to class methods
    # without having to create an instance of an object first.
    # This method accesses and reads the "file" data from type_
    # checks whether it is a file and returns the value if it is

    @classmethod
    def file(cls, type_='customer'):  # Method definition with parameter default 'customer'
        file_path = cls.__open_config().get(type_, 'file')  # Open the file and read the value at identifier file in type_

        if not os.path.isfile(file_path):  # If the value does not correspond to a file
            raise FileNotFoundError('Error, file does not exist.')  # Raise the exception FileNotFoundError with fitting text

        # ... other error handling, validation, or mutation

        return file_path  # Return the value

    # Class method definition
    # curve_style.
    # Class methods are static, and has access to class methods
    # without having to create an instance of an object first.
    # This method accesses and reads the "engrave" data from type_
    # checks whether it is a boolean and returns the value if it is.

    @classmethod # Decorator
    def engrave(cls, type_='customer'):  # Method definition with parameter default 'customer'
        engrave_bool = cls.__open_config().getboolean(type_, 'engrave') # Open the file and read the value at identifier colour in type

        if type(engrave_bool) != bool:  # If the value is not a boolean
            raise KeyError('Error, not a boolean type')  # Raise the exception KeyError with fitting text

        return engrave_bool   # Return the value
