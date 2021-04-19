import os

from configparser import ConfigParser


class CaseConfig:

    # if you want only a set of colours to be available
    _ALLOWED_COLOURS = ['white', 'blue', 'black']
    _ALLOWED_CURVES = ['none', 'sides', 'curved']

    @classmethod
    def __open_config(cls) -> ConfigParser:
        cfg = ConfigParser()
        cfg.read('config.ini')
        return cfg

    @classmethod
    def colour(cls):
        colour_id = cls.__open_config().get('costumer', 'colour')

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
    def curve_style(cls):
        curve_style_id = cls.__open_config().get('costumer', 'curve_style')

        if curve_style_id not in cls._ALLOWED_CURVES:
            raise KeyError('Error, curve style is not available.')

        # ... other error handling, validation, or mutation

        return curve_style_id

    @classmethod
    def file(cls):
        file_path = cls.__open_config().get('costumer', 'file')

        if not os.path.isfile(file_path):
            raise FileNotFoundError('Error, file does not exist.')

        # ... other error handling, validation, or mutation

        return file_path

    @classmethod
    def engrave(cls):
        engrave_bool = cls.__open_config().getboolean('costumer', 'engrave')

        #Error handling, validation or mutation

        return engrave_bool
