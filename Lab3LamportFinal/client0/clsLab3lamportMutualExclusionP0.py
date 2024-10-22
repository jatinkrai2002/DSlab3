# lab 3
# Process Interface: This interface defines methods for processes to interact with the mutual exclusion logic. Methods can include:  
# Name: Jatin K rai
#DawID

#Process Interface: This interface defines methods for processes to interact with the mutual exclusion logic. Methods can include: 
# requestCriticalSection(): Requests entry to the critical section. 
# releaseCriticalSection(): Releases control after exiting the critical section. 
# getClock(): Retrieves the local vector clock value (using VectorClock interface, explained later). 


"""
Process Implementation: This class implements the Process interface. It maintains:
• A local VectorClock object (see below).
• A boolean flag indicating critical section access status.
• A reference to a shared MutexManager object (explained later).
• It implements methods from the interface:
o requestCriticalSection(): Increments the local clock, sends a REQUEST message with the current clock to the MutexManager using RMI.
o releaseCriticalSection(): Sets the critical section flag to false, sends a RELEASE message to the MutexManager using RMI.
o getClock(): Returns the local VectorClock object.

"""

import Pyro5.api
from iLab3lamportMutualExclusion import ILab3LamportMutualExclusion
from clLab3VectorClock import clLab3VectorClock

@Pyro5.api.expose
class clsLab3LamportMutualExclusionP0(ILab3LamportMutualExclusion):

    # pass process id also
    #Assume process
    ProcessP0 = 0
    AllProcesses = []
    #Assume there is a local queue for request, receive and reply.
    ProcessRequestQueue = []
    ProcessRelesedCSQueue = []
    ProcessReplyQueue = []
    ProcessinCriticalSection = []


    #constructor
    def __init__(self, mutex_manager):
        self.vector_clock = clLab3VectorClock()
        self.ProcessP0 = 0
        self.currentprocessid = 0
        self.AllProcesses = [0]
        self.in_critical_section = False
        self.mutex_manager = Pyro5.api.Proxy(mutex_manager)

#requestCriticalSection(): Requests entry to the critical section.
    def requestCriticalSection(self):
        try:
            print ("RequestCriticalSection : This is process  P0")

            for pid in self.AllProcesses:
                self.currentprocessid = pid
                self.vector_clock.increment()

                currentclockvalue = self.vector_clock.getClock()

                print ("requestCriticalSection : vector clock value = (" + str(currentclockvalue) + ")")
                print ("requestCriticalSection : process id value = P" + str(pid) + " requesting for Critical section")

                combinedwithclockvalandprocess = str(currentclockvalue) + ":P" +  str (pid)
                self.ProcessRequestQueue.append(combinedwithclockvalandprocess)

                #processrequestQueue will have (1P0, 2P1,3P2)
                self.ProcessReplyQueue = self.mutex_manager.requestEntry(self.currentprocessid, currentclockvalue)

            #Wait for reply
            # Logic to wait for REPLY message
            index = 0
            removefromtepliedlist = ""

            #take the top value
            repliedmessagefromutexmanager = self.ProcessReplyQueue[0]
            process = repliedmessagefromutexmanager.split(":")
            clockval = process[0]
            processval = list(process[1])

            #To avoid deadlock and unreachable.
            if ((self.in_critical_section == True) and (len(self.ProcessinCriticalSection) > 0)):
                if (repliedmessagefromutexmanager in self.ProcessinCriticalSection):
                    self.ProcessReplyQueue = self.mutex_manager.releaseEntry(processval[1])
                
            
            if (len(self.ProcessinCriticalSection) > 0):
                #forcely release critical section to avoid deadlock
                self.ProcessinCriticalSection.clear()
                self.in_critical_section = False

            if (self.in_critical_section == False):
                # ready to goto critical section.
                self.ProcessinCriticalSection.append(repliedmessagefromutexmanager)
                self.in_critical_section = True
                 #Remved from the Reply Quque
                self.ProcessReplyQueue.remove(repliedmessagefromutexmanager)
                
            
            #Empty value
            repliedmessagefromutexmanager = ""

        
            if (len(self.ProcessReplyQueue) > 0):
                for repliedmessagefromutexmanager in self.ProcessReplyQueue:
                    process = repliedmessagefromutexmanager.split(":")
                    clockval = process[0]
                    processval = list(process[1])

                    if (len(self.ProcessinCriticalSection) > 0):
                        self.in_critical_section = True

                    if ((self.in_critical_section == True) and (len(self.ProcessinCriticalSection) > 0)):
                        if (repliedmessagefromutexmanager in self.ProcessinCriticalSection):
                           print ("clsLab3LamportMutualExclusion: requestCriticalSection : Enter into CS of process_id = P" + str(processval[1]) + ", and vector clock value = (" + str(clockval) + ")" )
                        else: 
                            print ("clsLab3LamportMutualExclusion: requestCriticalSection :  process_id = P" + str(processval[1]) + ", and vector clock value = (" + str(clockval) + ")" + " are still in Reply Queue.")
        except Exception as error:
            print("clsLab3LamportMutualExclusion: requestCriticalSection failed")
            print (error)
        finally:
            print("clsLab3LamportMutualExclusion():requestCriticalSection completed successfully")


   # releaseCriticalSection(): Releases control after exiting the critical section.
    def releaseCriticalSection(self):
        try:
            self.in_critical_section = False
            releasecriticalsectionprocessval = ""

            for processisincriticalsection in self.ProcessinCriticalSection:
                process = processisincriticalsection.split(":")
                clockval = process[0]
                processval = list(process[1])
                self.currentprocessid = processval[1]
                #this process will be in critical sections.
                print ("clsLab3LamportMutualExclusion: releaseCriticalSection : Exit from CS of process_id = P" + str(processval[1]) + ", and vector clock value =(" + str(clockval) + ")")
                releasecriticalsectionprocessval = processisincriticalsection
                #call mutexmanager to release from critical sections and replied with updated replied queue.
                self.ProcessReplyQueue = self.mutex_manager.releaseEntry(self.currentprocessid)


             #makesure processid is valid and remove from cs queue and add into release quque.
            if (len(releasecriticalsectionprocessval) > 2):
                self.ProcessinCriticalSection.remove(releasecriticalsectionprocessval)
                #append into the released CS list for future reference.
                self.ProcessRelesedCSQueue.append(releasecriticalsectionprocessval)
                process = releasecriticalsectionprocessval.split(":")
                clockval = process[0]
                processval = list(process[1])
                print ("clsLab3LamportMutualExclusion: releaseCriticalSection Released from Critical section of process_id = P", str(processval[1]))
            else:
                print ("clsLab3LamportMutualExclusion: releaseCriticalSection: Does not Released from Critical section of process_id = P", str(processval[1]))

            """
            print ("releaseCriticalSection : vector_clock value = " , self.vector_clock.getClock())
            print ("releaseCriticalSection : process id value = " , self.currentprocessid)
            self.in_critical_section = False
            print ("releaseCriticalSection : self.in_critical_section value is False")
            """

            #release all pending in Quque to avoid deadlock.
            if(len(self.ProcessReplyQueue) > 0):
               for processwaitingforcriticalsection in self.ProcessReplyQueue:
                process = processwaitingforcriticalsection.split(":")
                clockval = process[0]
                processval = list(process[1])
                #this process will be in critical sections.
                print ("releaseCriticalSection: Waiting for critical section : process_id = P" + str(processval[1]) + ", and vector clock value = (" + str(clockval) + ")")
    

        except Exception as error:
            print("clsLab3LamportMutualExclusion: releaseCriticalSection failed")
            print (error)
        finally:
            print("clsLab3LamportMutualExclusion():releaseCriticalSection completed successfully")


#getClock(): Retrieves the local vector clock value (using VectorClock interface, explained later).
    def getClock(self):
        try:
            return self.vector_clock.getClock()
            # Logic to wait for REPLY message
        except Exception as error:
            print("clsLab3LamportMutualExclusion: getClock failed")
            print (error)
        finally:
            print("clsLab3LamportMutualExclusion():getClock completed successfully")


  