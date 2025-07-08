import uuid
from enum import Enum
from collections import deque

class Size(Enum):
    # enumerate all vehicle and parking spot sizes with numeric values for comparison
    SMALL = 0
    MEDIUM = 1
    LARGE = 2
    
    def get_num_val(self):
        return self.value

class ParkingSpot:
    def __init__(self, size, spot_id):
        # each parking spot has size, unique id, and occupancy status
        self.spot_size = size
        self.spot_id = spot_id
        self.occupied_by_vehicle = None  # stores vehicle info when occupied
    
    def park_vehicle(self, vehicle_size):
        # assign vehicle to this parking spot
        self.occupied_by_vehicle = vehicle_size
    
    def remove_vehicle(self):
        # clear vehicle from parking spot and return vehicle info
        vehicle = self.occupied_by_vehicle
        self.occupied_by_vehicle = None
        return vehicle
    
    def is_available(self):
        return self.occupied_by_vehicle is None

class ParkingLot:
    def __init__(self, spot_config):
        # spot_config: [small_count, medium_count, large_count]
        
        # maintain available spots for each size using deque for O(1) operations
        self.available_spots = {size: deque() for size in Size}  # <Size, deque[ParkingSpot]>
        self.ticket_to_spot = {}  # <ticket_id, ParkingSpot> for O(1) lookup when leaving
        
        # create parking spots based on configuration
        spot_counts = [spot_config[0], spot_config[1], spot_config[2]]  # [small, medium, large]
        sizes = [Size.SMALL, Size.MEDIUM, Size.LARGE]
        
        for i, (size, count) in enumerate(zip(sizes, spot_counts)):
            for spot_num in range(count):
                spot_id = f"{size.name}_{spot_num}"  # unique spot identifier
                new_spot = ParkingSpot(size, spot_id)
                self.available_spots[size].append(new_spot)  # add to available queue
    
    def park_vehicle(self, vehicle_size):
        # find smallest available spot that can fit the vehicle (upward compatibility)
        for spot_size in Size:
            # skip spots that are too small for the vehicle
            if spot_size.get_num_val() < vehicle_size.get_num_val():
                continue
            
            # try to assign spot of current size
            assigned_spot = self._assign_spot_by_size(vehicle_size, spot_size)
            if assigned_spot:
                return assigned_spot  # return ticket_id if successful
        
        # no suitable spot found
        return "Reject"
    
    def leave_vehicle(self, ticket_id):
        # find parked vehicle using ticket and free up the spot
        if ticket_id not in self.ticket_to_spot:
            return  # invalid ticket, silently ignore
        
        # get parking spot from ticket mapping
        parked_spot = self.ticket_to_spot[ticket_id]
        parked_spot.remove_vehicle()  # clear vehicle from spot
        
        # return spot to available queue for reuse
        self.available_spots[parked_spot.spot_size].append(parked_spot)
        
        # clean up ticket mapping
        del self.ticket_to_spot[ticket_id]
    
    def _assign_spot_by_size(self, vehicle_size, spot_size):
        # helper method to assign spot of specific size if available
        if not self.available_spots[spot_size]:
            return None  # no spots available of this size
        
        # get next available spot from queue
        assigned_spot = self.available_spots[spot_size].popleft()  # O(1) deque operation
        assigned_spot.park_vehicle(vehicle_size)  # mark spot as occupied
        
        # generate unique ticket for this parking session
        ticket_id = str(uuid.uuid4())
        self.ticket_to_spot[ticket_id] = assigned_spot  # store ticket-to-spot mapping
        
        return ticket_id
    
    def process_operations(self, operations):
        # process list of parking operations and return results
        results = []
        for operation in operations:
            op_type = operation[0]  # "park" or "leave"
            
            if op_type == "park":
                vehicle_size = operation[1]  # Size enum value
                result = self.park_vehicle(vehicle_size)
                results.append(result)  # append ticket_id or "Reject"
            elif op_type == "leave":
                ticket_id = operation[1]  # ticket string
                self.leave_vehicle(ticket_id)
                # leave operations produce no output
        
        return results