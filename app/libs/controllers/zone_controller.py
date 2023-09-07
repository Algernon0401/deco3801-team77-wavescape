"""
    zone_stabilisation.py
    
    Introduces a basic logic controller for establishing and
    removing zones.
"""
from ..base import *
from ..object import *

class ZoneController(Controller):
    """
    This represents a controller that establishes new zones, and devises
    the logic that allows a zone to be destroyed based on non-existing objects
    
    NOTE: Even if a zone is destroyed, it's information is stored inside this class
    so that if it is accidentally removed, it still has the same attributes (based on center)
    """

    def __init__(self, controller: AppController):
        """
        Initializes the controller

        Arguments:
            controller -- the app controller this controller runs from
        """
        self.zones = []
        # Set object that defines zone as square
        self.zone_border_object = Tag.ARROW.value
        pass
    
    def update(self, controller: AppController):
        """
        Updates the controller on every loop iteration.

        Arguments:
            controller -- the app controller this controller runs from
        """
        # Create sorted lists by x,y starts
        def get_x(obj):
            return obj.x
        def get_y(obj):
            return obj.y
        
        # Create X sorted list
        xsort = [x for x in controller.objects if x.tag == self.zone_border_object]
        xsort.sort(key=get_x)
        
        # Create Y sorted list
        ysort = [x for x in xsort]
        ysort.sort(key=get_y)
        
        for object in xsort:
            # Analyze the space assuming this is the top-left corner, and
            # that all corners are the same size/shape.
            xmin = object.x
            ymin = object.y
            xmax = None
            ymax1 = None
            ymax2 = None
            
            # Test for first top-right corner.
            for o2 in xsort:
                if o2.x > xmin and o2.y + o2.h >= ymin and o2.y <= ymin + object.h:
                    xmax = o2.x + o2.w
                    break
            
            if xmax is None:
                continue
            
            # Test for bottom left corner.
            for o2 in ysort:
                if o2.y > ymin and o2.x + o2.w >= xmin and o2.x <= xmin + object.w:
                    ymax1 = o2.y + o2.h
                    break
                
            # Test for bottom right corner
            for o2 in ysort:
                if o2.y > ymin and o2.x + o2.w >= xmax - object.w and o2.x <= xmax:
                    ymax2 =  o2.y + o2.h
                    break
                
            if ymax1 is None or ymax2 is None:
                continue # No zones found here.
            
            # Ensure ymax1 and ymax2 are within (h/2) or each other.
            # otherwise, they are considered to be different corners.
            
            dist = ymax1 - ymax2
            if dist < 0:
                dist = -dist
            
            if dist > object.h / 2:
                continue
            
            ymax = ymax1
            if ymax < ymax2:
                ymax = ymax2
                
            # Finally check existing zones, and if the center does not collide
            # with any, then add.
            center_x = (xmax - xmin) / 2 + xmin
            center_y = (ymax - ymin) / 2 + ymin
            
            colliding_zone = None
            for zone in self.zones:
                if zone.within((center_x, center_y, 1, 1)):
                    colliding_zone = zone
                    break
                
            # Create new zone
            if colliding_zone is None:
                zone = controller.create_zone((xmin, ymin))
                zone.w = xmax - xmin
                zone.h = ymax - ymin
                self.zones.append(zone)
                
                
                        
                        
        
    
    def event(self, controller: AppController, event: pygame.event.Event):
        """
        Receives an event from the pygame interface.

        Arguments:
            controller -- the app controller this controller runs from
            event -- the pygame event that happened
        """
        pass