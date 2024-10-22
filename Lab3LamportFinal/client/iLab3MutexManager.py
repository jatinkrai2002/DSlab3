# lab 3
# .MutexManager Interface: This interface manages the mutual exclusion logic. Methods can include:.  
# Name: Jatin K rai
#DawID

"""
#. MutexManager Interface: This interface manages the mutual exclusion logic. Methods can include: 
• requestEntry(processId, clock): Processes a REQUEST message from a process. 
• releaseEntry(processId): Processes a RELEASE message from a process. 

"""
import Pyro5.api

class ILab3MutexManager:

    #requestEntry(processId, clock): Processes a REQUEST message from a process. 
    @Pyro5.api.expose
    def requestEntry(self, process_id, clock):
        pass
    #releaseEntry(processId): Processes a RELEASE message from a process. 
    @Pyro5.api.expose
    def releaseEntry(self, process_id):
        pass