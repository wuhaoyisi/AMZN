"""
design a parking system with parking spot of caring size: small, medium, large
each parking spot can park at most one car, 
as long as the car size does not exceed the parking size

"""

import uuid
from enum import Enum
from collections import deque\

class Size(Enum):
    SMALL = 0
    MEDIUM = 1
    LARGE = 2

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
        self.available_parking = {size: deque() for size in Size}
        # <each parked car, parked location>
        self.parked_location = {}

        for size, count in parking_count_by_size.items():
            for _ in range(count):
                self.available_parking[size].append(ParkingSpot(size))

    def assign_car(self, car):
        for size in Size:
            if car.get_size().get_num_val() > size.get_num_val():
                continue
            assigned_parking = self._assign_car_by_size(car, size)

            if assigned_parking:
                return assigned_parking.get_id()
        return "Reject"
    
    def get_car(self, car_id):
        if car_id in self.parked_location:
            parking_spot = self.parked_location[car_id]
            retrieved_car = parking_spot.retrieve_car()
            
            self.available_parking[parking_spot.get_size()].append(parking_spot)
            del self.parked_location[car_id]

            return retrieved_car
        return None

    def _assign_car_by_size(self, car, size):
        if self.available_parking[size]:
            assigned_parking = self.available_parking[size].popleft()
            assigned_parking.assign_car(car)
            self.parked_location[car.get_id()] = assigned_parking

            return assigned_parking
        
        return None
        



        