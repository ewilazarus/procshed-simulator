'''
Created on May 29, 2012

@author: gabriel
'''
import sys
import utils
import simulator


'''
    Function Main
    @note - this is the first function ran by the program 
    @param - argv: an array with the parameters sent on command line
'''
def main(argv):
    
    # gets the right command input
    if argv.__len__() < 2:
        print "You must specify the file to be parsed."
    elif argv.__len__() > 2:
        print "Wrong number of parameters."
    else:
        filePath = sys.argv[1]
        
        # starts the file parser
        parser = utils.Parser()
        parser.read(filePath)
        procs = parser.parse()
        
#        DEBUG
#        print "Processes: "
#        for p in procs:
#            print p
        
        # starts the simulator
        sim = simulator.Simulator(procs)
        sim.start_simulation()
        
        
if __name__ == '__main__':
    main(sys.argv)