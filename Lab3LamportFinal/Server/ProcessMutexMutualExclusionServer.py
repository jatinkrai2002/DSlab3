
# lab 3
# ProcessMutexMutualExclusionServer  : This is act as Server process 
# Name: Jatin K rai
#DawID

"""
This is act as server process ProcessMutexMutualExclusionClient
"""

import Pyro5.api
from clsLab3MutecxManager import clsLab3MutecxManager

def main():


    #Act as Server.
    try:
        #make it server ready for remote process.
        daemon = Pyro5.api.Daemon()

    except Exception as error:
        print("Pyro5.api.Daemo(): failed.")
        print(error)
    finally:
        print("Pyro5.api.Daemo(): completed successfully.")

    try:
        #make it server ready for remote process.
        # Register MutexManager
        mutex_manager = clsLab3MutecxManager()
        uri = daemon.register(mutex_manager)

    except Exception as error:
        print("Pyro5.api.Daemo.register(): failed.")
        print(error)
    finally:
        print("Pyro5.api.Daemo.register() : completed successfully.")
        
    try:
        #make it server ready for remote process.
        print("UnicastRemoteObject for Lamport MutualExclusion  Protocol=" , uri)
        print("Lamport Mutual Exclusion registered. Ready.")
        daemon.requestLoop()  # Start the event loop of 
    except Exception as error:
        print("Pyro5.api.Daemo.requestLoop(): failed.")
        print(error)
    finally:
        print("Pyro5.api.Daemo.requestLoop() : completed successfully.")

if __name__ == "__main__":
    main()