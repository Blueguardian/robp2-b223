# The following file contains code made by ROB2 - B223
# 2. Semester AAU 2021.

import os  # Import os for checking paths

from configparser import ConfigParser  # Import the configprser for reading the config file


class CaseConfig:
    # Global variables
    # Set allowed values for covers
    _ALLOWED_COLOURS = ['white', 'blue', 'black']  # Allowed colors white, blue and black
    _ALLOWED_CURVES = ['none', 'edge', 'curved']  # Allowed curve types none, edge and curved

    @classmethod
    def __open_config(cls) -> ConfigParser:
        cfg = ConfigParser()
        cfg.read('config.ini')
        return cfg

    @classmethod
    def colour(cls, _type='costumer'):
        colour_id = cls.__open_config().get(_type, 'colour')

        # if you decide to use hex strings instead of colour names, use re to ensure it is valid
        # import re
        #
        # if not re.match('[a-fA-F0-9]', colour_id'):
        #     raise KeyError('Error, colour code not valid.')
        #
        # and append the # when returning
        # return f'#{colour_id}'

        if colour_id not in cls._ALLOWED_COLOURS:
            raise KeyError('Error, colour is not available.')

        # ... other error handling, validation, or mutation

        return colour_id

    @classmethod
    def curve_style(cls, _type='customer'):
        curve_style_id = cls.__open_config().get(_type, 'curve_style')

        if curve_style_id not in cls._ALLOWED_CURVES:
            raise KeyError('Error, curve style is not available.')

        # ... other error handling, validation, or mutation

        return curve_style_id

    @classmethod
    def file(cls, _type='customer'):
        file_path = cls.__open_config().get(_type, 'file')

        if not os.path.isfile(file_path):
            raise FileNotFoundError('Error, file does not exist.')

        # ... other error handling, validation, or mutation

        return file_path

    @classmethod
    def engrave(cls, _type='costumer'):
        engrave_bool = cls.__open_config().getboolean(_type, 'engrave')

        return engrave_bool
