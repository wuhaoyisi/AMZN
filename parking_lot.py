"""
design a parking system with parking spot of caring size: small, medium, large
each parking spot can park at most one car, 
as long as the car size does not exceed the parking size

"""

import uuid
from enum import Enum
from collections import deque\

class Size(Enum):
    SMALL: 0
    MEDIUM: 1
    LARGE: 2

    def get_num_val(self):
        return self.value
    
class Car():
    def __init__(self, size):
        self.id = str(uuid.uuid4())
        self.size = size

    def get_id(self):
        return self.id
    
    def get_size(self):
        return self.size
    
class ParkingSpot():
    def __init__(self, size):
        self.id = str(uuid.uuid4())
        self.size = size
        self.parked = None

    def get_id(self):
        return self.id
    
    def get_size(self):
        return self.size
    
    def assign_car(self, car: Car):
        self.parked = car
    
    def retrieve_car(self):
        car = self.parked
        self.parked = None

        return car
    
class ParkingSystem():
    def __init__(self, parking_count_by_size):
        # <each size, deque of ParkingSpot item>
        self.avaliable_parking = {size: deque for size in Size}
        self.parked_location = ()
