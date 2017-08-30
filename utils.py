'''
Created on May 29, 2012

@author: gabriel
'''
import sys
import process


# @@@@@@@@@@@@@@@@ class Parser @@@@@@@@@@@@@@@@

'''
    Class Parser
    @note - This class was designed to read a text file containing the
            processes' data and parse it into processess' objects
    
'''
class Parser():

# ++++++++++++++++ read +++++++++++++++++
    
    '''
        Method Read
        @note - This method is responsible for reading the file and
                storing the text into the private __text variable
        @param - filePath: path to the file to be read
    '''
    def read(self, filePath):
        print "Reading file..."
        try:
            f = open(filePath, "r")
            self.__text = f.read()
        except IOError:
            print "Couldn't read the specified file."
            
# ---------------- read -----------------

# ++++++++++++++++ splittext +++++++++++++++++

    '''
        Method Split Text
        @note - This method is responsible for splitting the text stored
                into the private __text variable into an array of lines.
    '''    
    def split_text(self):
        lines = self.__text.splitlines()
    
        v = []
        for line in lines:
            v.append(line.split())
        
        return v
    
# ---------------- split_text -----------------

# ++++++++++++++++ validate +++++++++++++++++
    
    '''
        Method Validate
        @note - This method is responsible for validating the lines read from
                the text file. (Should be used after the  split_text method.)
        @param - stext: array containing the read file's lines.
    '''
    def validate(self, stext):
        print "Validating..."
   
        i = 0
        
        for item in stext:
            if i == 0:
                if item.__len__() != 1:
                    raise Exception("Invalid input file.")
            else:
                n = int(item[3])
                if item.__len__() != ((n * 2) + 3):
                    raise Exception("Invalid input file.")
            i += 1

# ---------------- validate -----------------

# ++++++++++++++++ create_processes +++++++++++++++++

    '''
        Method Create Processes
        @note - This method is respobsible for creating the process instances
                and grouping them into an array. (Should be used after the validate method.)
        @param - stext: array containing the read file's lines.
    
    '''
    def create_processes(self, stext):
        print "Creating processes..."
        
        self.__processes = []
        
        quantum = stext[0][0]
        del stext[0]
        
        for item in stext:
            cpuTime = []
            ioTime = []
            
            n = int(item[3])
            for i in range(0, n):
                cpuTime.append(int(item[4+(i*2)]))
                if i != n - 1:
                    ioTime.append(int(item[5+(i*2)]))
            
            proc = process.Process(int(quantum), item[0], int(item[1]), int(item[2]), int(item[3]), cpuTime, ioTime)
            self.__processes.append(proc)

# ---------------- create_processes -----------------        

# ++++++++++++++++ parse +++++++++++++++++

    '''
        Method Parse
        @note - This method is the one that should be accessed from outside this
                object. This is responsible for calling the other methods of this
                class in the right order and maintaining the right program control flow.
    '''
    def parse(self):
        stext = self.split_text()
        
        try:
            self.validate(stext)
        except:
            e = sys.exc_info()[1]
            print e
            sys.exit(1)
        
        self.create_processes(stext)
        
        return self.__processes
        
# ---------------- parse -----------------

# @@@@@@@@@@@@@@@@ end of class Parser @@@@@@@@@@@@@@@@