import bisect
from typing import Any, Optional, Dict, List, Tuple
import time


class TimeTravelHashMap:
    def __init__(self):
        # more compact storage using separate timestamp and value arrays
        self.data: Dict[str, Tuple[List[int], List[Any]]] = {}  # <key, (timestamps, values)>
        
    def put(self, key: str, value: Any, timestamp: Optional[int] = None) -> None:
        # store using parallel arrays for better memory efficiency
        if timestamp is None:
            timestamp = int(time.time() * 1000)
            
        if key not in self.data:
            self.data[key] = ([], [])  # initialize parallel arrays
            
        timestamps, values = self.data[key]
        
        # find insertion position and insert into both arrays
        insert_pos = bisect.bisect_left(timestamps, timestamp)
        timestamps.insert(insert_pos, timestamp)
        values.insert(insert_pos, value)
        
    def get(self, key: str, timestamp: int) -> Optional[Any]:
        # retrieve using parallel array structure
        if key not in self.data:
            return None
            
        timestamps, values = self.data[key]
        
        # binary search in timestamp array
        insert_pos = bisect.bisect_right(timestamps, timestamp)
        
        if insert_pos == 0:
            return None
            
        # return corresponding value from values array
        return values[insert_pos - 1]