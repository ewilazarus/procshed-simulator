'''
Created on Jun 2, 2012

@author: gabriel
'''
import process
import copy


LATEST_USED_PRIORITY = -1


# @@@@@@@@@@@@@@@@ class Scheduling Policies @@@@@@@@@@@@@@@@
'''
    Class Scheduling Policies
    @note - This class is just an enum that represents the scheduling policies.
'''
class SchedulingPolicies:
    Priority, MultipleQueue = range(2)

# @@@@@@@@@@@@@@@@ class Scheduling Policies @@@@@@@@@@@@@@@@

# @@@@@@@@@@@@@@@@ class Simulator @@@@@@@@@@@@@@@@
'''
    Class Simulator
    @note - This class is where the magic happens. Here is the code that decides
            what to do and when to do things to the processes.
'''
class Simulator:

# ++++++++++++++++ constructor +++++++++++++++++
    
    '''
        Method __init__ (constructor)
        @note - Initialize the queues
        @parm - procs: array containing the processes
    '''
    def __init__(self, procs):

        #the __procs queue is a backup queue to save the original processes
        self.__procs = procs
        
        self.__ready = copy.copy(procs)
        self.__blocked = []
        self.__finished = []

# ---------------- constructor -----------------

# ++++++++++++++++ start simulation +++++++++++++++++

    '''
        Method Start Simulation
        @note - This method is responsible for invoking the scheduling policies
                to be ran.
    '''
    def start_simulation(self):
        print "\nBEGINNING SIMULATION:"
        
        self.priority_sch_pol()
        raw_input("\nPress any key to continue . . . \n")
        
        self.clean()
        self.mq_sch_pol()

# ---------------- start simulation -----------------    
    
# ++++++++++++++++ clean +++++++++++++++++

    '''
        Method Start Simulation
        @note - This method is responsible for setting up the queues for the next scheduling policy
    '''
    def clean(self):
#        print "CLEANCLEANCLEAN"

        for p in self.__finished:
            del p
        
        for p in self.__procs:
            q = copy.copy(p)
            self.__ready.append(q)
        
# ---------------- clean -----------------
    
# ++++++++++++++++ priority scheduling policy +++++++++++++++++

    '''
        Method Priority Scheduling Policy
        @note - Simulates the Priority Scheduling Policy
    '''
    def priority_sch_pol(self):
        print "SCHEDULING POLICY: Priority"

        # starts all process as different threads
        for p in self.__ready:
                p.start()

        # infinite loop
        while True:
            
            # if both the __ready queue and the __blocked queue are empty, than finish
            if self.__ready.__len__() == 0 and self.__blocked.__len__() == 0:
                break
            
            # if the __ready queue is not empty
            if self.__ready.__len__() > 0:
                
                #finds the greater priority process (GPP)
                p = get_greater_priority_process(self.__ready)
                pStatus = p.get_status()
            
                #if the GPP's status is Finished, than append it to the __finished queue
                if pStatus == process.ProcessStatus.Finished:
                    self.__ready.remove(p)
                    self.__finished.append(p)
                    
                #if the GPP's status is Ready, than change it to Setting Up
                elif pStatus == process.ProcessStatus.Ready:
                    p.set_status(process.ProcessStatus.SettingUp)
                
                #if the GPP's status is Blocked, than append it to the __blocked queue
                elif pStatus == process.ProcessStatus.Blocked:
                    self.__ready.remove(p)
                    self.__blocked.append(p)
                
                #checks every process in the __ready queue
                for t in self.__ready:
                    #if there's a process there that has status different from Ready and is not the GPP,
                    #than change its status to Ready
                    if t != p and t.get_status() != process.ProcessStatus.Ready:
                        t.set_status(process.ProcessStatus.Ready)

            #checks every process in the __blocked queue
            for p in self.__blocked:
                #if one's status is different from Blocked, than append it to the __ready queue
                if p.get_status() != process.ProcessStatus.Blocked:
                    self.__blocked.remove(p)
                    self.__ready.append(p)
        
        #Overall record of the scheduling policy
        print "\nRECORD:"
        for p in self.__finished:
            print p.name + " --> waiting time: " + str(p.waitingtime) + "; turnaround time: " + str(p.turnaroundtime) + "." 
                    
# ---------------- priority scheduling policy -----------------

# ++++++++++++++++ multiple queue scheduling policy +++++++++++++++++
    '''
        Method Multiple (Virtual) Queue Scheduling Policy
        @note - Simulates the Multiple Queue Scheduling Policy
    '''
    def mq_sch_pol(self):
        global LATEST_USED_PRIORITY 
        
        print "SCHEDULING POLICY: Multiple Queue"
        
        # starts all process as different threads
        for p in self.__ready:
                p.start()

        # infinite loop
        while True:
            
            # if both the __ready queue and the __blocked queue are empty, than finish
            if self.__ready.__len__() == 0 and self.__blocked.__len__() == 0:
                break
            
            # if the __ready queue is not empty
            if self.__ready.__len__() > 0:
                
                #finds the greater priority process (GPP)
                p = get_same_priority_process(self.__ready)
                pStatus = p.get_status()
            
                #if the GPP's status is Finished, than append it to the __finished queue
                if pStatus == process.ProcessStatus.Finished:
                    self.__ready.remove(p)
                    self.__finished.append(p)
                    
                #if the GPP's status is Ready, than change it to Setting Up
                elif pStatus == process.ProcessStatus.Ready:
                    p.set_status(process.ProcessStatus.SettingUp)
                
                #if the GPP's status is Blocked, than append it to the __blocked queue
                elif pStatus == process.ProcessStatus.Blocked:
                    self.__ready.remove(p)
                    self.__blocked.append(p)
                
                #checks every process in the __ready queue
                for t in self.__ready:
                    #if there's a process there that has status different from Ready and is not the GPP,
                    #than change its status to Ready
                    if t != p and t.get_status() != process.ProcessStatus.Ready:
                        
                        t.set_status(process.ProcessStatus.Ready)
                        if t.get_priority() > LATEST_USED_PRIORITY:
                            LATEST_USED_PRIORITY = t.priority

            #checks every process in the __blocked queue
            for p in self.__blocked:
                #if one's status is different from Blocked, than append it to the __ready queue
                if p.get_status() != process.ProcessStatus.Blocked:
                    self.__blocked.remove(p)
                    #if p's waiting time is greater than the process averagewait, than increase p's priority
                    if p.waitingtime > process.Process.averagewait:
                        p.increase_priority()
                    self.__ready.append(p)
                    
        
        #Overall record of the scheduling policy
        print "\nRECORD:"
        for p in self.__finished:
            print p.name + " --> waiting time: " + str(p.waitingtime) + "; turnaround time: " + str(p.turnaroundtime) + "." 

        
# ---------------- multiple queue scheduling policy -----------------

# @@@@@@@@@@@@@@@@ end of class Simulator @@@@@@@@@@@@@@@@


# @@@@@@@@@@@@@@@@ useful functions @@@@@@@@@@@@@@@@


# ++++++++++++++++ get greater priority process +++++++++++++++++

'''
    Function Get Greater Priority Process
    @note - This funcition checks which process in a given queue has the greater priority
            and returns it
    @param - procs: is an array containing processes
    @return - the process with the greater priority among the processes in the procs array 
'''
def get_greater_priority_process(procs):
    
    greater_priority_value = -1
    greater_priority_process = None
    
    for p in procs:
        if p.priority > greater_priority_value:
            greater_priority_value = p.priority
            greater_priority_process = p
            
    return greater_priority_process

# ---------------- get greater priority process -----------------

# ++++++++++++++++ get same priority process +++++++++++++++++

def get_same_priority_process(procs):
    
    global LATEST_USED_PRIORITY
    
    for p in procs:
        if p.priority == LATEST_USED_PRIORITY:
            return p
    
    p = get_greater_priority_process(procs)
    LATEST_USED_PRIORITY = p.priority
    
    return p

# ---------------- get same priority process -----------------

# @@@@@@@@@@@@@@@@ end of useful functions @@@@@@@@@@@@@@@@