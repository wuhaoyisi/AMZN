import uuid
from enum import Enum
from collections import deque

class Size(Enum):
    #enumera all size of locker
    SMALL = 0
    MEDIUM = 1
    LARGE = 2

    def get_num_val(self):
        return self.value

class Package:
    def __init__(self, size):
        # package has size and id 
        self.package_size = size
        self.package_id = str(uuid.uuid4())

    # two getters
    def get_size(self):
        return self.package_size

    def get_id(self):
        return self.package_id

class Locker:
    def __init__(self, size):
        # locker has size and id and boolean of package_inside
        self.locker_size = size
        self.locker_id = str(uuid.uuid4())
        self.package_inside = None

    # two getters
    def get_size(self):
        return self.locker_size

    def get_id(self):
        return self.locker_id

    # assign package
    def assign_package(self, package):
        self.package_inside = package

    # deassign
    def empty_locker(self):
        package = self.package_inside
        self.package_inside = None
        return package

class LockerSystem:
    def __init__(self, locker_count_by_size):
        # locker_sizes <Size, count>

        # only track available lockers and package location is enough
        self.available_lockers = {size: deque() for size in Size} # <Size, deque of locker items> initi each size a deque
        self.package_location = {} # <package_id, locker item> package locker map

        for size, count in locker_count_by_size.items(): 
            for _ in range(count):
                self.available_lockers[size].append(Locker(size)) # deque of locker items

    def assign_package(self, package):
        # iterate over all sizes from small to large, so we can assign the smallest locker that is large enough
        for size in Size: 
            if size.get_num_val() < package.get_size().get_num_val(): # if package size is larger than size, skip
                continue
            
            # once size of locker is large enough, assign locker
            assigned_locker = self._assign_locker_by_size(package, size)

            if assigned_locker:
                return assigned_locker

        return None
    

    def get_package(self, package_id):
        if package_id not in self.package_location:
            return None
        
        # key operation: notice they are both return item instead of id, this is OOP
        # get locker item from package_location
        locker = self.package_location[package_id]
        # empty locker and return package
        package = locker.empty_locker()

        self.available_lockers[locker.get_size()].append(locker)# append same locker item
        
        # update all related data in initial state
        del self.package_location[package_id]

        return package

    # helper to try to assign by given size, so when this is called, should be in the loop of size from small to large
    def _assign_locker_by_size(self, package, size):
        if not self.available_lockers[size]:
            return None

        locker = self.available_lockers[size].popleft() # O(1), deque is a double linked list
        locker.assign_package(package) # update locker item.package_inside with a package item

        # update related data in initial state
        self.package_location[package.get_id()] = locker

        return locker

    def get_system_status(self):
        return {
            'available_count': {size: len(queue) for size, queue in self.available_lockers.items()}, # cool way to init a dict
            'occupied_count': len(self.package_location)
        }


if __name__ == "__main__":
    locker_count_by_size = {Size.SMALL: 2, Size.MEDIUM: 1, Size.LARGE: 1}
    pickup = LockerSystem(locker_count_by_size)
    
    # 测试分配包裹
    small_package = Package(Size.SMALL)
    result = pickup.assign_package(small_package)
    
    print(f"Package assigned: {result is not None}")
    print(f"Assigned locker ID: {result.get_id() if result else 'None'}")
    print(f"System status: {pickup.get_system_status()}")
    
    # 测试取包裹
    retrieved_package = pickup.get_package(small_package.get_id())
    print(f"Retrieved package: {retrieved_package is not None}")
    print(f"Final status: {pickup.get_system_status()}")