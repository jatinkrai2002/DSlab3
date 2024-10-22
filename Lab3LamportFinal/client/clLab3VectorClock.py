
# lab 3
# . VectorClock Implementation: This class implements the VectorClock interface (refer to the previous explanation for details). 
# Name: Jatin K rai
#DawID

"""
# Process Implementation: This class implements the Process interface. It maintains: 
• . VectorClock Implementation: This class implements the VectorClock interface (refer to the previous explanation for details). 
 A local VectorClock object (see below). 
increment()
 getClock()
 update()

"""
from iLab3VectorClock import iLab3VectorClock

class clLab3VectorClock(iLab3VectorClock):

    #logical clock value and static valu
    clock = 0

    #constructor
    def __init__(self):
        
        try:
            self.clock = 0
        except Exception as error:
            print("clLab3VectorClock: construction failed")
            print (error)
        finally:
            print("clLab3VectorClock(): construction successfully")

   #Increment the clock
    def increment(self):
        # Increment the local clock
        self.clock = self.clock + 1
        pass

      #get the current local clock
    def getClock(self):
        return self.clock

    def update(self, other_clock):
        # Update the local clock with another clock
        self.clock = other_clock
        pass