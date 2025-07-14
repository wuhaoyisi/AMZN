"""
设计一个服务，接受一组营销event，提供一个接口看当前的时间是不是允许部署代码。在营销时间内不是不允许部署代码的。时间前后要留一个固定的时间。
"""
from datetime import datetime, timedelta
from typing import List

class MarketingEvent:
    def __init__(self, start_time, end_time, buffer_time_minutes):
        # marketing event with start, end time and buffer
        self.start_time = start_time
        self.end_time = end_time
        self.buffer_time_minutes = buffer_time_minutes
    
    def is_in_no_deploy_window(self, current_time):
        # calculate no-deploy window: [start - buffer, end + buffer]
        no_deploy_start = self.start_time - timedelta(minutes=self.buffer_time_minutes)
        no_deploy_end = self.end_time + timedelta(minutes=self.buffer_time_minutes)
        
        # check if current time falls within no-deploy window
        return no_deploy_start <= current_time <= no_deploy_end

class DeploymentManage:
    def __init__(self, default_buffer_minutes=30):
        # list to store all marketing events
        self.marketing_events = []  # List[MarketingEvent]
        # default buffer time before and after marketing events
        self.default_buffer_minutes = default_buffer_minutes
    
    def add_marketing_event(self, start_time, end_time, buffer_minutes=None):
        # use default buffer if not specified
        buffer = buffer_minutes if buffer_minutes is not None else self.default_buffer_minutes
        
        # create and add marketing event to list
        event = MarketingEvent(start_time, end_time, buffer)
        self.marketing_events.append(event)
    
    def can_deploy(self, current_time=None):
        # use current time if not specified
        if current_time is None:
            current_time = datetime.now()
        
        # iterate through all marketing events
        for event in self.marketing_events:
            # if current time is in any no-deploy window, deployment not allowed
            if event.is_in_no_deploy_window(current_time):
                return False
        
        # no conflicts found, deployment allowed
        return True
    
    def get_next_deploy_window(self, current_time=None):
        # bonus: find when next deployment window opens
        if current_time is None:
            current_time = datetime.now()
        
        # if can deploy now, return immediately
        if self.can_deploy(current_time):
            return current_time
        
        # find earliest end time of conflicting events
        earliest_end = None
        for event in self.marketing_events:
            if event.is_in_no_deploy_window(current_time):
                event_end = event.end_time + timedelta(minutes=event.buffer_time_minutes)
                if earliest_end is None or event_end < earliest_end:
                    earliest_end = event_end
        
        return earliest_end