
# lab 3
# .MutexManager Implementation: This class implements the MutexManager interface. It maintains:  
# Name: Jatin K rai
#DawID

"""
# MutexManager Implementation: This class implements the MutexManager interface. It maintains: 
• A queue for holding received REQUEST messages. 
• A variable to track the current process allowed in the critical section (based on Lamport's rules). 
• It implements methods from the interface: 

o requestEntry(processId, clock):  Updates the local queue with the received request. 
 Checks if the requesting process has the highest timestamp based on Lamport's rules (considering both logical clock value and process ID). 
 If the request is allowed, sends a REPLY message to the requesting process using RMI. 

o releaseEntry(processId):  Removes the process from the request queue. 
 If the queue is not empty, grants access to the next eligible process based on Lamport's rules and sends a REPLY message. 

"""


import Pyro5.api
from iLab3MutexManager import ILab3MutexManager

@Pyro5.api.expose
class clsLab3MutecxManager(ILab3MutexManager):

    #static Queue to manage the state of process.
    mutexmanagerRequestqueue = []
    mutexmanagerReplyqueue = []
    mutexmanagerReleasequeue = []
    queue = []

   #constructor
    def __init__(self):
        self.mutexmanagerRequestqueue = []
        self.mutexmanagerReplyqueue = []
        self.mutexmanagerReleasequeue = []
        #temporary queue for apply lamport sorting.
        self.current_process = None

    # requestEntry(processId, clock): Updates the local queue with the received request.
    def requestEntry(self, process_id, clock):

        try:
            self.current_process = process_id
            print ("clsLab3MutecxManager:requestEntry process_id = P" + str(process_id) + ", and vector clock value = (" + str(clock) + ")")
            """
            Updates the local queue with the received request.
            """

            """
            Checks if the requesting process has the highest timestamp based on Lamport's rules (considering both logical clock value and process ID).
            
            """
            #sorting
            self.queue.append((process_id, clock))
            #sorted request queue
            combinedwithclockvalandprocess = str(clock) + ":P" +  str (process_id)
            self.mutexmanagerRequestqueue.append(combinedwithclockvalandprocess)

            #reset reply Queue
            self.mutexmanagerReplyqueue.clear()

            self.queue.sort(key=lambda x: (x[1], x[0]))  # Sort by clock and process_id

            for queuedata in self.queue:
                combinedwithclockvalandprocess = str(queuedata[1]) + ":P" +  str (queuedata[0])
                self.mutexmanagerReplyqueue.append(combinedwithclockvalandprocess)

            if self.current_process is None or self.queue[0][0] == process_id:
                self.current_process = process_id
                # Send REPLY message to the process
                # combinedwithclockvalandprocess = str(self.queue[0][1]) + ":P" +  str (self.queue[0][0])
                #  self.mutexmanagerReplyqueue.append(combinedwithclockvalandprocess)
            
            """
                When a process receives REQUEST(TSn, Pi) message from process Pi, 
                it returns a timestamped REPLY message to Pi 
                place Pi's request on its own request queue Q. 

            """
            print ("clsLab3MutecxManager:requestEntry Queue entered process_id = " , process_id)
            """
            C1 : Pi has received a message with timestamp larger than its own (TSn,Pi)  from all other process. 
            C2 : Pi's request at the top of its request queue Q
            
            """
        except Exception as error:
            print("clsLab3MutecxManager: requestEntry failed")
            print (error)
        finally:
            print("clsLab3MutecxManager():requestEntry completed successfully")
        return self.mutexmanagerReplyqueue

    # releaseEntry(processId): Removes the process from the request queue. 
    def releaseEntry(self, process_id):
        
        try:
            self.current_process = process_id
            """
            Process Pi, on exiting the CS, 
            Removes its request from top of its request queue Q
            Removes the process from the request queue.
            If the queue is not empty, grants access to the next eligible process
            based on Lamport's rules and sends a REPLY message.
            
            """
            #remove from request Queue
            removeprocessidfromrequestrelease = ""

            #reset Quque
            self.queue.clear()

            #find the correct process id from request queue
            for processandclock in self.mutexmanagerRequestqueue:
                process = processandclock.split(":")
                clockval = process[0]
                processval = list(process[1])

                if (processval[1] == process_id):
                    removeprocessidfromrequestrelease = processandclock
                    self.mutexmanagerReplyqueue.remove(removeprocessidfromrequestrelease);
                    print ("clsLab3MutecxManager:releaseEntry Released from CS of process_id = P" + str(processval[1]) + ", and vector clock value =(" + str(clockval) + ")")
                else:
                    self.queue.append((int(processval[1]), int(clockval)))
                    print ("clsLab3MutecxManager:releaseEntry Exist in the Request Queue process_id = P" + str(processval[1]) + ", and vector clock value = (" + str(clockval) + ")")
                #populate for temporary
            
            #makesure processid is valid and remove from req queue and add into release quque.
            if (len(removeprocessidfromrequestrelease) > 2):
                self.mutexmanagerRequestqueue.remove(removeprocessidfromrequestrelease)
                #append into the released list for future reference.
                self.mutexmanagerReleasequeue.append(removeprocessidfromrequestrelease)
            else:
                print ("clsLab3MutecxManager:releaseEntry Request Queue process_id = P" + str(process_id) + " does not found in Queue")


             #reset reply Queue
            self.mutexmanagerReplyqueue.clear()

            self.queue = [req for req in self.queue if req[0] != process_id]

            #returning reply to all remaining queue.
            for queuedata in self.queue:
                combinedwithclockvalandprocess = str(queuedata[1]) + ":P" +  str (queuedata[0])
                self.mutexmanagerReplyqueue.append(combinedwithclockvalandprocess)

            """
            if self.queue:
                self.current_process = self.queue[0][0]
                # Send REPLY message to the next process
                combinedwithclockvalandprocess = str(self.queue[0][1]) + ":P" +  str (self.queue[0][0])
                self.mutexmanagerReplyqueue.append(combinedwithclockvalandprocess)
            """

            print ("clsLab3MutecxManager:releaseEntry Queue released process_id = " , process_id)
        except Exception as error:
            print("clsLab3MutecxManager: releaseEntry failed")
            print (error)
        finally:
            print("clsLab3MutecxManager():releaseEntry completed successfully")
        return self.mutexmanagerReplyqueue
