"""
    geometry.py

    Contains all functions related to shapes, lines.
"""

def line_intersection(line1, line2):
    """
    Gets the intersection of two lines, if they intersect.

    According to wikipedia.org/wiki/Line=line inersection

    Arguments:
        line1 - a line ((p1x,p1y), (p2x,p2y))
        line2 - a line ((p3x,p3y), (p4x,p4y))

    Returns:
        none if the two lines don't intersect, else the point of intersection
    """
    ((x1,y1), (x2,y2)) = line1
    ((x3,y3), (x4, y4)) = line2

    pxd = (x1-x2) * (y3-y4) - (y1-y2) * (x3-x4)
    pyd = (x1-x2) * (y3-y4) - (y1 - y2) * (x3 - x4)

    # If the denominator is zero, then the two lines are parallel or coincident
    if pxd == 0 or pyd == 0:
        return None
    
    pxn = (x1*y2 - y1*x2)*(x3-x4) - (x1-x2)*(x3*y4 - y3*x4)
    pyn = (x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4 - y3*x4)

    return ((pxn/pxd), (pyn/pyd))

def line_intersection_box(line, box):
    """
    Gets the intersection of a line and a box, if they intersect.

    Arguments:
        line1 - a line ((p1x,p1y), (p2x,p2y))
        box - a box (bx,by,bw,bh)

    Returns:
        none if the box and the line don't intersect, else the point of intersection
    """

    # Top
    (bx,by,bw,bh) = box
    intersection = line_intersection(((bx,by), (bx+bw,by)), line)
    if intersection is None:
        # Bottom
        intersection = line_intersection(((bx,by+bh), (bx+bw,by+bh)), line)
        if intersection is None:
            # Left
            intersection = line_intersection(((bx,by), (bx,by+bh)), line)
            if intersection is None:
                # Right
                intersection = line_intersection(((bx+bw,by), (bx+bw,by+bh)), line)
    return intersection