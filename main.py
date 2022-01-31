# Jim Palomo
# ECE 464 | All Project Combined
# Combination of all ECE 464 Projects
# Normal Circuit Simulation | Fault Simulation | Controllability | PRPG Analysis on c432.bench

import classes as cls
import logging as log
from function import *

def main(): 
    NodeList = cls.NodeList()
    NodeList.simulate()

if __name__ == "__main__":
    main()  # comment out if option 3: PRPG on bench c432.bench was ran

    # run if PRPG on bench c432.bench from main was already ran to save runtime
    # averageDetectionData()
    # noneDetectedData()
    # maxControlData()   
     
