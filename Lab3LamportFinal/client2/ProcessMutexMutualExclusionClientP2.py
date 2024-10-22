
# lab 3
# ProcessMutexMutualExclusionClient: This is act as Client Process.  
# Name: Jatin K rai
#DawID

"""
# Process Implementation: This class implements the Process interface. It maintains: . 
"""

import Pyro5.api
from clsLab3lamportMutualExclusionP2 import clsLab3LamportMutualExclusionP2


def start_ProcessMutexMutualExclusionClient():
    try:
        uri = input("Enter the UnicastRemoteObject for Lamport Mutual Exclusion URI: ")

        # remote_process = Pyro5.api.Proxy(uri)
        remote_processP2 = clsLab3LamportMutualExclusionP2(uri)
        print ("clsLab3lamportMutualExclusion:requestCriticalSection has started for P2")

        remote_processP2.requestCriticalSection()
        print ("clsLab3lamportMutualExclusion:requestCriticalSection has completed  for P2")
        # Simulate critical section work
        print ("clsLab3lamportMutualExclusion:releaseCriticalSection has started  for P2")

        remote_processP2.releaseCriticalSection()
        print ("clsLab3lamportMutualExclusion:releaseCriticalSection has completed  for P2")

    except Exception as error:
            print("Pyro5.api.Proxy(): ClockArry Pyro5.api.Proxy failed while calling")
            print (error)
    finally:
            print("Pyro5.api.Proxy(): ClockArry Pyro5.api.Proxy completed successfully while calling.")
    # uri = "PYRONAME:lamportMutualExclusion.clsLab3MutecxManager"
   

if __name__ == "__main__":
    start_ProcessMutexMutualExclusionClient()
