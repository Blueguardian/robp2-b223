# The following file contains code made by ROB2 - B223
# 2. Semester AAU 2021.

from robolink.robolink import Robolink

from config import CaseConfig
from cover import Cover
from engrave import Engrave
from stock import Stock
from gui import gui

GUI = gui()
RDK = Robolink()
stock = Stock()  # For simulating stock
cover = Cover(CaseConfig.colour(), CaseConfig.curve_style(), stock)
cover.new_cover_check()

if stock.get(f'{CaseConfig.colour()}_{CaseConfig.curve_style()}') == 0:
    none_flat_str = CaseConfig.curve_style().replace('none', 'flat', -1)
    error_str = f'Stock depleted of {CaseConfig.colour()} {none_flat_str} covers'
    RDK.RunMessage(error_str)
else:
    cover.give_top()
    if CaseConfig.engrave():
        pattern = Engrave(RDK)
        if CaseConfig.curve_style() == 'none':
            pattern.begin_flat()
        if CaseConfig.curve_style() == 'edge':
            pattern.begin_edge()
        if CaseConfig.curve_style() == 'curved':
            pattern.begin_curved()
        cover.retrieve()
