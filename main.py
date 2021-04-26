# The following file contains code made by ROB2 - B223
# 2. Semester AAU 2021.

from robolink.robolink import Robolink
from config import CaseConfig
from stock import Stock
from cover import Cover
from engrave import Engrave

RDK = Robolink()
stock = Stock()  # For simulating stock
cover = Cover(CaseConfig.colour(), CaseConfig.curve_style(), stock)

# If the item 'cover color curve_style exists continue  # Uncertain if this works
if RDK.Item(f'cover_{CaseConfig.colour()}_{CaseConfig.curve_style()}').item.__bool__():
    cover.give_top()
    if CaseConfig.engrave():
        pattern = Engrave()
        if CaseConfig.curve_style() == 'none':
            pattern.begin_flat()
        if CaseConfig.curve_style() == 'edge':
            pattern.begin_edge()
        if CaseConfig.curve_style() == 'curved':
            pattern.begin_curved()
        cover.retrieve()
    stock.update(f'{CaseConfig.colour()}_{CaseConfig.curve_style()}',
                 stock.get(f'{CaseConfig.colour()}_{CaseConfig.curve_style()}') - 1)