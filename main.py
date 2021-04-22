# The following file contains code made by ROB2 - B223
# 2. Semester AAU 2021.
# The following file has no copyright and can be used freely
# Credit is expected when used commercially

# Necessary imports for program
from robolink.robolink import Robolink
from config import CaseConfig
from stock import Stock
from cover import Cover
from engrave import Engrave

RDK = Robolink()  # Establish link to robodk
stock = Stock()  #Create a stock object to simulate stock
cover = Cover(CaseConfig.colour(), CaseConfig.curve_style(), stock)  #Create a cover object, with the given color, curve and insert the stock object into it

if RDK.Item(f'cover {CaseConfig.colour()} curve_{CaseConfig.curve_style()}').item.__bool__():  # If the item 'cover color curve_style exists continue  # Uncertain if this works
    cover.give_top()  # Pick and place top cover and if it needs to be engraved place it on the engraving plate
    if CaseConfig.engrave():  # If the cover needs engraving
        pattern = Engrave()  # Create an engraving object
        if CaseConfig.curve_style() == 'none':
            pattern.begin_flat()  # Engrave the cover
        if CaseConfig.curve_style() == 'edge':
            pattern.begin_edge()
        if CaseConfig.curve_style() == 'curved':
            pattern.begin_curved()
