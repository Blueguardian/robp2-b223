# The following file contains code made by ROB2 - B223
# 2. Semester AAU 2021.

from statistics import Statistics
from robolink import *

RDK = Robolink()
stat = Statistics(RDK)
stat.__str__()
