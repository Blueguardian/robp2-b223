# The following file contains code made by ROB2 - B223
# 2. Semester AAU 2021.

from robolink.robolink import Robolink
from stock import Stock

"""
Restock script:
Refills the entire stock
"""

RDK = Robolink()
TYPES = ['black_none', 'black_edge', 'black_curved', 'white_none', 'white_edge', 'white_curved', 'blue_none',
         'blue_edge', 'blue_curved']
stock = Stock()


# For each type check the stock
for type_cover in TYPES:
    stock.set(type_cover, 10)
