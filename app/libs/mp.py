"""
    mp.py - Hosts the Message class.
"""

class Message:
    """
    Provides a simple message structure between processes
    """

    def __init__(self, type, data=0):
        self.type = type
        self.data = data
