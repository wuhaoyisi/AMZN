"""
Design a system to record user login timestamps and retrieve the username of the earliest user with exactly one login session.
"""
from collections import defaultdict

class LoginTracker:
    def __init__(self):
        # track all login timestamps for each user
        self.user_login_times = defaultdict(list)  # <username, list of timestamps>
        # track login count for quick lookup
        self.user_login_count = defaultdict(int)   # <username, count>
    
    def record_login(self, username, timestamp):  # O1
        # add timestamp to user's login history
        self.user_login_times[username].append(timestamp)
        # increment login count for this user
        self.user_login_count[username] += 1
    
    def get_earliest_single_login_user(self): # ON
        earliest_user = None
        earliest_timestamp = float('inf')
        
        # iterate through all users to find single login users
        for username, count in self.user_login_count.items():
            if count == 1:  # user has exactly one login
                # get the only timestamp for this user
                user_timestamp = self.user_login_times[username][0]
                # update earliest if this user logged in earlier
                if user_timestamp < earliest_timestamp:
                    earliest_timestamp = user_timestamp
                    earliest_user = username
        
        return earliest_user
    

import heapq
from collections import defaultdict

class OptimizedLoginTracker:
    def __init__(self):
        # track login count for each user
        self.user_login_count = defaultdict(int)  # <username, count>
        # track first login time for each user
        self.user_first_login_time = {}  # <username, first_timestamp>
        # min heap to maintain single login users by earliest timestamp
        self.single_login_heap = []  # [(timestamp, username), ...]
    
    def record_login(self, username, timestamp): # logN if new
        if username not in self.user_login_count: 
            # first login: add to heap and record first login time
            self.user_first_login_time[username] = timestamp
            heapq.heappush(self.single_login_heap, (timestamp, username))
        
        # increment login count regardless
        self.user_login_count[username] += 1
        
        # note: we don't remove from heap immediately for O(log n) complexity
        # instead, we handle it in get_earliest_single_login_user()
    
    def get_earliest_single_login_user(self): # O1 Amortized, means it could go slow still ave O1
        # clean up heap top until we find valid single login user
        while self.single_login_heap:
            timestamp, username = self.single_login_heap[0]
            
            # check if this user still has exactly one login
            if self.user_login_count[username] == 1:
                return username
            else:
                # user has multiple logins, remove from heap
                heapq.heappop(self.single_login_heap)
        
        # no single login users found
        return None