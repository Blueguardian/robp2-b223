# The following file contains code made by ROB2 - B223
# 2. Semester AAU 2021.

import json
import os

from robolink.robolink import Robolink


class Statistics:
    # Global variables
    STATISTICS_FILE = 'statistics.json'
    FIELDS = ['type', 'created']
    INITIAL_VALUE = 0
    TYPES = ['black_none', 'black_none_engraved', 'black_edge', 'black_edge_engraved', 'black_curved',
             'black_curved_engraved', 'white_none', 'white_none_engraved', 'white_edge', 'white_edge_engraved',
             'white_curved', 'white_curved_engraved', 'blue_none', 'blue_none_engraved', 'blue_edge',
             'blue_edge_engraved', 'blue_curved', 'blue_curved_engraved']

    def __init__(self):
        """

        """
        if not os.path.isfile(self.STATISTICS_FILE):
            self.__create_statistics()

    def __str__(self):
        """

        :return:
        """
        RDK = Robolink()
        statistics_ = self.__get_statistics()
        RDK.RunMessage(statistics_)

    def __create_statistics(self):
        """

        :return:
        """
        statistics = {type_: self.INITIAL_VALUE for type_ in self.TYPES}

        with open(self.STATISTICS_FILE, 'w') as f:
            f.write(json.dumps(statistics, indent=4))

    def __get_statistics(self):
        """

        :return:
        """
        with open(self.STATISTICS_FILE, 'r') as f:
            return json.loads(f.read())

    def __update_statistics(self, stock: json):
        """

        :param stock:
        """
        with open(self.STATISTICS_FILE, 'w') as f:
            f.write(json.dumps(stock, indent=4))

    def get(self, stat_: str):
        """

        :param stat_: the type to get the value from
        :return: The value contained in the type "stat_"
        """
        statistics_ = self.__get_statistics()
        return statistics_[stat_]

    def add(self, stat_: str, count: int):
        """

        :param stat_: the type that has to be added to
        :param count: The amount to be added
        """
        statistics_ = self.__get_statistics()
        statistics_[stat_] += count
        self.__update_statistics(statistics_)
