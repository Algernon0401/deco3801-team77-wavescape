import math
import pygame
class CamObject:
    """
        Represents an object that is recognised from the camera.
    """

    def __init__(self, tag, bounds, depth=0):
        """
            Constructs a camera recognised object from the given
            tag and bounds.

            The bounds should be a tuple (x,y,w,h), that contains
            the projected co-ordinates (i.e. you must consider
            the ratio of camera feed to screen size)

            The tag should be the recognised object name (e.g. star)

            The depth can be left out at this point in time, but will
            be necessary.
        """ 

        self.tag = tag
        (self.x, self.y, self.w, self.h) = bounds
        self.depth = depth
        self.attributes = {} # Attribute list for controls
    
    def within(self, bounds):
        """
            Returns True if object is contained within the bounds
        """
        (xf,yf,wf,hf) = bounds
        (x,y,w,h) = (self.x, self.y, self.w, self.h)
        # Calculate intersecting rectangle using pygame's clip
        return x + w >= xf and y + h >= yf and x < xf + wf and y < yf + hf
        
        