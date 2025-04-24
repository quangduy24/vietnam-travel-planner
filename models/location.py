class Location:

    def __init__(self, name, coordinates=None):

        self.name = name
        self.coordinates = coordinates
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"Location('{self.name}', {self.coordinates})"
    
    def distance_to(self, other_location):

        if self.coordinates is None or other_location.coordinates is None:
            return float('inf')
            
        # Simple Euclidean distance calculation
        x1, y1 = self.coordinates
        x2, y2 = other_location.coordinates
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
