"""
design a hashtable 
suport operations like put get remove

"""


class HashTable:
    def __init__(self, initial_capacity=16):
        # initialize bucket array with empty lists for chaining collision resolution
        self.capacity = initial_capacity
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]  # list of lists, each bucket is a list of (key, value) tuples
        self.load_factor_threshold = 0.75  # resize trigger threshold
    
    def _hash_function(self, key):
        # simple modulo hash function to map key to bucket index
        return hash(key) % self.capacity  # hash() is built-in python hash function
    
    def _resize(self):
        # double capacity when load factor exceeds threshold
        old_buckets = self.buckets
        self.capacity *= 2
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]  # create new larger bucket array
        
        # rehash all existing key-value pairs into new buckets
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)  # reinsert using new hash function
    
    def put(self, key, value):
        # check if resize needed before insertion
        if self.size >= self.capacity * self.load_factor_threshold:
            self._resize()
        
        # find target bucket using hash function
        bucket_index = self._hash_function(key)
        target_bucket = self.buckets[bucket_index]
        
        # check if key already exists in bucket, update if found
        for i, (existing_key, existing_value) in enumerate(target_bucket):
            if existing_key == key:
                target_bucket[i] = (key, value)  # update existing key-value pair
                return
        
        # key not found, append new key-value pair to bucket
        target_bucket.append((key, value))
        self.size += 1
    
    def get(self, key):
        # find target bucket and search for key
        bucket_index = self._hash_function(key)
        target_bucket = self.buckets[bucket_index]
        
        # linear search in bucket for matching key
        for existing_key, existing_value in target_bucket:
            if existing_key == key:
                return existing_value  # return value if key found
        
        # key not found, raise KeyError
        raise KeyError(f"Key '{key}' not found")
    
    def remove(self, key):
        # find target bucket and remove key-value pair
        bucket_index = self._hash_function(key)
        target_bucket = self.buckets[bucket_index]
        
        # search and remove key-value pair from bucket
        for i, (existing_key, existing_value) in enumerate(target_bucket):
            if existing_key == key:
                removed_value = target_bucket.pop(i)  # remove and return (key, value) tuple
                self.size -= 1
                return removed_value[1]  # return only the value
        
        # key not found, raise KeyError
        raise KeyError(f"Key '{key}' not found")
    
    def __len__(self):
        return self.size
    
    def __str__(self):
        # display all key-value pairs for debugging
        pairs = []
        for bucket in self.buckets:
            for key, value in bucket:
                pairs.append(f"{key}: {value}")
        return "{" + ", ".join(pairs) + "}"