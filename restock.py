# The following file contains code made by ROB2 - B223
# 2. Semester AAU 2021.

from robolink.robolink import Robolink
from stock import Stock

"""
Restock script:
Checks whether a stock item is empty and then refills it
"""

RDK = Robolink()
_INIT_STOCK = Stock.get_init()
_OFFSETX_COVER_DIST = 70
_OFFSETY_COVER_DIST = 73
_OFFSETZ_COVER_FLAT_DIST = 11.7
_OFFSETZ_COVER_EDGE_DIST = 14.7
_OFFSETZ_COVER_CURVED_DIST = 16.7
TYPES = ['black_none', 'black_edge', 'black_curved', 'white_none', 'white_edge', 'white_curved', 'blue_none',
         'blue_edge', 'blue_curved']
stock = Stock()

dist_map = {
    'flat': _OFFSETZ_COVER_FLAT_DIST,
    'edge': _OFFSETZ_COVER_EDGE_DIST,
    'curved': _OFFSETZ_COVER_CURVED_DIST
}

# Dict containing the distance from the bottom of the
# container to the bottom of the hole
container_height_map = {
    'flat': 55,
    'edge': 25,
    'curved': 5
}

# Dict containing identifiers for placement
case_types = {
    'black_none': 0,
    'black_edge': 1,
    'black_curved': 2,
    'white_none': 3,
    'white_edge': 4,
    'white_curved': 5,
    'blue_none': 6,
    'blue_edge': 7,
    'blue_curved': 8
}

# For each type check the stock
for type_cover in TYPES:
    if stock.get(type_cover) is 0:
        # Restock
        for i in range(_INIT_STOCK):
            cover = RDK.AddFile(f'covers/cover_{type_cover}')
            cover.setName(f'cover_{type_cover}_{stock.get(type_cover) + 1}')
            cover.setPoseFrame('stock_container')
            height_offset = container_height_map[type_cover.split('_')[-1]]
            cover_height = dist_map[type_cover.split('_')[-1]] * stock.get(type_cover)
            cover.MoveL([_OFFSETX_COVER_DIST * case_types[type_cover], _OFFSETY_COVER_DIST,
                         height_offset + cover_height, 0, 0, 0])
            stock.add(type_cover, 1)
