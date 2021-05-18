from datetime import datetime, timedelta
from statistics import Statistics


class Timer:
    COVER_TYPES = ['black_none', 'black_edge', 'black_curved', 'white_none', 'white_edge', 'white_curved', 'blue_none',
                   'blue_edge', 'blue_curved']

    def __init__(self):
        self.stat = Statistics()

    def end(self, type_, start_):
        end = datetime.now()
        diff = end - start_
        diff = diff.total_seconds()
        self.time_avg = 0
        if type_ == 'average_production_time':
            for types in self.COVER_TYPES:
                self.time_avg =+ self.stat.get(types)
            self.stat.set(type_, self.addtoaverage(self.stat.get(type_), self.time_avg, diff))
            self.time_avg = 0
        if type_ == 'average_engraving_time':
            for types in self.COVER_TYPES:
                self.time_avg =+ self.stat.get(f'{types}_engraved')
            self.stat.set(type_, self.addtoaverage(self.stat.get(type_), self.time_avg, diff))
            self.time_avg = 0
        if type_ == 'average_total_time':
            for types in self.COVER_TYPES:
                self.time_avg =+ self.stat.get(types)
            self.stat.set(type_, self.addtoaverage(self.stat.get(type_), self.time_avg, diff))
            self.time_avg = 0
            print(f'The operation took {diff} seconds')

    def addtoaverage(self, average, size, value):
        return (size * average + value) / (size + 1)

