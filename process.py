'''
Created on May 29, 2012

@author: gabriel
'''
import threading
import time
from datetime import datetime

# @@@@@@@@@@@@@@@@ module variables @@@@@@@@@@@@@@@@

'''
    INTERVAL is the variable responsible for the "clock" of the process scheduler.
    The bigger INTERVAL is, the slower the "clock" will be.
'''
INTERVAL = 0.1

# @@@@@@@@@@@@@@@@ module variables @@@@@@@@@@@@@@@@

# @@@@@@@@@@@@@@@@ class ProcessStatus @@@@@@@@@@@@@@@@

'''
    Class Process Status
    @note - This class is just an enum that represents a process status.
'''
class ProcessStatus:
    SettingUp, Executing, Blocked, Ready, Finished = range(5)

# @@@@@@@@@@@@@@@@ class ProcessStatus @@@@@@@@@@@@@@@@

# @@@@@@@@@@@@@@@@ class Process @@@@@@@@@@@@@@@@

'''
    Class Process
    @note - This class is the blueprint for the process object. It contains several
            methods and attributes related to the process management.
'''
class Process (threading.Thread):

# ++++++++++++++++ class variables +++++++++++++++++

    # process count
    count = 0
    
    # quantum that will be used for the processes
    quantum = 0
   
    #the average time a process is held waiting
    averagewait = 0
    
# ---------------- class variables -----------------

# ++++++++++++++++ constructor +++++++++++++++++

    def __init__(    self,
                    quantum,
                    name,
                    setupTime,
                    priority,
                    cpuUsage,
                    cpuTime,
                    ioTime    ):
        
        #invokes threading.Thread constructor
        super(Process, self).__init__()
        
        #fills the process attributes with those parsed from the input file
        Process.quantum = quantum
        self.__name = name
        self.__setupTime = setupTime
        self.__priority = priority
        self.__cpuUsage = cpuUsage
        self.__cpuTime = cpuTime
        self.__ioTime = ioTime
        
        #set the process status to ready
        self.__status = ProcessStatus.Ready
        
        #the setupTimeTemp is a variable responsible for keeping the setup countdown
        #in case the process doesn't leave the CPU.
        self.__setupTimeTemp = self.__setupTime
        
        #flag that means if the process has just been in the CPU
        self.__leftCPU = True
        
        #attributes used for calculating the final record
        self.__waitingTime = 0
        self.__startTime = None
        self.__endTime = None
        
        #increases the process count
        Process.count += 1   
        
# ---------------- constructor -----------------

# ++++++++++++++++ getters & setters +++++++++++++++++
    
    def get_name(self):
        return self.__name
    
    def set_queue(self, queue):
        self.__queue = queue

    def getPriority(self):
        return self.__priority
    priority = property(getPriority)
    
    def increase_priority(self):
        self.__priority += 1
    
    def getName(self):
        return self.__name
    name = property(getName)

    def getWaitingTime(self):
        return self.__waitingTime
    waitingtime = property(getWaitingTime)
    
    def getTurnaroundTime(self):
        return self.__endTime - self.__startTime
    turnaroundtime = property(getTurnaroundTime)

    def set_status(self, status):
        self.__status = status
    
    def get_status(self):
        return self.__status
    
# ---------------- getters & setters -----------------

# ++++++++++++++++ str overload +++++++++++++++++

    def __str__(self):
        s = str(len(self.__cpuTime))
        
        return "  ---------------------------------------------------------------------------\n" + \
            "  | NAME: " + self.__name + " | SETUP_TIME: " + str(self.__setupTime) + \
            " | PRIORITY: " + str(self.__priority) + " | CPU_USAGE: " + s + " |\n" + \
            "  ---------------------------------------------------------------------------"

# ---------------- str overload -----------------

# ++++++++++++++++ Run +++++++++++++++++
    
    '''
        Method Run
        @note - This method is responsible for the process behavior.
                It is called by the thread.start() method.
    '''
    def run(self):
        #set the private __startTime variable to get the current time
        self.__startTime = datetime.now()
        
        #while the process status is not set as finished, do:
        while self.__status != ProcessStatus.Finished:
            
            #quantum counter. range: 0..quantum
            i = 0
            
            #"process left CPU" control flow
            if self.__leftCPU == True:
                setupTime = self.__setupTime
            else:
                setupTime = self.__setupTimeTemp
            
            #while counter i is lesser than quantum, do:
            while i < Process.quantum:
                
                #--------------------------------------------------
                #if process status is set to Setting Up
                if self.__status == ProcessStatus.SettingUp:        
                    self.__leftCPU = False
                    
                    #setup time count down
                    if setupTime > 0:
                        setupTime -= 1
                        self.__setupTimeTemp = setupTime
                    #if setup time = 0, than process is ready to execute
                    else:
                        self.__status = ProcessStatus.Executing
                    
                    print self.__name + " is now setting up." + "setup time left: " + str(setupTime)
                
                #--------------------------------------------------
                #if process status is set to Executing
                if self.__status == ProcessStatus.Executing:
                    self.__leftCPU = False
                    
                    #decreases the cpu time
                    self.__cpuTime[0] -= 1
                        
                    print self.__name + " is now executing." + " cpu time left: " + str(self.__cpuTime[0])
                    #if the cpu time reaches 0    
                    if self.__cpuTime[0] == 0:
                        del self.__cpuTime[0]
                        self.__status = ProcessStatus.Blocked
                
                #--------------------------------------------------
                #if process status is set to Blocked
                if self.__status == ProcessStatus.Blocked:
                    self.__leftCPU = True
                    
                    #if I/O time array length is greater than 0, than decreases the I/O time
                    if self.__ioTime.__len__() > 0:
                        self.__ioTime[0] -= 1
                        print self.__name + " is now blocked." + " I/O time left: " + str(self.__ioTime[0])
                        
                        #if the I/O time reaches 0
                        if self.__ioTime[0] == 0:
                            del self.__ioTime[0]
                            self.__status = ProcessStatus.Ready
                    
                    #TODO: VERIFICAR        
                    #if I/O time array length reaches 0, than process is finished
                    else:
                        self.__status = ProcessStatus.Finished
                        print self.__name + " IS NOW FINISHED."
                        break
                
                #--------------------------------------------------
                #if process status is set to Ready
                if self.__status == ProcessStatus.Ready:
                    self.__leftCPU = True
                    
                    #increases waiting time
                    self.__waitingTime += INTERVAL
                    Process.averagewait += self.waitingtime
                    Process.averagewait /= 2
                    
                    print self.__name + " is now ready."
                    
                #--------------------------------------------------
                
                
                time.sleep(INTERVAL)
                
                #refreshes the quantum counter
                i += 1
            
            #set the private __endTime variable to get the current time
            self.__endTime = datetime.now()

# ---------------- Run -----------------
            
# @@@@@@@@@@@@@@@@ end of class Process @@@@@@@@@@@@@@@@