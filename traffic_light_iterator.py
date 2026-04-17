from collections.abc import Iterator

class TrafficLightIterator(Iterator):
    
    def __init__(self, records):
        self._records = records
        self._index = 0
    
    def __next__(self):
        if self._index < len(self._records):
            result = self._records[self._index]
            self._index += 1
            return result
        raise StopIteration
    
    def __iter__(self):
        return self
