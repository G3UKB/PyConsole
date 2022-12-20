#!/usr/bin/env python
#
# broker.py
#
# Python publish/subscribe broker for the PyConsole
# 
# Copyright (C) 2022 by G3UKB Bob Cowdery
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#    
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#    
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#    
#  The author can be reached by email at:   
#     bob@bobcowdery.plus.com
#

"""

The broker manages a simple publish/subscribe service.
Events are registerd with the broker at start of day.
Any module may then publish or subscribe to event types.

There is no queue mechanism implemented but this is a possible future
enhancement. At present, incoming messages are immediately dispatched
synchronously to each subscriber in turn. Events therefore arrive at a
subscriber on the thread of the caller. The subscriber must ensure that
they return from the call as quickly as possible and execute in a thread
safe manner.

"""

import sys
import logging
import traceback

logger = logging.getLogger ("tc.gsdm.twodb.events")

# The event registration format is
# {event_1:[subscriber_1, subscriber_2], event_2[...]}
events = {}
event_type = False
stop_events = False

def declare_event(event):
    """
    Add a new event to the dictionary
    
    Arguments:
        event   -- event name
        
    """
    
    if event in events:
        return False
    else:
        events[event] = []
        return True

def subscribe(subscriber, event):
    """
    Add a subscriber for the given event
    
    Arguments:
        subscriber  -- a class object with a processEvent() method
        event       -- event name to subscribe to
        
    """
    
    if event in events:
        list = events[event]
        list.append(subscriber)
        return True
    else:
        return False

def unsubscribe(subscriber, event):
    """
    Remove a subscriber from the given event
    
    Arguments:
        subscriber  --  a class object with a processEvent() method
        event       --  event name to unsubscribe from
        
    Currently this is never called. The reason is that the classes that provide
    the event sinks are permanent and live until the program terminates. If
    dynamic classes were introduced that use the event system then they *MUST*
    call this method to release subscriptions before the instance is destroyed.
    
    """
    
    if event in events:
        list = events[event]
        if subscriber in list:
            list.remove(subscriber)
        return True
    else:
        return False

def send(event_type, event_data):
    """
    Send the event_data to all subscribers of the event
    
    Arguments:
        event_type       -- event to send
        event_data       -- opaque data
        
    """
 
    if not stop_events:
        if event_type in events:
            list = events[event_type]
            for subscriber in list:
                try:
                    subscriber.process_event(event_type, event_data)
                except Exception as e:
                    pass

def closing():
    """ The system is closing so don't propogate any events """
    
    stop_events = True