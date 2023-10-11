import math
import pygame
import datetime
from enum import Enum
class Tag(Enum):
    """
        Represents the possible types/shapes of an object.
    """

    # type
    # PHONE = "phone"
    # WALLET = "wallet"
    # EARBUDS = "earbuds"
    # WATCH = "watch"
    # KEYS = "keys"
    # BOTTLE = "bottle"
    # CARD = "card"

    # shapes
    TRIANGLE = "triangle"
    SQUARE = "square"
    CIRCLE = "circle"
    STAR = "star"
    RECTANGLE = "rectangle"
    ARROW = "arrow"

ALL_TAGS = [
    e.value for e in Tag
]

class CamObject:
    """
        Represents an object that is recognised from the camera.
    """

    def __init__(self, tag:Tag, bounds, track_id=0):
        """
            Constructs a camera recognised object from the given
            tag and bounds.

            The bounds should be a tuple (x,y,w,h), that contains
            the projected co-ordinates (i.e. you must consider
            the ratio of camera feed to screen size)

            The tag should be the recognised object name (e.g. star)
        """ 

        self.tag = tag
        (self.x, self.y, self.w, self.h) = bounds
        self.track_id = track_id
        self.attributes = {} # Attribute list for controls
        self.date_created = datetime.datetime.now()
        self.date_last_included = datetime.datetime.now()
    
    def get_object_attributes(self):
        """
            Gets the object-based attributes
        """
        return self.attributes
    
    def get_object_attribute(self, attribute_name):
        """
            Gets a single object-based attribute
        """
        if attribute_name in self.attributes:
            return self.attributes[attribute_name]
        return None
    
    def set_object_attribute(self, attribute_name, attribute_value):
        """
        Sets the given attribute on the object.
        """
        
        self.attributes[attribute_name] = attribute_value

    def within(self, bounds):
        """
            Returns True if object's center is contained within the bounds.
        """
        (xf,yf,wf,hf) = bounds
        (x,y,w,h) = (self.x, self.y, self.w, self.h)
        (cx,cy) = (x+w/2, y+h/2)
        return cx >= xf and cy >= yf and cx < xf + wf and cy < yf + hf
    
    def get_center(self):
        """
        Returns the center of the control
        """
        return (self.x+self.w/2, self.y+self.h/2)
    
    def distance(self, center):
        """
            Calculates the distance between the center of this object and another point (x, y)
        """    
        (x,y) = center
        center_x = self.x + self.w/2
        center_y = self.y + self.h/2
        return math.sqrt(math.pow(x - center_x, 2) + math.pow(y - center_y, 2))
    
    def get_time_since_creation(self) -> float:
        """
            Returns the time since the object was created.
        """
        return (datetime.datetime.now() - self.date_created).total_seconds()
        