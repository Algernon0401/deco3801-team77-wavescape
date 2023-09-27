
from multiprocessing import Process, Queue
from ..mp import Message
from ..sound import *
from ..tone_generator import *


queues = None
MP_MSG_QUIT = 100
MAX_WAVE_COUNT = 300

class AudioQueueManager:
    """
    Wrapper for the two sound queues.
    """
    
    def __init__(self):
        """
        Initialises the two sound queues
        """
        self.wave_queue = Queue(MAX_WAVE_COUNT)
        self.message_audio_queue = Queue(10)

def run_audio_system():
    """
    Continuously runs the audio system
    (to be used as a subprocess), until
    a message is received to quit.
    
    The audio system uses the wave queue
    to detect which sounds to play.
    """
    global queues
    audio_system = Sound()
    
    print ("Audio system sub-process initialised")
    while True:
        # Process messages from main thread
        while queues.message_audio_queue.qsize() > 0:
             msg = queues.message_audio_queue.get()
             if msg.type == MP_MSG_QUIT:
                 # End thread
                 print ("Audio system sub-process exited")
                 return
             
        # Process all waves received from main thread
        while queues.wave_queue.qsize() > 0:
            waves = queues.wave_queue.get()
            audio_system.chorus(waves)
            
        time.sleep(0.05) # Do 20 times per second at most
         
class AudioSystem:
    """
    Represents a subprocess for playing sound waves.
    Only one audio system should exist at a time (AppController.audio_system)
    """
    
    def __init__(self):
        """
        Creates and initialises the audio system, by initialising queues
        and creating a subprocess to handle playing waves.
        """
        global queues
        queues = AudioQueueManager()
        
        # Create sub-process for processing sound waves
        Process(target=self.init_audio_system, args=(queues,)).start()
        
    def init_audio_system(self, audio_queues):
        """
        Initialises the sub-process with the given audio queues
        
        Arguments:
            audio_queues -- the queues passed to the subprocess
        """
        global queues
        queues = audio_queues
        run_audio_system()
        
    def play_waves(self, waves):
        """
        Passes to given waves to the audio system's subprocess,
        so that it is played next.
        """
        global queues
        
        if queues.wave_queue.qsize() >= MAX_WAVE_COUNT:
            # No choice but to remove queue item
            queues.wave_queue.get()
        queues.wave_queue.put(waves)
        
    def destroy(self):
        """
        Disposes of the subprocess responsible for the audio system
        """
        queues.message_audio_queue.put(Message(MP_MSG_QUIT))