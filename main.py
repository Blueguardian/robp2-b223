from robolink.robolink import Robolink
from config import CaseConfig
from stock import Stock
from cover import Cover
from engrave import Engrave

RDK = Robolink()
stock = Stock()
cover = Cover(CaseConfig.colour(), CaseConfig.curve_style(), stock)

if RDK.Item('cover').item.__bool__():
    cover.give_top()
    if CaseConfig.engrave():
        pattern = Engrave()
        pattern.begin()
