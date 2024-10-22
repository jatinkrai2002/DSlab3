# lab 3
# Process Interface: This interface defines methods for processes to interact with the mutual exclusion logic. Methods can include:  
# Name: Jatin K rai
#DawID

"""
# Process Implementation: This class implements the Process interface. It maintains: 
• A local VectorClock object (see below). 
• A boolean flag indicating critical section access status. 
• A reference to a shared MutexManager object (explained later). 
• It implements methods from the interface: o requestCriticalSection(): Increments the local clock, sends a REQUEST message with the current clock to the MutexManager using RMI. 
o releaseCriticalSection(): Sets the critical section flag to false, sends a RELEASE message to the MutexManager using RMI. 
o getClock(): Returns the local VectorClock object. 
"""

import Pyro5.api


class ILab3LamportMutualExclusion:
    #requestCriticalSection(): Requests entry to the critical section.
    @Pyro5.api.expose
    def requestCriticalSection(self):
        pass

    #releaseCriticalSection(): Releases control after exiting the critical section.
    @Pyro5.api.expose
    def releaseCriticalSection(self):
        pass
    
    #getClock(): Retrieves the local vector clock value (using VectorClock interface, explained later).
    @Pyro5.api.expose
    def getClock(self):
        pass