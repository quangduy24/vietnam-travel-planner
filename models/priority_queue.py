import heapq

class PriorityQueue:

    def __init__(self):
        self.elements = []
        self.entry_finder = {}  # Mapping of items to entries
        self.counter = 0        # Unique sequence count
        
    def empty(self):

        return len(self.entry_finder) == 0
        
    def put(self, item, priority):

        if item in self.entry_finder:
            self.remove(item)
        count = self.counter
        self.counter += 1
        entry = [priority, count, item]
        self.entry_finder[item] = entry
        heapq.heappush(self.elements, entry)
        
    def remove(self, item):

        entry = self.entry_finder.pop(item)
        entry[-1] = None  # Mark as removed
        
    def get(self):

        while self.elements:
            priority, count, item = heapq.heappop(self.elements)
            if item is not None:
                del self.entry_finder[item]
                return item
        raise KeyError('pop from an empty priority queue')
