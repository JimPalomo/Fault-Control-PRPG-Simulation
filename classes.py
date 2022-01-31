# Jim Palomo
# ECE 464 | All Project Combined
# Combination of all ECE 464 Projects
# Normal Circuit Simulation | Fault Simulation | Controllability | PRPG Analysis on c432.bench

import pickle
import logging as log
import os
from copy import *

import random   # not used for P3

class NodeList():
    def __init__(self):
        self.bench              = ""
        self.userOption         = ""
        self.nodes              = {} # list of nodes
        self.knownList          = []
        self.unknownList        = []
        self.numInputs          = 0
        self.inputTV            = ""
        self.faultList          = {}
        self.maxLevel           = 0
        
        self.noWireNodeList     = {}    # list of nodes w/ no wires
        self.noWireKnownList    = []
        self.noWireUnknownList  = []

        self.userTap            = ""
        self.LFSRIter           = ""

        self.options            = ["1", "2", "3"]
        self.choice             = ["a", "b", "c", "d", "A", "B", "C", "D"]
        self.benchFiles         = ["c17", "c432", "c499", "c880", "c1355", "c1908", 
                                    "c2670", "c3540", "c5315", "c6288", "hw1", "hw2.2", 
                                    "hw2", "p2"]    # c7552 currently taken off due to INPUT == OUTPUT case

        # clear logger  [module]
        with open('output.txt', 'w'):
            pass

        with open('data.csv', 'w'):
            pass

        # logger configurations [logs output to a .txt file (similar to output file but more convenient)]
        log.basicConfig(filename="output.txt", level=log.DEBUG, format='%(message)s')      

    def info(self):
        print(f"bench\t = {self.bench}")
        print(f"nodes\t = {self.nodes}")
        print(f"knownList\t = {self.knownList}")
        print(f"unknownList\t = {self.unknownList}")
        print(f"numInputs\t = {self.numInputs}")
        
    def __loadBenchFile(self):
        if self.userOption != "3":
            self.__inputBenchFile()
        else:
            self.__inputC432BenchFile()

        benchFile = self.__sortBenchFile()
        self.__processBenchFile(benchFile)
        self.noWireNodeList = deepcopy(self.nodes)
        self.__processWire()
    
    def __userOptionMain(self):
        self.userOption = input("\nSelect an option:\n 1: Fault Simulation\n 2: Controllability & Monte Carlo\n 3: PRPG on bench c432.bench\n > ")

        while self.userOption not in self.options:
            print("\nInvalid option selected")
            self.userOption = input("\nSelect an option:\n 1: Fault Simulation\n 2: Controllability & Monte Carlo\n 3: PRPG on bench c432.bench\n > ")

        print()

    def __userOptionFaultSim(self):
        self.userOption = input("\nSelect an option:\n A. Normal Circuit Simulation\n B. Single TV single fault\n C. Single TV all faults\n D. Best 5 TV for all faults\n > ")

        while self.userOption not in self.choice:
            print("\nInvalid option selected")
            self.userOption = input("\nSelect an option:\n A. Normal Circuit Simulation\n B. Single TV single fault\n C. Single TV all faults\n D. Best 5 TV for all faults\n > ")

        print()

        return self.userOption

    def __logResults(self):
        outputFile = open("data.csv", "w")

        outputFile.write("fault,detected,level,c0,c1,c0/c1,n0,n1,n1/n0" + "\n")

        for fault in self.faultList:
            curFault = self.faultList[fault].name.split("-")
            if fault.count("-") == 1:   # input/output
                outputFile.write(f"{self.faultList[fault].name},{self.faultList[fault].detected},{self.nodes[curFault[0]].level},{self.nodes[curFault[0]].c0},{self.nodes[curFault[0]].c1},{self.nodes[curFault[0]].n0},{self.nodes[curFault[0]].n1}" + "\n")
                    
            else:   # wire
                outputFile.write(f"""{self.faultList[fault].name},{self.faultList[fault].detected},{self.nodes[f"{curFault[0]}-{curFault[1]}"].level},{self.nodes[f"{curFault[0]}-{curFault[1]}"].c0},{self.nodes[f"{curFault[0]}-{curFault[1]}"].c1},{self.nodes[f"{curFault[0]}-{curFault[1]}"].n0},{self.nodes[f"{curFault[0]}-{curFault[1]}"].n1}""" + "\n")        

        outputFile.close()

        # Save model as .pkl file
        with open('NodeList.pkl', 'wb') as f:
            pickle.dump([self.nodes, self.faultList, self.maxLevel], f)
            f.close()  

    # simulate program
    def simulate(self):
        # while userChoice != "q"
        self.__userOptionMain()

        # Fault Simulation (single fault, full fault list, best 5 TV)
        if self.userOption == "1":
            self.__userOption1_FaultSim()

        # Controllability & Monte Carlo
        elif self.userOption == "2":
            self.__userOption2_ControlandMC()
        
        else:   # self.userOption == "3":
            self.__userOption3_PRPG()
        
        # save NodeList as .pkl file and save data as csv (for option 3)
        self.__logResults()

    # 1: Fault Simulation
    def __userOption1_FaultSim(self):
        # A1: ask user for bench file 
        print("Available bench files:")     
        print(" " + str(self.benchFiles)[1:][:-1])      
        print()
        
        # load bench file and update known/unknown lists
        self.__loadBenchFile()
        self.__appendKnownUnknownList(self.nodes, self.knownList, self.unknownList, self.inputTV)
        self.__appendKnownUnknownList(self.noWireNodeList, self.noWireKnownList, self.noWireUnknownList, self.inputTV)
                
        # A2: print netlist
        print(f"""{"NodeList":^115}""")
        log.info(f"""{"NodeList":^115}""")
        
        print("-" * 115)
        log.info("-" * 115)
        
        print(f"""{"Name":^10}{"Type":<15}{"Gate":<15}{"Input":<35}{"Operation":<30}{"Output":<30}""")
        log.info(f"""{"Name":^10}{"Type":<15}{"Gate":<15}{"Input":<35}{"Operation":<30}{"Output":<30}""")
        
        print("-" * 115)            
        log.info("-" * 115)            
        
        for node in self.noWireNodeList:
            print(f'{node:^10}{self.noWireNodeList[node].pos:<15}{self.noWireNodeList[node].gate:<15}{self.noWireNodeList[node].ip:<35}{self.noWireNodeList[node].opr:<30}{self.noWireNodeList[node].value:<30}')
            log.info(f'{node:^10}{self.noWireNodeList[node].pos:<15}{self.noWireNodeList[node].gate:<15}{self.noWireNodeList[node].ip:<35}{self.noWireNodeList[node].opr:<30}{self.noWireNodeList[node].value:<30}')
        
        # B1: ask user for test vector
        self.__inputUserTV(self.numInputs, self.inputTV)   
        
        # update input values given user test vector 
        inputTVIndex = 0
        for node in self.knownList:
            self.nodes[node].value = self.inputTV[inputTVIndex] + "/" + self.inputTV[inputTVIndex]
            inputTVIndex += 1
        
        # B2: ask user for options
        userChoice = self.__userOptionFaultSim()
        
        # option A: normal circuit simulation
        if userChoice == "a" or userChoice == "A":
            self.__userChoiceA_NormalCircSim()
        
        # option B: single fault
        elif userChoice == "b" or userChoice == "B":
            self.__userChoiceB_SingleFault()
        
        # option C: generate full fault list and fault sim on each fault
        elif userChoice == "c" or userChoice == "C":
            self.__userChoiceC_AllFault()
        
        # option D: full fault list and generate 5 tvs to cover faults (random)
        else: # userChoice == "c":
            self.__userChoiceD_Generate4TV()

    # 1: 2: Controllability & Monte Carlo
    def __userOption2_ControlandMC(self):
        print("Available bench files:")     
        print(" " + str(self.benchFiles)[1:][:-1])      
        print()
        
        # load bench
        self.__loadBenchFile()
        self.__appendKnownUnknownList(self.nodes, self.knownList, self.unknownList, self.inputTV)
        self.__appendKnownUnknownList(self.noWireNodeList, self.noWireKnownList, self.noWireUnknownList, self.inputTV)
        
        # update n0/n1
        self.__updateInputn0n1()

        # generate full fault list
        self.__fullFaultList()

        # simulate control
        self.__simulateControl()

        # transfer control values
        self.__transferControl()

        originalKnownList = deepcopy(self.knownList)
        originalUnknownList = deepcopy(self.unknownList)
        self.__simulateMonteCarlo(originalKnownList, originalUnknownList)
        
        # display Controllability values
        controlOption = self.__displayControl()

        # display MC values
        self.__displayMonteCarlo(controlOption)

        # display Controllability and MC analysis
        self.__displayControlandMCResults(controlOption)
        
    # 3: PRPG on bench c432.bench           
    def __userOption3_PRPG(self):
        # option 4: PRPG

        # load and process bench file
        self.__loadBenchFile()

        # 9V algebra starts here, comment out to remove user input
        # noWireKnownList, noWireUnknownList, noWireInputTV = [], [], deepcopy(self.inputTV) # for control
        self.__appendKnownUnknownList(self.nodes, self.knownList, self.unknownList, self.inputTV)
        self.__appendKnownUnknownList(self.noWireNodeList, self.noWireKnownList, self.noWireUnknownList, self.inputTV)
        # add user to enter fault

        # update n0/n1 for inputs
        self.__updateInputn0n1()

        # generate full fault list
        self.__fullFaultList()

        # simulate control
        self.__simulateControl()

        # transfer control from noWireNodeList to nodes dict
        self.__transferControl()

        validTap = False

        while validTap == False:
            self.userTap = input("Select LFSR tap configuration:\n a: h=1\n b: h=1,3,5\n c: h=2,4,6\n d: h=6,7,8\n> ")
            if self.userTap == "a" or self.userTap == "b" or self.userTap == "c" or self.userTap == "d":
                print(f"\nSelected tap configuration: {self.userTap}\n")
                validTap = True
            else:
                print(f"\n{self.userTap} is an invalid tap configuration")

        originalKnownList = deepcopy(self.knownList)
        originalUnknownList = deepcopy(self.unknownList)
        self.__simulateMonteCarlo_PRPG(originalKnownList, originalUnknownList)
            
        # print fault, numDetected, level
        # Fault | numDetected | Level | c0 | c1 | c0/c1 | n0 | n1 | n1/n0
        print("No. detected -> number of faults detected at output\n")
        print("-"*75)
        log.info("-"*75)        
            
        print(f"""|{"Fault":^10} | {"No. detected":^15} | {"Level":^10} | {"c0":^5} | {"c1":^5} | {"n0":^5} | {"n1":^5}|""")
        log.info(f"""|{"Fault":^10} | {"No. detected":^15} | {"Level":^10} | {"c0":^5} | {"c1":^5} | {"n0":^5} | {"n1":^5}|""")
            
        print("-"*75)
        log.info("-"*75)
            
        for fault in self.faultList:
            curFault = self.faultList[fault].name.split("-")
            if fault.count("-") == 1:   # input/output
                print(f"|{self.faultList[fault].name:^10} | {self.faultList[fault].detected:^15} | {self.nodes[curFault[0]].level:^10} | {self.nodes[curFault[0]].c0:^5} | {self.nodes[curFault[0]].c1:^5} | {self.nodes[curFault[0]].n0:^5} | {self.nodes[curFault[0]].n1:^5}|")
                log.info(f"|{self.faultList[fault].name:^10} | {self.faultList[fault].detected:^15} | {self.nodes[curFault[0]].level:^10} | {self.nodes[curFault[0]].c0:^5} | {self.nodes[curFault[0]].c1:^5} | {self.nodes[curFault[0]].n0:^5} | {self.nodes[curFault[0]].n1:^5}|")
                    
            else:   # wire
                print(f"""|{self.faultList[fault].name:^10} | {self.faultList[fault].detected:^15} | {self.nodes[f"{curFault[0]}-{curFault[1]}"].level:^10} | {self.nodes[f"{curFault[0]}-{curFault[1]}"].c0:^5} | {self.nodes[f"{curFault[0]}-{curFault[1]}"].c1:^5} | {self.nodes[f"{curFault[0]}-{curFault[1]}"].n0:^5} | {self.nodes[f"{curFault[0]}-{curFault[1]}"].n1:^5}|""")
                log.info(f"""|{self.faultList[fault].name:^10} | {self.faultList[fault].detected:^15} | {self.nodes[f"{curFault[0]}-{curFault[1]}"].level:^10} | {self.nodes[f"{curFault[0]}-{curFault[1]}"].c0:^5} | {self.nodes[f"{curFault[0]}-{curFault[1]}"].c1:^5} | {self.nodes[f"{curFault[0]}-{curFault[1]}"].n0:^5} | {self.nodes[f"{curFault[0]}-{curFault[1]}"].n1:^5}|""")

        print(f"\n{len(self.faultList)} faults have been simulated") 
        log.info(f"\n{len(self.faultList)} faults have been simulated") 

        # total fault simulations = user TV * 1064 faults in c432.bench
        print(f"\nNumber of fault simulations: total fault simulations = user TV * 1064 faults in c432.bench")
        log.info(f"\nNumber of fault simulations: total fault simulations = user TV * 1064 faults in c432.bench")

        print(f"\n{self.LFSRIter} * 1064 faults = {int(self.LFSRIter)*1064} fault simulations")
        log.info(f"\n{self.LFSRIter} * 1064 faults = {int(self.LFSRIter)*1064} fault simulations")

    def __userChoiceA_NormalCircSim(self):
        originalKnownList = deepcopy(self.knownList)
        originalUnknownList = deepcopy(self.unknownList)                
        self.__simulateCircuit()

        print(f"""{"NodeList":^115}""")
        log.info(f"""\n{"NodeList":^115}""")

        print("-" * 115)
        log.info("-" * 115)
        
        print(f"""{"Name":^10}{"Type":<15}{"Gate":<15}{"Input":<35}{"Operation":<30}{"Output":<30}""")
        log.info(f"""{"Name":^10}{"Type":<15}{"Gate":<15}{"Input":<35}{"Operation":<30}{"Output":<30}""")
        
        print("-" * 115)
        log.info("-" * 115)

        for node in self.noWireNodeList:
            print(f'{node:^10}{self.noWireNodeList[node].pos:<15}{self.noWireNodeList[node].gate:<15}{self.noWireNodeList[node].ip:<35}{self.noWireNodeList[node].opr:<30}{self.nodes[node].value:<30}')
            log.info(f'{node:^10}{self.noWireNodeList[node].pos:<15}{self.noWireNodeList[node].gate:<15}{self.noWireNodeList[node].ip:<35}{self.noWireNodeList[node].opr:<30}{self.nodes[node].value:<30}')
        
        print()

    def __userChoiceB_SingleFault(self):
        # C1: ask user for single fault f
        userFault = input("Enter a single fault (e.g. a-1 or d-a-0)> ")
        log.info(f"\nUser fault: {userFault}")

        # add check user fault and add to Fault List
        self.__checkUserFault(userFault)

        # C2: perform fault simulation
        self.__activateFault(userFault)

        originalKnownList = deepcopy(self.knownList)
        originalUnknownList = deepcopy(self.unknownList)                
        self.__simulateCircuit()

        print(f"""{"NodeList":^115}""")
        log.info(f"""\n{"NodeList":^115}""")

        print("-" * 115)
        log.info("-" * 115)

        print(f"""{"Name":^10}{"Type":<15}{"Gate":<15}{"Input":<35}{"Operation":<30}{"Output":<30}""")
        log.info(f"""{"Name":^10}{"Type":<15}{"Gate":<15}{"Input":<35}{"Operation":<30}{"Output":<30}""")
        
        print("-" * 115)
        log.info("-" * 115)
        
        for node in self.noWireNodeList:
            print(f'{node:^10}{self.noWireNodeList[node].pos:<15}{self.noWireNodeList[node].gate:<15}{self.noWireNodeList[node].ip:<35}{self.noWireNodeList[node].opr:<30}{self.nodes[node].value:<30}')
            log.info(f'{node:^10}{self.noWireNodeList[node].pos:<15}{self.noWireNodeList[node].gate:<15}{self.noWireNodeList[node].ip:<35}{self.noWireNodeList[node].opr:<30}{self.nodes[node].value:<30}')
        
        print()

        detected, notDetected = [], []

        for node in self.nodes:
            if self.nodes[node].pos == "OUTPUT":
                if "u" in self.nodes[node].value:
                    # print(f"Fault ({userFault}) NOT DETECTED at output node {node}")
                    notDetected.append(node)

                elif self.nodes[node].value[0] != self.nodes[node].value[2]:
                    # print(f"Fault ({userFault}) DETECTED at output node {node}")
                    detected.append(node)

                else:
                    # print(f"Fault ({userFault}) NOT DETECTED")
                    notDetected.append(node)

        # check to see if node is detected
        if len(detected) > 0:
            print("Node was detected at output node(s):", end=" ")
            log.info("\nNode was detected at output node(s):", end=" ")
            for node in detected:
                print(node, end=" ")
                log.info(node, end=" ")

        else:
            print(f"Fault ({userFault}) NOT DETECTED at output nodes")
            log.info(f"\nFault ({userFault}) NOT DETECTED at output nodes")

        print()

        # userChoice = input("\n\nWhat would you like to do?\n   default: go back to choose options (enter)\n   another fault (f)\n   another tv (t)\n   another bench (b)\n   quit(q)\n> ")
            
    def __userChoiceC_AllFault(self):
        # D1: generate full fault list F
        self.__fullFaultList()
        
        print("Full fault list: ", end="")
        for fault in self.faultList:
            print(fault, end=", ")
        
        print("\n")

        # D2: perform fault simulation on all faults
        # update MC with options for LFSR and number of test vectors
        originalKnownList = deepcopy(self.knownList)
        originalUnknownList = deepcopy(self.unknownList)
        self.__simulateAllFaults(originalKnownList, originalUnknownList)
        
        print()

    def __userChoiceD_Generate4TV(self):
        # E1: generate full fault list F
        self.__fullFaultList()
        
        print("Full fault list: ", end="")
        log.info("\nFull fault list:")

        for fault in self.faultList:
            print(fault, end=", ")
            log.info(f"{fault}")
        
        # E2: generate another 4 TV
        print("\n\nGenerating 4 additional TV along with User's TV...\n")
        log.info("\nAdditional TV along with User's TV...\n")
        
        print(f"User TV  : {self.inputTV}")
        log.info(f"User TV  : {self.inputTV}")
        
        for i in range(4):
            tv = self.__randomizeTV(self.numInputs)
            print(f"Generated: {tv}")
            log.info(f"Generated: {tv}")

    def __displayControl(self):
        controlOption = input("Control Options\n 1: Display only output nodes \n 2: Display all nodes \n > ")
        
        while controlOption not in ["1", "2"]:
            print("\nInvalid selection\n")
            controlOption = input("Control Options\n 1: Display only output nodes \n 2: Display all nodes \n > ")

        print(f'{"Node":^10} | {"Control Results (c0, c1)":^30}')
        log.info(f'{"Node":^10} | {"Control Results (c0, c1)":^30}')

        print(f"-" * 43)
        log.info(f"-" * 43)

        # display control values ------------------
        if controlOption == "1":
            for node in self.nodes:
                if self.nodes[node].pos == "OUTPUT":
                    # string cast just in case print out is a list
                    control = f'({self.nodes[node].c0}, {self.nodes[node].c1})'
                    print(f"""{f'{self.nodes[node].name}':^10} | {control:^30}""")
                    log.info(f"""{f'{self.nodes[node].name}':^10} | {control:^30}""")

        else:   # 2
            for node in self.nodes:
                control = f'({self.nodes[node].c0}, {self.nodes[node].c1})'
                print(f"""{f'{self.nodes[node].name}':^10} | {control:^30}""")
                log.info(f"""{f'{self.nodes[node].name}':^10} | {control:^30}""")
            
        input("\nPress enter to continue...\n") 
        print("\n" + "="*150 + "\n")
        log.info("\n" + "="*150 + "\n")

        return controlOption

    def __displayMonteCarlo(self, controlOption):
        print(f'{"Node":^10} | {"Monte Carlo Results (n0, n1)":^30}')
        log.info(f'{"Node":^10} | {"Monte Carlo Results (n0, n1)":^30}')
        
        print(f"-" * 45)
        log.info(f"-" * 45)

        userInput = ""

        if controlOption == "1":
            for node in self.nodes:
                if self.nodes[node].pos == "OUTPUT":
                    mc = f'({self.nodes[node].n0}, {self.nodes[node].n1})'
                    print(f"""{f'{self.nodes[node].name}':^10} | {mc:^30}""")
                    log.info(f"""{f'{self.nodes[node].name}':^10} | {mc:^30}""")
        
        else:   # 2
            for node in self.nodes:
                mc = f'({self.nodes[node].n0}, {self.nodes[node].n1})'
                print(f"""{f'{self.nodes[node].name}':^10} | {mc:^30}""")
                log.info(f"""{f'{self.nodes[node].name}':^10} | {mc:^30}""")
                        
        input("\nPress enter to continue...\n")  
        print("\n" + "="*150 + "\n")
        log.info("\n" + "="*150 + "\n")        

    def __qualAnalysis(self, node):
        qualc0c1 = ""
        qualn0n1 = ""
        correlate = ""    

        if int(self.nodes[node].c0) < int(self.nodes[node].c1):
            # qualc0c1 = f"{self.nodes[node].c0} < {self.nodes[node].c1}"
            qualc0c1 = "0"
        elif int(self.nodes[node].c0) > int(self.nodes[node].c1):
            qualc0c1 = "1"
        else:   # c0 == c1
            qualc0c1 = "="

        if int(self.nodes[node].n0) < int(self.nodes[node].n1):
            qualn0n1 = "1"
        elif int(self.nodes[node].n0) > int(self.nodes[node].n1): 
            qualn0n1 = "0"
        else: # n0 == n1
            qualn0n1 = "="

        if qualc0c1 == qualn0n1:
            correlate = "Agree"
        else:
            correlate = "Disagree"

        return qualc0c1, qualn0n1, correlate    

    def __displayControlandMCResults(self, controlOption):    
        print(f'{"""Node List | Output Node Results | "=" under QL means values are equal""":^115}')
        log.info(f'{"""Node List | Output Node Results | "=" under QL means values are equal""":^115}')
        
        print(f"-" * 115)
        log.info(f"-" * 115)

        print(f"""{"Node":^10}{"Controllability":^20}{"Monte-Carlo":^20}{"":<5}{"Quantitative":^19}{"":<5}{"Qualitative":^19}{"":<5}{"Result":<10}""")
        print(f"""{"":^10}{"(c0, c1)":^20}{"(n0, n1)":^20}{"":<5}{"c0/c1":<8}{"vs.":<5}{"n1/n0":<10}{"":<5}{"c":<4}{"vs.":<5}{"n":<5}{"":<10}""")

        log.info(f"""{"Node":^10}{"Controllability":^20}{"Monte-Carlo":^20}{"":<5}{"Quantitative":^19}{"":<5}{"Qualitative":^19}{"":<5}{"Result":<10}""")
        log.info(f"""{"":^10}{"(c0, c1)":^20}{"(n0, n1)":^20}{"":<5}{"c0/c1":<8}{"vs.":<5}{"n1/n0":<10}{"":<5}{"c":<4}{"vs.":<5}{"n":<5}{"":<10}""")

        print(f"-" * 115)
        log.info(f"-" * 15)

        userInput = ""

        if controlOption == "1":
            for node in self.nodes:
                if self.nodes[node].pos == "OUTPUT":
                    qualc0c1, qualn0n1, correlate = self.__qualAnalysis(node)

                    control = f'({self.nodes[node].c0}, {self.nodes[node].c1})'
                    mc = f'({self.nodes[node].n0}, {self.nodes[node].n1})'

                    print(f"""{f'{self.nodes[node].name}':^10}{f'{control:^20}'}{"":5}{f'{mc:^10}'}{"":<10}{f'{float(self.nodes[node].c0) / float(self.nodes[node].c1):.3f}':<8}{"vs.":<5}{f'{float(self.nodes[node].n1) / float(self.nodes[node].n0):.3f}':<10}{"":<5}{qualc0c1:<4}{"vs.":<5}{qualn0n1:<3}{"":<8}{correlate:<10}""")
                    log.info(f"""{f'{self.nodes[node].name}':^10}{f'{control:^20}'}{"":5}{f'{mc:^10}'}{"":<10}{f'{float(self.nodes[node].c0) / float(self.nodes[node].c1):.3f}':<8}{"vs.":<5}{f'{float(self.nodes[node].n1) / float(self.nodes[node].n0):.3f}':<10}{"":<5}{qualc0c1:<4}{"vs.":<5}{qualn0n1:<3}{"":<8}{correlate:<10}""")
        
        else: # 2    
            for node in self.nodes:
                    qualc0c1, qualn0n1, correlate = self.__qualAnalysis(node)

                    control = f'({self.nodes[node].c0}, {self.nodes[node].c1})'
                    mc = f'({self.nodes[node].n0}, {self.nodes[node].n1})'

                    print(f"""{f'{self.nodes[node].name}':^10}{f'{control:^20}'}{"":5}{f'{mc:^10}'}{"":<10}{f'{float(self.nodes[node].c0) / float(self.nodes[node].c1):.3f}':<8}{"vs.":<5}{f'{float(self.nodes[node].n1) / float(self.nodes[node].n0):.3f}':<10}{"":<5}{qualc0c1:<4}{"vs.":<5}{qualn0n1:<3}{"":<8}{correlate:<10}""")
                    log.info(f"""{f'{self.nodes[node].name}':^10}{f'{control:^20}'}{"":5}{f'{mc:^10}'}{"":<10}{f'{float(self.nodes[node].c0) / float(self.nodes[node].c1):.3f}':<8}{"vs.":<5}{f'{float(self.nodes[node].n1) / float(self.nodes[node].n0):.3f}':<10}{"":<5}{qualc0c1:<4}{"vs.":<5}{qualn0n1:<3}{"":<8}{correlate:<10}""")
                                
        print("\n" + "="*150 + "\n")
        log.info("\n" + "="*150 + "\n")
        print()

    def __activateFault(self, fault):
        splitFault = self.faultList[fault].name.split("-")

        # check input fault
        if self.nodes[splitFault[0]].pos == "INPUT":
                self.nodes[splitFault[0]].fault = True
                self.nodes[splitFault[0]].sa_fault = splitFault[1]     
                self.nodes[splitFault[0]].value = self.nodes[splitFault[0]].value[:-1] + self.nodes[splitFault[0]].sa_fault
            # self.__addInputFaults()

        else:   # check output and wire fault
            if self.faultList[fault].name.count("-") == 1: # output
                self.nodes[splitFault[0]].fault = True
                self.nodes[splitFault[0]].sa_fault = splitFault[1]
            else:   # wire
                self.nodes[splitFault[0]].fault = True
                self.nodes[splitFault[0]].sa_fault = splitFault[2]            

    # __simulateCircuit: normal circuit simulation  
    def __simulateCircuit(self):
        G = Gate()  # create instance of Gate class
        while len(self.unknownList) != 0:
            for node in self.unknownList:          
                returnedInputs = self.__checkInputs(node, self.unknownList)
                check = returnedInputs[0]
                inputs = returnedInputs[1]

                if check == False:  # check = False when inputs do not have a value
                    continue
                else:               # inputs have values
                    if self.nodes[node].pos == "WIRE":
                        op = "WIRE"
                    else:
                        op = self.nodes[node].gate

                    # update level
                    self.__updateLevel(node, inputs)

                    # logical operation
                    G._operation(node, inputs, self.nodes, op)

                    self.unknownList.remove(node)
                    self.knownList.append(node)

    # __simulateControl: simulates controllability throughout the circuit
    def __simulateControl(self):
        print("Simulating control...\n")
        G = Gate()  # create instance of Gate class
        while len(self.noWireUnknownList) != 0:
            for node in self.noWireUnknownList:
                returnedInputs = self.__checkInputs(node, self.noWireUnknownList, "c")
                check = returnedInputs[0]
                inputs = returnedInputs[1]

                if check == False:  # check = False when inputs do not have a value
                    continue
                else:               # inputs have values
                    op = self.noWireNodeList[node].gate

                    G._operation(node, inputs, self.noWireNodeList, op, "c")

                    self.noWireUnknownList.remove(node)
                    self.noWireKnownList.append(node)    

    # simulates MC on given TV either 1000 random, non-repeating TV or exhaustively when number of inputs <= 10
    def __simulateMonteCarlo(self, originalKnownList, originalUnknownList):
        print("Simulating all faults in fault list...\n")
        TV = []

        # determine TV to be used
        if self.numInputs <= 10:
            TV = self.__exhaustInputs()
        else:
            TV = self.__random1000TV() # optional: replace with __random1000TV 

        for fault in self.faultList:
            for tv in TV:                                    
                # each iteration will test one tv at a time from a list of TV

                # reset knownList and unknownList
                self.knownList = deepcopy(originalKnownList)
                self.unknownList = deepcopy(originalUnknownList)

                # update input TV of NodeList with provided TV
                for i in range(self.numInputs):
                    self.nodes[self.knownList[i]].value = f"{tv[i]}/{tv[i]}"
                    if tv[i] == "0":
                        self.nodes[self.knownList[i]].n0 += 1
                    else:
                        self.nodes[self.knownList[i]].n1 += 1

                # activate fault
                self.__activateFault(fault)

                self.__simulateCircuit()

                self.__faultCheck(fault)
                
                # reset NodeList node values
                for node in self.nodes:
                    self.nodes[node].value = "-"
                    self.nodes[node].sa_fault = "-"
                    self.nodes[node].fault = False                

    # simulates MC on given TV either 1000 random, non-repeating TV or exhaustively when number of inputs <= 10
    def __simulateMonteCarlo_PRPG(self, originalKnownList, originalUnknownList):
        print("Simulating all faults in fault list...\n")
        TV = []

        # determine TV to be used
        if self.numInputs <= 10:
            TV = self.__exhaustInputs()
        else:
            TV = self.__LFSR_userAmount() # optional: replace with __random1000TV 

        for fault in self.faultList:
            for tv in TV:                                    
                # each iteration will test one tv at a time from a list of TV

                # reset knownList and unknownList
                self.knownList = deepcopy(originalKnownList)
                self.unknownList = deepcopy(originalUnknownList)

                # update input TV of NodeList with provided TV
                for i in range(self.numInputs):
                    self.nodes[self.knownList[i]].value = f"{tv[i]}/{tv[i]}"
                    if tv[i] == "0":
                        self.nodes[self.knownList[i]].n0 += 1
                    else:
                        self.nodes[self.knownList[i]].n1 += 1

                # activate fault
                self.__activateFault(fault)

                self.__simulateCircuit()

                self.__faultCheck(fault)
                
                # reset NodeList node values
                for node in self.nodes:
                    self.nodes[node].value = "-"
                    self.nodes[node].sa_fault = "-"
                    self.nodes[node].fault = False 

    # simulate all faults given the user TV
    def __simulateAllFaults(self, originalKnownList, originalUnknownList):
        print("Simulating all faults in fault list...\n")
        TV = []

        # determine TV to be used
        # TV = self.__exhaustInputs()
        TV.append(self.inputTV)

        print(f"""All Faults simulated on TV = {self.inputTV:<10}\n\n{"Fault":<10} {"Detected ?":<15}""")
        log.info(f"""\nAll Faults simulated on TV = {self.inputTV:<10}\n\n{"Fault":<10} {"Detected ?":<15}""")

        for fault in self.faultList:
            for tv in TV:                                    
                # each iteration will test one tv at a time from a list of TV

                # reset knownList and unknownList
                self.knownList = deepcopy(originalKnownList)
                self.unknownList = deepcopy(originalUnknownList)

                # update input TV of NodeList with provided TV
                for i in range(self.numInputs):
                    self.nodes[self.knownList[i]].value = f"{tv[i]}/{tv[i]}"
                    if tv[i] == "0":
                        self.nodes[self.knownList[i]].n0 += 1
                    else:
                        self.nodes[self.knownList[i]].n1 += 1
                    
                # activate fault
                self.__activateFault(fault)

                self.__simulateCircuit()

                self.__faultCheck(fault)
                
                # display fault result
                if self.faultList[fault].detected != 0:
                    print(f"""{fault:<10} {"Detected ✓":<15}""")
                    log.info(f"""{fault:<10} {"Detected ✓":<15}""")
                else:
                    print(f"""{fault:<10} {"Detected ✗":<15}""")
                    log.info(f"""{fault:<10} {"Detected ✗":<15}""")

                # reset NodeList node values
                for node in self.nodes:
                    self.nodes[node].value = "-"
                    self.nodes[node].sa_fault = "-"
                    self.nodes[node].fault = False   

    def __faultCheck(self, fault):
        faultFound = False

        for node in self.nodes:
            if self.nodes[node].pos == "OUTPUT":
                result = self.nodes[node].value.split("/")

                if result[0] == "u" or result[1] == "u":
                    pass    # do nothing to fault detected counter (order of statement matters, check unknowns first)
                elif result[0] == result[1]:  # same 1/1 or 0/0
                    pass    # fault 
                else: # different 0/1 or 1/0 and fault propagated to output as D or D'
                    self.faultList[fault].detected += 1

    # __transferControl: transfer control values from control Node List to universal
    def __transferControl(self):
        splitNode = ""
        for node in self.nodes:
            if node.count("-") == 0:    # x
                self.nodes[node].c0 = self.noWireNodeList[node].c0
                self.nodes[node].c1 = self.noWireNodeList[node].c1
            else: # x-y
                splitNode = node.split("-")[1]  # y
                self.nodes[node].c0 = self.noWireNodeList[splitNode].c0
                self.nodes[node].c1 = self.noWireNodeList[splitNode].c1    

    # __fullFaultList:
    def __fullFaultList(self):  
        print("Generating full fault list...\n")      
        for node in self.nodes:
            # self.faultList.append(f"{node}-0")
            # self.faultList.append(f"{node}-1")
            self.faultList[(f"{node}-0")] = Fault(f"{node}-0")
            self.faultList[(f"{node}-1")] = Fault(f"{node}-1")            

    # updateInputn0n1:
    def __updateInputn0n1(self):
        for tv in self.inputTV:
            if self.nodes[tv].value == "0/0":
                self.nodes[tv].n0 += 1
            elif self.nodes[tv].value == "1/1":
                self.nodes[tv].n1 += 1
            else:
                pass # unknown

    def __addInputFaults(self):
        for node in self.nodes:
            if self.nodes[node].pos == "INPUT" and self.nodes[node].fault == True:
                self.nodes[node].value = self.nodes[node].value[:-1] + self.nodes[node].sa_fault

    # updateLevel: updateLevel
    def __updateLevel(self, node, inputs):
        levels = []
        newLevel = 0 

        for ip in inputs:
            # two options: 
            # y-i -> i
            # g -> g-a, g-b
            # if ip == "i":
            #     print

            if self.nodes[node].pos == "WIRE":
                levels.append(self.nodes[ip].level)
                newLevel = max(levels)
            else:
                inputList = ip.split("-")            
                levels.append(self.nodes[inputList[1]].level)
                newLevel = max(levels) + 1

        self.nodes[node].level = newLevel

        if newLevel > self.maxLevel:
            self.maxLevel = newLevel

    # checkInputs: check the inputs to see if the provided inputs contain values (0 or 1 | control values exists)
    # Return: returns True if the inputs have known values else false and provides the inputs  
    def __checkInputs(self, node, unknownList, option="-"):

        inputs = self.nodes[node].ip.split(",")   # split on "," and make into list
        
        controlInputs   = []   # controlled inputs, remove wire notation
        
        if option == "c":
            for ip in inputs:
                ip = ip.split("-")
                controlInputs.append(ip[1])
        
        if option == "c":   # control
            for ip in controlInputs:
                if ip in unknownList:
                    return False, inputs
        else:
            for ip in inputs:
                if self.nodes[ip].pos == "WIRE":
                    # inputList = ip.split("-")
                    # curIP = inputList[1]

                    # if curIP in unknownList:
                    #     return False, inputs
                    if ip in unknownList:
                        return False, inputs
                        

                else:
                    if ip in unknownList:
                        return False, inputs

        return True, inputs

    # Bench File

    def __appendKnownUnknownList(self, NodeList, knownList, unknownList, inputTV):
        # append known and unknown values to proper list for iteration
        for node in NodeList:
            if NodeList[node].pos == "INPUT":
                knownList.append(node)
                inputTV += node
            else:
                unknownList.append(node)           

        # save numInputs for # of input vectors
        self.numInputs = len(knownList)

    def __inputBenchFile(self):
        inputFile = ""

        while True:
            inputFile = input("Enter bench file> ")

            if not os.path.isfile(f"bench/{inputFile}.bench"):
                print(f'File {inputFile} not found')
                continue
            break

        inputFile = open(f"bench/{inputFile}.bench", "r")

        print(f'\nTesting {inputFile.name}...\n')

        self.bench = inputFile

    def __inputC432BenchFile(self):
        inputFile = ""

        print("The bench file used in this project is c432.bench")
        inputFile = open("bench/c432.bench", "r")

        print(f'\nTesting {inputFile.name}...\n')
        # log.info(f'Testing {inputFile.name}...\n')        

        self.bench = inputFile
        
    # sortBenchFile: sorts the provided bench file (in order of INPUT OUTPUT INTERNAL)
    # Return: sorted version of the provided bench file
    def __sortBenchFile(self):
        IN = []     # INPUT
        OUT = []    # OUTPUT
        ETC = []    # could be internal or part of output (rest of file)
        sortedBenchFile = []

        for line in self.bench:
            if line[0] == "#" or line == "\n":
                continue

            if "INPUT" in line:
                IN.append(line[:-1])    # [:-1] to remove newline (\n)

            elif "OUTPUT" in line:
                OUT.append(line[:-1])

            else: # potentially INTERAL node
                ETC.append(line[:-1])

        for x in IN:
            sortedBenchFile.append(x)

        for x in OUT:
            sortedBenchFile.append(x)

        for x in ETC:
            sortedBenchFile.append(x)

        return sortedBenchFile  

    # parseParen: get the data inside the parentheses [used for I/O]
    # Return: data inside parentheses
    def __parseParen(self, line):
                                # INPUT(), OUTPUT(), e = AND(a', b, c)
        p1 = line.index("(")    # index parentheses 1
        p2 = line.index(")")    # index parentheses 2

        return line[p1+1:p2]    # returns data inside parentheses

    # parseInternal: parse internal nodes
    # Return: output internal node info: name, gate, inputs, operation
    def __parseInternal(self, line):
                                    # e = AND(a', b, c) [example]
        line = line.replace(" ", "")
        idx = line.index("=")

        node = line[:idx]           # e

        op = line[idx+1:].strip("\n")   # AND(a', b, c)

        inputs = self.__parseParen(op)     # a', b, c

        idx = op.index("(")         # index operation for AND

        gate = op[:idx]             # AND

        return node, gate, inputs, op

    # processBenchFile: go through the provided benchFile and update the NodeList according to the given information
    def __processBenchFile(self, benchFile):
        for line in benchFile:

            if "INPUT" in line:
                node = self.__parseParen(line)
                self.nodes[node] = Node(node, "INPUT", c0="1", c1="1")

            elif "OUTPUT" in line:
                node = self.__parseParen(line)
                self.nodes[node] = Node(node, "OUTPUT")
            
            else:   # internal
                result = self.__parseInternal(line)
                node = result[0]
                gate = result[1]
                inputs = result[2]
                opr = result[3]

                # add x-x format to each input of a gate
                inputList = inputs.split(",")
                inputs = ""

                for ip in inputList:
                    inputs += f"{node}-{ip},"
                    
                inputs = inputs[:-1]

                if node in self.nodes:    # node previously assigned as OUTPUT
                    self.nodes[node].gate = gate
                    self.nodes[node].ip = inputs
                    self.nodes[node].opr = opr
                else:                   # node not established in NodeList so make new node and mark as INTERNAL
                    self.nodes[node] = Node(node, "INTERNAL", gate, inputs, opr)

    def __processWire(self):
        # wire = x-x format (e.g. A = NAND(b,c) -> wire = A-b & A-c)
        copyOfNodeList = deepcopy(self.nodes)
        
        for name, node in copyOfNodeList.items():   # name = name of node "str", node = Node object
            if node.pos == "INTERNAL" or node.pos == "OUTPUT":
                inputs = self.__parseParen(node.opr).split(",")
                
                for ip in inputs:
                    self.nodes[f'{node.name}-{ip}'] = Node(f'{node.name}-{ip}', "WIRE", ip=ip) 

    # User Input

    # __twoscomp: 2's Complement [return binary (string)]    (string -> string)
    # Input: s = binary (string)
    # Return: 2's complement binary (string)
    def __twoscomp(self, s):
        for j in reversed(range(len(s))):
            if s[j] == '1':
                break

        t = ""
        for i in range(0, j, 1):        # flip everything
            t += str(1-int(s[i]))

        for i in range(j, len(s), 1):   # until the first 1 from the right
            t += s[i]

        return t                        # return 2's complement binary (string)
        
    # __itosbin: convert integer (int) to signed binary (string)
    # Input: i = integer (int) | n = # of bits of desired binary
    # Return: returns signed binary (string)
    def __itosbin(self, i, n):
        s = ""

        i = int(i)

        if i >= 0:
            s = bin(i)[2:].zfill(n)
        else:
            s = bin(0-i)[2:].zfill(n)
            s = self.__twoscomp(s)

        return s

    # twoscomp_dec: 2's Complement [return decimal (int)]     [use for sign extend]
    # Input: b = binary (string)
    # Return: 2's complement decimal (int)
    def __twoscomp_dec(self, b):

        l = len(b)          # length of bit provided

        x = b[:1].zfill(l)  # save the first bit and fill with 0's until original length
        x = x[::-1]         # flip binary

        x = int(x, 2) * -1  # value of binary (unsigned: 10000..0) * -1

        y = int(b[1:], 2)   # value of binary without the first bit

        x += y              # add up differing values

        return x            # return 2's complement decimal (int)

    # __bin_to_dec: convert binary (string) to decimal (int)  [use for sign extend]
    # Input: binary (string)
    # Return: Decimal (int)
    def __bin_to_dec(self, b):
        if(b[0]=="0"):
            return int(b, base=2)
        else:        
            return self.__twoscomp_dec(b)

    # __binaryCheck: checks to make sure userInput is a binary string
    # Return: True if binary string | False if not binary string
    def __binaryCheck(self, userInput):
        for char in userInput:
            if char != "0" and char != "1":
                return False
            
        return True

    # __binaryCheck_U: checks to make sure that user's input is binary (0 or 1) and/or has unknown values (u)
    # Return: True if binary and/or contains unknowns | False if not a binary/unknown input 
    def __binaryCheck_U(self, userInput):
        for char in userInput:
            if char != "0" and char != "1" and char != "u" and char != "U":
                return False
            
        return True

    # __partialInput: if user inputs a partial input then make the rest of the input unknowns (u)
    # Return: user's input with appended unknown values (u)
    def __partialInput(self, userInput, inputCount):
        for i in range(inputCount - len(userInput)):
            userInput += "u"
            
        return userInput 

    # __checkUserInput: checks to make sure that user inputs a valid input
    # Return: True if user input is valid | False if user input is invalid | userInput (string)
    def __checkUserInput(self, userInput, inputCount):
        print(f'Your input TV: {userInput}')

        # user's input is a TV that is less than the total amount of inputs of circuit c and is binary (0 or 1) and/or contains unknowns (u)
        if len(userInput) < inputCount and self.__binaryCheck(userInput) == True or self.__binaryCheck_U(userInput) == True:    
            userInput = self.__partialInput(userInput, inputCount)
            print(f'Updated input TV: {userInput}')
            return True, userInput

        # user's input is a TV that is a number that is less than the number of inputs then convert to binary string
        elif userInput.replace("-", "").isnumeric() == True:
            if len(userInput) < inputCount:
                userInput = self.__itosbin(userInput, inputCount)
                print(f'Updated TV: {userInput}')
                
                return True, userInput

        # user's input is less than the total number of inputs of circuit c and invalid 
        elif (len(userInput) < inputCount and self.__binaryCheck_U(userInput)) == True:
            print(f'Invalid: {userInput}\n(enter only valid characters: 0, 1, u, or i)')
            return False, userInput

        # user's input is greater than the total numbe rof inputs of circuit c 
        elif len(userInput) > inputCount:
            print(f'Invalid: {userInput}\n(user input is too long)')
            return False, userInput      

        # if passed all filters of valid and invalid then assume false
        else:
            return False, userInput

    # __updateNodeListUserTV: updates NodeList "OUTPUT" with inputted user TV
    def __updateNodeListUserTV(self, userInput, inputTV):
        # update NodeList from initial inputs
        for i in range(len(inputTV)):
            if userInput[i] == "1":
                self.nodes[inputTV[i]].value = userInput[i] + "/1"
            elif userInput[i] == "0":
                self.nodes[inputTV[i]].value = userInput[i] + "/0"
            else:
                self.nodes[inputTV[i]].value = "u/u"

    def __inputUserTV(self, inputCount, inputTV):
        # ask user for test vector (e.g. 111, 01u, 1u, uuu)    
        userInput = input(f"\nEnter TV values for TV (e.g. 1001 (bin) or 5 (int))> ")
        userInput = userInput.replace(" ", "")
        valid = False

        # check user input and make sure user's input is valid
        while valid == False:
            check = self.__checkUserInput(userInput, inputCount)
            if check[0] == True:
                userInput = check[1]    # check[1] = userInput 
                valid = True
            else:
                valid = False
                userInput = input(f"\nEnter input values for TV (e.g. 1001 (bin) or 5 (int))> ")

        self.inputTV = userInput

        # update NodeList with new user inputted TV
        self.__updateNodeListUserTV(userInput, inputTV)    

    def __LFSR_userAmount(self):
        '''
        LFSR (psuedo-random)
        h = 1000....

        e.g. h=100
            q0(t+1) = q3(t)
            q1(t+1) = q0(t) ^ q3(t)
            q2(t+1) = q1(t)
            q3(t+1) = q2(t)
        '''

        TV = []
        startingTV = ""

        for i in range(self.numInputs):      # starting TV = 1111....
            startingTV += "1"

        binStr = startingTV

        self.LFSRIter = input("Number of INPUT nodes exceeds 10 so enter the amount of iterations\n > ")

        while self.LFSRIter.isdecimal() != True:
            print("\nPlease enter an integer")
            self.LFSRIter = input("Number of INPUT nodes exceeds 10 so enter the amount of iterations\n > ")

        for i in range(int(self.LFSRIter)):
            newBinStr = ""

            # rolling binary string
            lastBit = binStr[len(binStr)-1]  # get the last bit
            binNum = int(binStr,base=2)
            binNum = binNum >> 1   # bit shift right
            newBinStr += lastBit + self.__itosbin(binNum, len(binStr)-1)
            binStr = newBinStr
            
            qN = binStr[len(binStr)-1]
            if self.userTap == "a":
                # append xor'd value q1 to rolled binary string [tap=1]
                q0 = binStr[0]
                q0xorqN = str(int(q0) ^ int(qN))    
                binStr = binStr[:1] + q0xorqN + binStr[2:]

            elif self.userTap == "b":
                # tap = 1 3 5
                q1_result = str(int(binStr[0:1]) ^ int(qN)) 
                q3_result = str(int(binStr[2:3]) ^ int(qN)) 
                q5_result = str(int(binStr[4:5]) ^ int(qN)) 
                binStr = binStr[:2] + q1_result + binStr[3:4] + q3_result + binStr[5:6] + q5_result + binStr[7:]
                
            elif self.userTap == "c":
                # tap = 2 4 6
                q2_result = str(int(binStr[1:2]) ^ int(qN)) 
                q4_result = str(int(binStr[3:4]) ^ int(qN)) 
                q6_result = str(int(binStr[5:6]) ^ int(qN)) 
                binStr = binStr[:2] + q2_result + binStr[3:4] + q4_result + binStr[5:6] + q6_result + binStr[7:]

            elif self.userTap == "d":
                # tap = 6 7 8
                q6_result = str(int(binStr[5:6]) ^ int(qN))
                q7_result = str(int(binStr[6:7]) ^ int(qN))
                q8_result = str(int(binStr[7:8]) ^ int(qN))
                binStr = binStr[:6] + q6_result + q7_result + q8_result + binStr[9:]

            if binStr != startingTV:
                TV.append(binStr)   

        return TV        

    # Return: return the exhausted TVs
    def __exhaustInputs(self):
        TV = []
        startingTV = ""
        for i in range(self.numInputs):
            startingTV += "0"

        binStr = startingTV
        TV.append(startingTV)

        for i in range(2**self.numInputs-1):
            binInt = self.__bin_to_dec(binStr) + 1
            binStr = self.__itosbin(binInt, self.numInputs)
            TV.append(binStr)

        return TV

    # __randomizeTV: create random test vector based on the # of inputs in circuit c
    # Return: return randomized test vector 
    def __randomizeTV(self, inputCount):
        TV = ""
        for i in range(inputCount):
            TV += str(random.randint(0,1))
            
        return str(TV)

    # __random1000TV: truly generates 1000 random TV, non-repeating 
    # Return: return all 1000 generated TVs
    def __random1000TV(self):
        setTV = set()
        TV = []

        while len(setTV) != 1000:
            curTV = ""
            for i in range(self.numInputs):      # starting TV = 1111....
                curTV += str(random.randint(0,1))     

            setTV.add(curTV)

        for tv in setTV:
            TV.append(tv)

        return TV

    def __checkUserFault(self, fault):
        check = False

        while check == False:
            if fault.count("-") == 1:
                fault = fault.split("-")
                self.faultList[(f"{fault[0]}-{fault[1]}")] = Fault(f"{fault[0]}-{fault[1]}")
                return True
            
            elif fault.count("-") == 2:
                fault = fault.split("-")
                self.faultList[(f"{fault[0]}-{fault[1]}-{fault[2]}")] = Fault(f"{fault[0]}-{fault[1]}-{fault[2]}")
                return True

            else:
                print("\nInvalid fault")      
                userFault = input("Enter a single fault (e.g. a-1 or d-a-0)> ")

class Gate():
    # operation: operate all gate functions and decide which gate is operating
    def _operation(self, node, inputs, NodeList, op="-", option="-"):
        if op == "NOT":
            self.NOT(node, inputs, NodeList, option)
        elif op == "BUFF":
            self.BUFF(node, inputs, NodeList, option)
        elif op == "AND":
            self.AND(node, inputs, NodeList, option)
        elif op == "NAND":
            self.NAND(node, inputs, NodeList, option)        
        elif op == "OR":
            self.OR(node, inputs, NodeList, option)
        elif op == "NOR":
            self.NOR(node, inputs, NodeList, option)    
        elif op == "XOR":
            self.XOR(node, inputs, NodeList, option) 
        elif op == "XNOR":
            self.XNOR(node, inputs, NodeList, option)
        # elif op == "-": # c7552.bench -> node 241 is input and directly as output
            # self.c7552_case(node, NodeList)
        elif op == "WIRE" and option != "c":
            self._convertWire(node, inputs, NodeList)
        else:
            print(f">{op}< NOT IMPLEMENTED")

    def _convertWire(self, node, inputs, NodeList):
        v0, v1 = "", ""

        result = NodeList[inputs[0]].value    # e.g. y-i = i
        v0 = result[0]
        v1 = result[2]

        check = self.__checkFaultInput(node, inputs, NodeList, v1)
        check = self.__checkFaultOutput(node, inputs, NodeList, v1)
        v1, faultFound = check[0], check[1]

        NodeList[node].value = f"{v0}/{v1}"

        self.__updaten0n1(node, NodeList)

    # convertInputs: converts inputs based on node name to given value of control or normal
    # Return: returns converted inputs (normal or control, SCOAP)
    def _convertInputs(self, inputs, NodeList, option="-"):
        # extract inputs from NodeList
        cnvtInputs      = []   # hold converted inputs from NodeList
        cnvtInputsC0    = []   # hold c0 values from inputs
        cnvtInputsC1    = []   # hold c1 values from inputs
        controlInputs   = []   # controlled inputs, remove wire notation
        
        if option == "c":
            for ip in inputs:
                ip = ip.split("-")
                controlInputs.append(ip[1])

            # if option == "c":   # control
            for ip in controlInputs:
                cnvtInputsC0.append(NodeList[ip].c0)
                cnvtInputsC1.append(NodeList[ip].c1) 
        else:               
            for ip in inputs:
                if NodeList[ip].pos == "WIRE":
                    inputList = ip.split("-")
                    curIP = inputList[1]                
                    cnvtInputs.append(NodeList[curIP].value)                
                else:
                    cnvtInputs.append(NodeList[ip].value)
        
        if option == "c":
            return cnvtInputsC0, cnvtInputsC1
        else:
            return cnvtInputs

    # str2int: converts a string to an int
    # Return: returns the input
    def _str2int(self, inputs):
        ip = []

        for i in inputs:
            ip.append(int(i))

        return ip
    
    def __splitInputs(self, inputs):
        ip0, ip1 = [], []

        for ip in inputs:
            i = ip.split("/")
            ip0.append(i[0])
            ip1.append(i[1])

        return ip0, ip1

    def __checkFaultInput(self, node, originalInputs, NodeList, v1):
        faultFound = False

        # check faults in inputs (wires)
        for ip in originalInputs:
            if NodeList[ip].fault == True:
                v1 = NodeList[ip].sa_fault
                faultFound = True

        # # if output node is a wire
        # if NodeList[node].pos == "WIRE":
        #     if NodeList[node].fault == True:
        #         v1 = NodeList[node].sa_fault
        #         faultFound = True

        return v1, faultFound

    def __checkFaultOutput(self, node, originalInputs, NodeList, v1):
        faultFound = False

        # check fault for output
        if NodeList[node].fault == True:
            v1 = NodeList[node].sa_fault
            faultFound = True

        return v1, faultFound        

    def __updaten0n1(self, node, NodeList):
        if NodeList[node].value == "0/0":
            NodeList[node].n0 += 1
        elif NodeList[node].value == "1/1":
            NodeList[node].n1 += 1
        else:
            pass # unknown case      

    # ----------------------------------------------------------------------------------------

    # NOT: not gate operation given inputs (list) and node (output)
    def NOT(self, node, inputs, NodeList, option="-"):
        if option == "c":   # control
            ipc0 = NodeList[inputs[0].split("-")[1]].c0   # c0(node)
            ipc1 = NodeList[inputs[0].split("-")[1]].c1   # c1(node)

            # flip c0 and c1 values for output node and +1
            NodeList[node].c0 = str(int(ipc1) + 1)
            NodeList[node].c1 = str(int(ipc0) + 1)   

        else:   # normal
            v0, v1, faultFound = "", "", ""

            result = NodeList[inputs[0]].value.split("/")
            ip0, ip1 = result[0], result[1] 

            if ip0 == "u":
                v0 = "u"
            elif ip0 == "0":
                v0 = "1"  # update output node with "NOT'd" value
            else:
                v0 = "0"

            check = self.__checkFaultInput(node, inputs, NodeList, v1)
            v1, faultFound = check[0], check[1]

            if faultFound == False: # base on original input
                if ip1 == "u":
                    v1 = "u"
                elif ip1 == "0":
                    v1 = "1"  # update output node with "NOT'd" value
                else:
                    v1 = "0"       
            else: # base on fault
                if v1 == "u":
                    v1 = "u"
                elif v1 == "0":
                    v1 = "1"  # update output node with "NOT'd" value
                else:
                    v1 = "0"                        

            check = self.__checkFaultOutput(node, inputs, NodeList, v1)
            v1, faultFound = check[0], check[1]

            NodeList[node].value = f"{v0}/{v1}"

            self.__updaten0n1(node, NodeList)
    
    # ----------------------------------------------------------------------------------------       

    # BUFF: buff operation given inputs (list) and node (output)
    def BUFF(self, node, inputs, NodeList, option="-"):
        if option == "c":   # control
            ipc0 = NodeList[inputs[0]].c0   # c0(node)
            ipc1 = NodeList[inputs[0]].c1   # c1(node)

            # flip c0 and c1 values for output node
            NodeList[node].c0 = str(int(ipc0) + 1)
            NodeList[node].c1 = str(int(ipc1) + 1)            
        
        else:   # normal
            v0, v1, result = "", "", ""
            
            result = NodeList[inputs[0]].value.split("/")
            v0, v1 = result[0], result[1] 

            check = self.__checkFaultInput(node, inputs, NodeList, v1)
            check = self.__checkFaultOutput(node, inputs, NodeList, v1)
            v1, faultFound = check[0], check[1]      

            NodeList[node].value = f"{v0}/{v1}"

            self.__updaten0n1(node, NodeList)

    # ----------------------------------------------------------------------------------------

    # AND: AND gate operation given inputs (list) and node (output) | update NodeList [option: c -> control, otherwise -> normal]
    def AND(self, node, inputs, NodeList, option="-"):
        # extract inputs from NodeList

        if option == "c":   # control
            cnvtIp = self._convertInputs(inputs, NodeList, "c")
            cnvtInputsC0 = cnvtIp[0]
            cnvtInputsC1 = cnvtIp[1]
            result = self._AND_control(cnvtInputsC0, cnvtInputsC1)
            NodeList[node].c0 = result[0]
            NodeList[node].c1 = result[1]
        else:   # normal
            cnvtIp = self._convertInputs(inputs, NodeList)
            result = self._AND(cnvtIp, node, inputs, NodeList)
            NodeList[node].value = result
            
            self.__updaten0n1(node, NodeList)
        
    def _AND(self, inputs, node, originalInputs, NodeList):
        v0, v1 = "", ""
        ip0, ip1 = self.__splitInputs(inputs)

        if "0" in ip0:   # controlling value of AND gate
            v0 = "0"
        elif "u" in ip0: # unknown found after checking for "0" so only "1" and "u" exist
            v0 = "u"
        else:
            v0 = "1"      # no "u" or "0" so only "1" exists

        check = self.__checkFaultInput(node, originalInputs, NodeList, v1)
        v1, faultFound = check[0], check[1]

        if faultFound == False: # base on original
            if "0" in ip1:   # controlling value of AND gate
                v1 = "0"
            elif "u" in ip1: # unknown found after checking for "0" so only "1" and "u" exist
                v1 = "u"
            else:
                v1 = "1"      # no "u" or "0" so only "1" exists
        else:   # base on fault
            if v1 == "0":   # controlling value of AND gate
                v1 = "0"
            elif v1 == "u": # unknown found after checking for "0" so only "1" and "u" exist
                v1 = "u"
            else:
                v1 = "1"      # no "u" or "0" so only "1" exists            

        check = self.__checkFaultOutput(node, inputs, NodeList, v1)
        v1, faultFound = check[0], check[1]

        return f"{v0}/{v1}"
  
    # _AND_control: helper function to AND() producing control outputs of an AND gate
    # Return: returns new c0,c1 values
    def _AND_control(self, cnvtInputsC0, cnvtInputsC1):
        # access c0(x), c1(x), c0(y), c1(y) through NodeList

        # AND Gate: easy to control an output of 0 with input controlling input 0
        c0 = str(min(self._str2int(cnvtInputsC0)) + 1)
        c1 = str(sum(self._str2int(cnvtInputsC1)) + 1)

        return c0, c1

    # ----------------------------------------------------------------------------------------
    
    # NAND: NAND gate operation given inputs (list) and node (output) [option: c -> control, otherwise -> normal]
    def NAND(self, node, inputs, NodeList, option="-"):
        # extract inputs from NodeList

        if option == "c":   # control
            cnvtIp = self._convertInputs(inputs, NodeList, "c")
            cnvtInputsC0 = cnvtIp[0]
            cnvtInputsC1 = cnvtIp[1]
            result = self._NAND_control(cnvtInputsC0, cnvtInputsC1)
            NodeList[node].c0 = result[0]
            NodeList[node].c1 = result[1]

        else:   # normal
            cnvtIp = self._convertInputs(inputs, NodeList)
            result = self._NAND(cnvtIp, node, inputs, NodeList)
            NodeList[node].value = result

            self.__updaten0n1(node, NodeList)

    # _NAND: helper function to NAND() producing normal NAND operation outputs
    # Return: returns output of NAND operation
    def _NAND(self, inputs, node, originalInputs, NodeList):
        v0, v1 = "", ""
        ip0, ip1 = self.__splitInputs(inputs)

        # check to see if there occurs a controlling bit [controlling bit irrespective of other inputs]
        if "0" in ip0:   # controlling value of an NAND gate found -> "0"
            v0 = "1"
        elif "u" in ip0: 
            v0 = "u"
        else:
            v0 = "0"

        check = self.__checkFaultInput(node, originalInputs, NodeList, v1)
        v1, faultFound = check[0], check[1]

        if faultFound == False: # vfault not found so base on original input
            if "0" in ip1:   # controlling value of an NAND gate found -> "0"
                v1 = "1"
            elif "u" in ip1: 
                v1 = "u"
            else:
                v1 = "0"
        else:   # fault found so base on v1
            if v1 == "0":   # controlling value of an NAND gate found -> "0"
                v1 = "1"
            elif v1 == "u": 
                v1 = "u"
            else:
                v1 = "0"

        check = self.__checkFaultOutput(node, inputs, NodeList, v1)
        v1, faultFound = check[0], check[1]

        return f"{v0}/{v1}"        

    # _NAND_control: helper function to NAND() producing control outputs of an NAND gate
    # Return: returns new c0,c1 values
    def _NAND_control(self, cnvtInputsC0, cnvtInputsC1):
        # access c0(x), c1(x), c0(y), c1(y) through NodeList

        # NAND Gate: easy to control an output of 1 with input controlling input 0
        c0 = str(sum(self._str2int(cnvtInputsC1)) + 1)
        c1 = str(min(self._str2int(cnvtInputsC0)) + 1)

        return c0, c1

    # ----------------------------------------------------------------------------------------

    # OR: OR gate operation given inputs (list) and node (output) | update NodeList [option: c -> control, otherwise -> normal]
    def OR(self, node, inputs, NodeList, option="-"):
        # extract inputs from NodeList

        if option == "c":
            cnvtIp = self._convertInputs(inputs, NodeList, "c")
            cnvtInputsC0 = cnvtIp[0]
            cnvtInputsC1 = cnvtIp[1]
            result = self._OR_control(cnvtInputsC0, cnvtInputsC1)
            NodeList[node].c0 = result[0]
            NodeList[node].c1 = result[1]            
        else:
            cnvtIp = self._convertInputs(inputs, NodeList)
            result = self._OR(cnvtIp, node, inputs, NodeList)
            NodeList[node].value = result

            self.__updaten0n1(node, NodeList)      

    # _OR: helper function to OR() producing normal OR operation outputs
    # Return: returns output of OR operation
    def _OR(self, inputs, node, originalInputs, NodeList):
        v0, v1 = "", ""
        ip0, ip1 = self.__splitInputs(inputs)

        # check to see if there occurs a controlling bit [controlling bit irrespective of other inputs]
        if "1" in ip0:   # controlling value of an NOR gate found -> "1"
            v0 = "1"
        elif "u" in ip0:
            v0 = "u"
        else:
            v0 = "0"

        check = self.__checkFaultInput(node, originalInputs, NodeList, v1)
        v1, faultFound = check[0], check[1]

        if faultFound == False: # base on original
            if "1" in ip1:   # controlling value of an NOR gate found -> "1"
                v1 = "1"
            elif "u" in ip1:
                v1 = "u"
            else:
                v1 = "0"
        else:   # base on fault
            if v1 == "0":   # controlling value of AND gate
                v1 = "0"
            elif v1 == "u": # unknown found after checking for "0" so only "1" and "u" exist
                v1 = "u"
            else:
                v1 = "1"      # no "u" or "0" so only "1" exists            
            
        check = self.__checkFaultOutput(node, inputs, NodeList, v1)
        v1, faultFound = check[0], check[1]

        return f"{v0}/{v1}"        

    # _OR_control: helper function to OR() producing control outputs of an OR gate
    # Return: returns new c0,c1 values
    def _OR_control(self, cnvtInputsC0, cnvtInputsC1):
        # access c0(x), c1(x), c0(y), c1(y) through NodeList

        # OR Gate: easy to control an output of 1 with input controlling input 1
        c0 = str(sum(self._str2int(cnvtInputsC0)) + 1)
        c1 = str(min(self._str2int(cnvtInputsC1)) + 1)

        return c0, c1

    # ----------------------------------------------------------------------------------------

    # NOR: NOR gate operation given inputs (list) and node (output) | update NodeList [option: c -> control, otherwise -> normal]
    def NOR(self, node, inputs, NodeList, option="-"):
        # extract inputs from NodeList

        if option == "c":   # control
            cnvtIp = self._convertInputs(inputs, NodeList, "c")
            cnvtInputsC0 = cnvtIp[0]
            cnvtInputsC1 = cnvtIp[1]
            result = self._NOR_control(cnvtInputsC0, cnvtInputsC1)
            NodeList[node].c0 = result[0]
            NodeList[node].c1 = result[1]        
        else:               # normal
            cnvtIp = self._convertInputs(inputs, NodeList)
            result = self._NOR(cnvtIp, node, inputs, NodeList)
            NodeList[node].value = result

            self.__updaten0n1(node, NodeList)            

    # _NOR: helper function to NOR() producing normal NOR operation outputs
    # Return: returns output of NOR operation
    def _NOR(self, inputs, node, originalInputs, NodeList):
        v0, v1 = "", ""
        ip0, ip1 = self.__splitInputs(inputs)

        # check to see if there occurs a controlling bit [controlling bit irrespective of other inputs]
        if "1" in ip0:   # controlling value of an NOR gate found -> "1"
            v0 = "0"
        elif "u" in ip0:
            v0 = "u"
        else:
            v0 = "1"

        check = self.__checkFaultInput(node, originalInputs, NodeList, v1)
        v1, faultFound = check[0], check[1]

        if faultFound == False: # base on original
            if "1" in ip1:   # controlling value of an NOR gate found -> "1"
                v1 = "0"
            elif "u" in ip1:
                v1 = "u"
            else:
                v1 = "1"
        else:   # base onfault
            if v1 == "0":   # controlling value of AND gate
                v1 = "0"
            elif v1 == "u": # unknown found after checking for "0" so only "1" and "u" exist
                v1 = "u"
            else:
                v1 = "1"      # no "u" or "0" so only "1" exists                            

        check = self.__checkFaultOutput(node, inputs, NodeList, v1)
        v1, faultFound = check[0], check[1]

        return f"{v0}/{v1}"        

    # _NOR_control: helper function to NOR() producing control outputs of an NOR gate
    # Return: returns new c0,c1 values
    def _NOR_control(self, cnvtInputsC0, cnvtInputsC1):
        # access c0(x), c1(x), c0(y), c1(y) through NodeList

        # OR Gate: easy to control an output of 1 with input controlling input 1
        c0 = str(min(self._str2int(cnvtInputsC1)) + 1)
        c1 = str(sum(self._str2int(cnvtInputsC0)) + 1)

        return c0, c1

    # ----------------------------------------------------------------------------------------

    # XOR: XOR gate operation given inputs (list) and node (output) | update NodeList [option: c -> control, otherwise -> normal]
    def XOR(self, node, inputs, NodeList, option="-"):
        # extract inputs from NodeList

        if option == "c":   # control
            cnvtIp = self._convertInputs(inputs, NodeList, "c")
            result = self._XOR_control(inputs, NodeList)
            NodeList[node].c0 = result[0]
            NodeList[node].c1 = result[1]
        else:               # normal        
            cnvtIp = self._convertInputs(inputs, NodeList)
            result = self._XOR(cnvtIp, node, inputs, NodeList)
            NodeList[node].value = result        

            self.__updaten0n1(node, NodeList)                  

    # _XOR: helper function to XOR() producing normal XOR operation outputs
    # Return: returns output of XOR operation
    def _XOR(self, inputs, node, originalInputs, NodeList):
        v0, v1 = "", ""
        ip0, ip1 = self.__splitInputs(inputs)

        # XOR is 1 when there are an odd number of 1's as input
        if "u" in ip0:
            v0 = "u"
        elif ip0.count("1") % 2 != 0:    # count of "1" inputs is odd
            v0 = "1"
        else:
            v0 = "0" 

        check = self.__checkFaultInput(node, originalInputs, NodeList, v1)
        v1, faultFound = check[0], check[1]

        if faultFound == False: # base on original
            if "u" in ip1:
                v1 = "u"
            elif ip1.count("1") % 2 != 0:    # count of "1" inputs is odd
                v1 = "1"
            else:
                v1 = "0"      
        else: # base on fault   
            z = v1.count("1") % 2         
            if v1 == "u":
                v1 = "u"
            elif v1 == "0":    # count of "1" inputs is odd
                v1 = "1"
            else:
                v1 = "0"    

        check = self.__checkFaultOutput(node, inputs, NodeList, v1)
        v1, faultFound = check[0], check[1]

        return f"{v0}/{v1}"        

    # _XOR_control: helper function to XOR() producing control outputs of an XOR gate
    # Return: returns new c0,c1 values
    def _XOR_control(self, inputs, NodeList):
        # access c0(x), c1(x), c0(y), c1(y) through NodeList
        '''
            XOR(a,b)

            c=0 -> a=b -> (a=0 & b=0) v (a=1 & b=1)
            (a=0 & b=0) -> sum(c0(a), c0(b)) + 1
            (a=1 & b=1) -> sum(c1(a), c1(b)) + 1
            (a=0 & b=0) v (a=1 & b=1) = min((a=0 & b=0), (a=1 & b=1))

            c=1 -> a != b -> (a=0 & b=1) v (a=1 & b=0)
            (a=0 & b=1) = sum(c0(a), c1(b)) + 1
            (a=1 & b=0) = sum(c1(a), c0(b)) + 1
            (a=0 & b=1) v (a=1 & b=0) = min((a=0 & b=1), (a=1 & b=0))
        '''
        
        # currently 2 input so input = ["a", "b"]
        a = inputs[0].split("-")[1]
        b = inputs[1].split("-")[1]

        c0_a = int(NodeList[a].c0)
        c1_a = int(NodeList[a].c1)
        c0_b = int(NodeList[b].c0)
        c1_b = int(NodeList[b].c1)

        c00 = c0_a + c0_b + 1
        c11 = c1_a + c1_b + 1
        c0 = str(min(c00, c11))

        c01 = c0_a + c1_b + 1
        c10 = c1_a + c0_b + 1
        c1 = str(min(c01, c10))

        return c0, c1

    # ----------------------------------------------------------------------------------------

    # XNOR: XNOR gate operation given inputs (list) and node (output) | update NodeList [option: c -> control, otherwise -> normal]
    def XNOR(self, node, inputs, NodeList, option="-"):
        # extract inputs from NodeList

        if option == "c":   # control
            cnvtIp = self._convertInputs(inputs, NodeList, "c")
            result = self._XNOR_control(inputs, NodeList)
            NodeList[node].c0 = result[0]
            NodeList[node].c1 = result[1]
        else:               # normal        
            cnvtIp = self._convertInputs(inputs, NodeList)
            result = self._XNOR(cnvtIp, node, inputs, NodeList)
            NodeList[node].value = result        

            self.__updaten0n1(node, NodeList)             

    # _XNOR: helper function to XNOR() producing normal XNOR operation outputs
    # Return: returns output of XNOR operation
    def _XNOR(self, inputs, node, originalInputs, NodeList):
        v0, v1 = "", ""
        ip0, ip1 = self.__splitInputs(inputs)

        # XNOR is 0 when there are an odd number of 1's as input
        if "u" in ip0:
            v0 = "u"
        elif ip0.count("1") % 2 != 0:    # count of "1" inputs is odd
            v0 = "0"
        else:
            v0 = "1"

        check = self.__checkFaultInput(node, originalInputs, NodeList, v1)
        v1, faultFound = check[0], check[1]

        if faultFound == False: # base on original
            if "u" in ip1:
                v1 = "u"
            elif ip1.count("1") % 2 != 0:    # count of "1" inputs is odd
                v1 = "0"
            else:
                v1 = "1"
        else:   # base on fault
            if v1 == "u":
                v1 = "u"
            elif v1 == "1":    # count of "1" inputs is odd
                v1 = "0"
            else:
                v1 = "1"
        
        check = self.__checkFaultOutput(node, inputs, NodeList, v1)
        v1, faultFound = check[0], check[1]

        return f"{v0}/{v1}"

    # _XNOR_control: helper function to XNOR() producing control outputs of an XNOR gate
    # Return: returns new c0,c1 values
    def _XNOR_control(self, inputs, NodeList):
        # access c0(x), c1(x), c0(y), c1(y) through NodeList
        '''
            XNOR(a,b)

            c=0 -> a != b -> (a=0 & b=1) v (a=1 & b=0)
            (a=0 & b=1) = sum(c0(a), c1(b)) + 1
            (a=1 & b=0) = sum(c1(a), c0(b)) + 1
            (a=0 & b=1) v (a=1 & b=0) = min((a=0 & b=1), (a=1 & b=0))

            c=1 -> a=b -> (a=0 & b=0) v (a=1 & b=1)
            (a=0 & b=0) -> sum(c0(a), c0(b)) + 1
            (a=1 & b=1) -> sum(c1(a), c1(b)) + 1
            (a=0 & b=0) v (a=1 & b=1) = min((a=0 & b=0), (a=1 & b=1))
        '''
        
        # currently 2 input so input = ["a", "b"]
        a = inputs[0].split("-")[1]
        b = inputs[1].split("-")[1]

        c0_a = int(NodeList[a].c0)
        c1_a = int(NodeList[a].c1)
        c0_b = int(NodeList[b].c0)
        c1_b = int(NodeList[b].c1)

        c01 = c0_a + c1_b + 1
        c10 = c1_a + c0_b + 1
        c0 = str(min(c01, c10))

        c00 = c0_a + c0_b + 1
        c11 = c1_a + c1_b + 1
        c1 = str(min(c00, c11))

        return c0, c1        

    # ----------------------------------------------------------------------------------------

# node class e.g. Given Y = NAND(A,B) -> Y, Y-A, Y-B
# Nodes: input/output and wires in between
class Node():
    def __init__(self, name: str="-", pos: str="-", gate: str="-", ip: str="-", opr: str="-", value: str="-", level: int=0, wire: str="-", fault: bool=False, sa_fault: str="-" ,n0: int=0, n1: int=0, c0: str="-", c1: str="-"):
        self.name       = name      
        self.pos        = pos       
        self.gate       = gate      
        self.ip         = ip        # input
        self.opr        = opr       # operation
        self.value      = value     # value/output
       
        self.level      = level
        self.wire       = wire      # T/F
        self.fault      = fault     # T/F
        self.sa_fault   = sa_fault  # value of the fault
        self.n0         = n0
        self.n1         = n1
        self.c0         = c0
        self.c1         = c1
    
    def info(self):
        print(f'\nname\t = {self.name}')
        print(f'pos\t = {self.pos}')
        print(f'gate\t = {self.gate}')
        print(f'ip\t = {self.ip}')
        print(f'opr\t = {self.opr}')
        print(f'value\t = {self.value}')
        print(f'level\t = {self.level}')
        print(f'counter\t = {self.counter}')
        print(f'fault\t = {self.fault}')
        print(f'sa_fault\t = {self.sa_fault}')
        print(f'c0\t = {self.c0}')
        print(f'c1\t = {self.c1}')
        print(f'n0\t = {self.n0}')
        print(f'n1\t = {self.n1}')

class Fault():
    def __init__(self, name, detected: int=0):
        self.name = name
        self.detected = detected  # num of times fault was detected
