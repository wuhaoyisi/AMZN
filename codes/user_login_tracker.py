"""
Design a system to record user login timestamps and retrieve the username of the earliest user with exactly one login session.
"""
from datetime import datetime
import heapq
from collections import defaultdict

class OptimizedUserLoginTracker:
    """
    优化版本：使用堆维护单次登录用户
    查询时间复杂度：O(log k) where k = single-login users
    """
    def __init__(self):
        self.login_counts = {}  # {username: count}
        self.user_timestamps = {}  # {username: first_login_time}
        self.single_login_heap = []  # min-heap of (timestamp, username)
        self.removed_users = set()  # 用于lazy deletion
        
    def add_login(self, username):
        """
        添加登录记录 - O(log k)
        """
        current_time = datetime.now()
        
        if username not in self.login_counts:
            # 首次登录
            self.login_counts[username] = 1
            self.user_timestamps[username] = current_time
            heapq.heappush(self.single_login_heap, (current_time, username))
        else:
            # 非首次登录
            self.login_counts[username] += 1
            # 如果之前是单次登录，现在需要从堆中移除
            if self.login_counts[username] == 2:
                self.removed_users.add(username)
    
    def get_earliest_single_login_user(self):
        """
        获取最早的单次登录用户 - O(log k)
        使用lazy deletion处理已移除的用户
        """
        while self.single_login_heap:
            timestamp, username = self.single_login_heap[0]
            
            # 检查用户是否仍然是单次登录
            if (username in self.removed_users or 
                username not in self.login_counts or 
                self.login_counts[username] != 1):
                # 用户已不再是单次登录，从堆中移除
                heapq.heappop(self.single_login_heap)
                self.removed_users.discard(username)
                continue
            
            # 找到有效的单次登录用户
            return username
        
        return None