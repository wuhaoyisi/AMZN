import random

class RandomizedSet:
    def __init__(self):
        # core data structures for O(1) operations
        self.val_to_index = {}  # {value: index_in_list}
        self.values = []        # dynamic array to store all values
        self.random_gen = random.Random()  # random number generator
    
    def insert(self, val) -> bool:
        # insert value if not exists, return True if inserted
        if val in self.val_to_index:
            return False  # value already exists
        
        # add to end of list and record index in hashmap
        self.values.append(val)
        self.val_to_index[val] = len(self.values) - 1
        return True
    
    def remove(self, val) -> bool:
        # remove value if exists, return True if removed
        if val not in self.val_to_index:
            return False  # value doesn't exist
        
        # key trick: swap with last element to maintain O(1) deletion
        last_val = self.values[-1]
        val_index = self.val_to_index[val]
        
        # swap target value with last element
        self.values[val_index] = last_val
        self.val_to_index[last_val] = val_index
        
        # remove last element (original target) and update hashmap
        self.values.pop()
        del self.val_to_index[val]
        return True
    
    def contains(self, val) -> bool:
        # check if value exists in set
        return val in self.val_to_index
    
    def getRandom(self) -> int:
        # return random element from current set
        if not self.values:
            raise Exception("Cannot get random from empty set")
        
        # generate random index and return corresponding value
        random_index = self.random_gen.randint(0, len(self.values) - 1)
        return self.values[random_index]
    
    def size(self) -> int:
        # helper method to get current size
        return len(self.values)
    
    def get_all_values(self) -> list:
        # helper method for debugging
        return self.values.copy()