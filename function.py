# Jim Palomo
# ECE 464 | All Project Combined
# Combination of all ECE 464 Projects
# Normal Circuit Simulation | Fault Simulation | Controllability | PRPG Analysis on c432.bench

import pickle
import logging as log

from classes import NodeList

def averageDetectionData():
    input_file = open(f"data.csv", "r")
    output_file = open(f"result_avgDetection.csv", "w")
    l0,l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11,l12,l13,l14,l15,l16,l17 = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]

    next(input_file)
    for line in input_file:
        curLine = line[:-1].split(",")
        numDetected = curLine[1]
        level = curLine[2]

        if level == "0" : l0.append(int(numDetected))
        if level == "1" : l1.append(int(numDetected))
        if level == "2" : l2.append(int(numDetected))
        if level == "3" : l3.append(int(numDetected))
        if level == "4" : l4.append(int(numDetected))
        if level == "5" : l5.append(int(numDetected))
        if level == "6" : l6.append(int(numDetected))
        if level == "7" : l7.append(int(numDetected))
        if level == "8" : l8.append(int(numDetected))
        if level == "8" : l8.append(int(numDetected))
        if level == "9" : l9.append(int(numDetected))
        if level == "10": l10.append(int(numDetected))
        if level == "11": l11.append(int(numDetected))
        if level == "12": l12.append(int(numDetected))
        if level == "13": l13.append(int(numDetected))
        if level == "14": l14.append(int(numDetected))
        if level == "15": l15.append(int(numDetected))
        if level == "16": l16.append(int(numDetected))
        if level == "17": l17.append(int(numDetected))

    output_file.write("Circuit Level,Average Detection\n")
    output_file.write("0,"  + str(sum(l0)/len(l0))   + "\n")
    output_file.write("1,"  + str(sum(l1)/len(l1))   + "\n")
    output_file.write("2,"  + str(sum(l2)/len(l2))   + "\n")
    output_file.write("3,"  + str(sum(l3)/len(l3))   + "\n")
    output_file.write("4,"  + str(sum(l4)/len(l4))   + "\n")
    output_file.write("5,"  + str(sum(l5)/len(l5))   + "\n")
    output_file.write("6,"  + str(sum(l6)/len(l6))   + "\n")
    output_file.write("7,"  + str(sum(l7)/len(l7))   + "\n")
    output_file.write("8,"  + str(sum(l8)/len(l8))   + "\n")
    output_file.write("9,"  + str(sum(l9)/len(l9))   + "\n")
    output_file.write("10," + str(sum(l10)/len(l10)) + "\n")
    output_file.write("11," + str(sum(l11)/len(l11)) + "\n")
    output_file.write("12," + str(sum(l12)/len(l12)) + "\n")
    output_file.write("13," + str(sum(l13)/len(l13)) + "\n")
    output_file.write("14," + str(sum(l14)/len(l14)) + "\n")
    output_file.write("15," + str(sum(l15)/len(l15)) + "\n")
    output_file.write("16," + str(sum(l16)/len(l16)) + "\n")
    output_file.write("17," + str(sum(l17)/len(l17)) + "\n")

def noneDetectedData():
    input_file = open(f"data.csv", "r")
    output_file = open(f"result_noDetection.csv", "w")
    l0, l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16, l17 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    l0_total, l1_total, l2_total, l3_total, l4_total, l5_total, l6_total, l7_total, l8_total, l9_total, l10_total, l11_total, l12_total, l13_total, l14_total, l15_total, l16_total, l17_total = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    next(input_file)
    for line in input_file:
        curLine = line[:-1].split(",")
        numDetected = curLine[1]
        level = curLine[2]

        if numDetected == "0":
            if level == "0" : l0 += 1
            if level == "1" : l1 += 1
            if level == "2" : l2 += 1
            if level == "3" : l3 += 1
            if level == "4" : l4 += 1
            if level == "5" : l5 += 1
            if level == "6" : l6 += 1
            if level == "7" : l7 += 1
            if level == "8" : l8 += 1
            if level == "8" : l8 += 1
            if level == "9" : l9 += 1
            if level == "10": l10 += 1
            if level == "11": l11 += 1
            if level == "12": l12 += 1
            if level == "13": l13 += 1
            if level == "14": l14 += 1
            if level == "15": l15 += 1
            if level == "16": l16 += 1
            if level == "17": l17 += 1

        if level == "0" : l0_total += 1
        if level == "1" : l1_total += 1
        if level == "2" : l2_total += 1
        if level == "3" : l3_total += 1
        if level == "4" : l4_total += 1
        if level == "5" : l5_total += 1
        if level == "6" : l6_total += 1
        if level == "7" : l7_total += 1
        if level == "8" : l8_total += 1
        if level == "8" : l8_total += 1
        if level == "9" : l9_total += 1
        if level == "10": l10_total += 1
        if level == "11": l11_total += 1
        if level == "12": l12_total += 1
        if level == "13": l13_total += 1
        if level == "14": l14_total += 1
        if level == "15": l15_total += 1
        if level == "16": l16_total += 1
        if level == "17": l17_total += 1            

    output_file.write("Circuit Level,Number of No Detections\n")
    output_file.write("0,"  + str(l0 / l0_total)   + "\n")
    output_file.write("1,"  + str(l1 / l1_total)   + "\n")
    output_file.write("2,"  + str(l2 / l2_total)   + "\n")
    output_file.write("3,"  + str(l3 / l3_total)   + "\n")
    output_file.write("4,"  + str(l4 / l4_total)   + "\n")
    output_file.write("5,"  + str(l5 / l5_total)   + "\n")
    output_file.write("6,"  + str(l6 / l6_total)   + "\n")
    output_file.write("7,"  + str(l7 / l7_total)   + "\n")
    output_file.write("8,"  + str(l8 / l8_total)   + "\n")
    output_file.write("9,"  + str(l9 / l9_total)   + "\n")
    output_file.write("10," + str(l10 / l10_total)  + "\n")
    output_file.write("11," + str(l11 / l11_total)  + "\n")
    output_file.write("12," + str(l12 / l12_total)  + "\n")
    output_file.write("13," + str(l13 / l13_total)  + "\n")
    output_file.write("14," + str(l14 / l14_total)  + "\n")
    output_file.write("15," + str(l15 / l15_total)  + "\n")
    output_file.write("16," + str(l16 / l16_total)  + "\n")
    output_file.write("17," + str(l17 / l17_total)  + "\n")

def maxControlData():
    # Load back in saved resized images
    with open(f'NodeList.pkl', 'rb') as f:
        data = pickle.load(f)
        f.close()    

    output_file = open(f"result_maxControl.csv", "w")

    NodeList = data[0]

    l0_c1, l1_c1, l2_c1, l3_c1, l4_c1, l5_c1, l6_c1, l7_c1, l8_c1, l9_c1, l10_c1, l11_c1, l12_c1, l13_c1, l14_c1, l15_c1, l16_c1, l17_c1 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    l0_c0, l1_c0, l2_c0, l3_c0, l4_c0, l5_c0, l6_c0, l7_c0, l8_c0, l9_c0, l10_c0, l11_c0, l12_c0, l13_c0, l14_c0, l15_c0, l16_c0, l17_c0 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 
    
    for node in NodeList:

        if NodeList[node].level == 0: 
            if int(NodeList[node].c0) > l0_c0:
                l0_c0 = int(NodeList[node].c0)
            
            if int(NodeList[node].c1) > l0_c1:
                l0_c1 = int(NodeList[node].c1)

        if NodeList[node].level == 1: 
            if int(NodeList[node].c0) > l1_c0:
                l0_c0 = int(NodeList[node].c0)
            
            if int(NodeList[node].c1) > l1_c1:
                l1_c1 = int(NodeList[node].c1)

        if NodeList[node].level == 2: 
          if int(NodeList[node].c0) > l2_c0:
              l2_c0 = int(NodeList[node].c0)
          
          if int(NodeList[node].c1) > l2_c1:
              l2_c1 = int(NodeList[node].c1)

        if NodeList[node].level == 3: 
            if int(NodeList[node].c0) > l3_c0:
                l3_c0 = int(NodeList[node].c0)
            
            if int(NodeList[node].c1) > l3_c1:
                l3_c1 = int(NodeList[node].c1)                

        if NodeList[node].level == 4: 
            if int(NodeList[node].c0) > l4_c0:
                l4_c0 = int(NodeList[node].c0)
            
            if int(NodeList[node].c1) > l4_c1:
                l4_c1 = int(NodeList[node].c1)

        if NodeList[node].level == 5: 
            if int(NodeList[node].c0) > l5_c0:
                l5_c0 = int(NodeList[node].c0)
            
            if int(NodeList[node].c1) > l5_c1:
                l5_c1 = int(NodeList[node].c1)

        if NodeList[node].level == 6: 
            if int(NodeList[node].c0) > l6_c0:
                l6_c0 = int(NodeList[node].c0)
            
            if int(NodeList[node].c1) > l6_c1:
                l6_c1 = int(NodeList[node].c1)

        if NodeList[node].level == 7: 
            if int(NodeList[node].c0) > l7_c0:
                l7_c0 = int(NodeList[node].c0)
            
            if int(NodeList[node].c1) > l7_c1:
                l7_c1 = int(NodeList[node].c1)

        if NodeList[node].level == 8: 
            if int(NodeList[node].c0) > l8_c0:
                l8_c0 = int(NodeList[node].c0)
            
            if int(NodeList[node].c1) > l8_c1:
                l8_c1 = int(NodeList[node].c1)

        if NodeList[node].level == 9: 
            if int(NodeList[node].c0) > l9_c0:
                l9_c0 = int(NodeList[node].c0)
            
            if int(NodeList[node].c1) > l9_c1:
                l9_c1 = int(NodeList[node].c1)

        if NodeList[node].level == 10: 
            if int(NodeList[node].c0) > l10_c0:
                l10_c0 = int(NodeList[node].c0)
            
            if int(NodeList[node].c1) > l10_c1:
                l10_c1 = int(NodeList[node].c1)

        if NodeList[node].level == 11: 
            if int(NodeList[node].c0) > l11_c0:
                l11_c0 = int(NodeList[node].c0)
            
            if int(NodeList[node].c1) > l11_c1:
                l11_c1 = int(NodeList[node].c1)

        if NodeList[node].level == 12: 
            if int(NodeList[node].c0) > l12_c0:
                l12_c0 = int(NodeList[node].c0)
            
            if int(NodeList[node].c1) > l12_c1:
                l12_c1 = int(NodeList[node].c1)

        if NodeList[node].level == 13: 
            if int(NodeList[node].c0) > l13_c0:
                l13_c0 = int(NodeList[node].c0)
            
            if int(NodeList[node].c1) > l13_c1:
                l13_c1 = int(NodeList[node].c1)

        if NodeList[node].level == 14: 
            if int(NodeList[node].c0) > l14_c0:
                l14_c0 = int(NodeList[node].c0)
            
            if int(NodeList[node].c1) > l14_c1:
                l14_c1 = int(NodeList[node].c1)

        if NodeList[node].level == 15: 
            if int(NodeList[node].c0) > l15_c0:
                l15_c0 = int(NodeList[node].c0)
            
            if int(NodeList[node].c1) > l15_c1:
                l15_c1 = int(NodeList[node].c1)

        if NodeList[node].level == 16: 
            if int(NodeList[node].c0) > l16_c0:
                l16_c0 = int(NodeList[node].c0)
            
            if int(NodeList[node].c1) > l16_c1:
                l16_c1 = int(NodeList[node].c1)
                
        if NodeList[node].level == 17: 
            if int(NodeList[node].c0) > l17_c0:
                l17_c0 = int(NodeList[node].c0)
            
            if int(NodeList[node].c1) > l17_c1:
                l17_c1 = int(NodeList[node].c1)

    output_file.write("Circuit Level,c0,c1\n")
    output_file.write("0,"  + str(l0_c0) + "," + str(l0_c1)   + "\n")
    output_file.write("1,"  + str(l1_c0) + "," + str(l1_c1)   + "\n")
    output_file.write("2,"  + str(l2_c0) + "," + str(l2_c1)   + "\n")
    output_file.write("3,"  + str(l3_c0) + "," + str(l3_c1)   + "\n")
    output_file.write("4,"  + str(l4_c0) + "," + str(l4_c1)   + "\n")
    output_file.write("5,"  + str(l5_c0) + "," + str(l5_c1)   + "\n")
    output_file.write("6,"  + str(l6_c0) + "," + str(l6_c1)   + "\n")
    output_file.write("7,"  + str(l7_c0) + "," + str(l7_c1)   + "\n")
    output_file.write("8,"  + str(l8_c0) + "," + str(l8_c1)   + "\n")
    output_file.write("9,"  + str(l9_c0) + "," + str(l9_c1)   + "\n")
    output_file.write("10," + str(l10_c0) + "," + str(l10_c1)  + "\n")
    output_file.write("11," + str(l11_c0) + "," + str(l11_c1)  + "\n")
    output_file.write("12," + str(l12_c0) + "," + str(l12_c1)  + "\n")
    output_file.write("13," + str(l13_c0) + "," + str(l13_c1)  + "\n")
    output_file.write("14," + str(l14_c0) + "," + str(l14_c1)  + "\n")
    output_file.write("15," + str(l15_c0) + "," + str(l15_c1)  + "\n")
    output_file.write("16," + str(l16_c0) + "," + str(l16_c1)  + "\n")
    output_file.write("17," + str(l17_c0) + "," + str(l17_c1)  + "\n")

def maxMCData(file):
    # Load back in saved resized images
    with open(f'{file}.pkl', 'rb') as f:
        data = pickle.load(f)
        f.close()    

    output_file = open(f"{file}_maxMC_results.csv", "w")

    NodeList = data[0]

    l0_n1, l1_n1, l2_n1, l3_n1, l4_n1, l5_n1, l6_n1, l7_n1, l8_n1, l9_n1, l10_n1, l11_n1, l12_n1, l13_n1, l14_n1, l15_n1, l16_n1, l17_n1 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    l0_n0, l1_n0, l2_n0, l3_n0, l4_n0, l5_n0, l6_n0, l7_n0, l8_n0, l9_n0, l10_n0, l11_n0, l12_n0, l13_n0, l14_n0, l15_n0, l16_n0, l17_n0 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 
    
    for node in NodeList:

        if NodeList[node].level == 0: 
            if int(NodeList[node].n0) > l0_n0:
                l0_n0 = int(NodeList[node].n0)
            
            if int(NodeList[node].n1) > l0_n1:
                l0_n1 = int(NodeList[node].n1)

        if NodeList[node].level == 1: 
            if int(NodeList[node].n0) > l1_n0:
                l0_n0 = int(NodeList[node].n0)
            
            if int(NodeList[node].n1) > l1_n1:
                l1_n1 = int(NodeList[node].n1)

        if NodeList[node].level == 2: 
          if int(NodeList[node].n0) > l2_n0:
              l2_n0 = int(NodeList[node].n0)
          
          if int(NodeList[node].n1) > l2_n1:
              l2_n1 = int(NodeList[node].n1)

        if NodeList[node].level == 3: 
            if int(NodeList[node].n0) > l3_n0:
                l3_n0 = int(NodeList[node].n0)
            
            if int(NodeList[node].n1) > l3_n1:
                l3_n1 = int(NodeList[node].n1)                

        if NodeList[node].level == 4: 
            if int(NodeList[node].n0) > l4_n0:
                l4_n0 = int(NodeList[node].n0)
            
            if int(NodeList[node].n1) > l4_n1:
                l4_n1 = int(NodeList[node].n1)

        if NodeList[node].level == 5: 
            if int(NodeList[node].n0) > l5_n0:
                l5_n0 = int(NodeList[node].n0)
            
            if int(NodeList[node].n1) > l5_n1:
                l5_n1 = int(NodeList[node].n1)

        if NodeList[node].level == 6: 
            if int(NodeList[node].n0) > l6_n0:
                l6_n0 = int(NodeList[node].n0)
            
            if int(NodeList[node].n1) > l6_n1:
                l6_n1 = int(NodeList[node].n1)

        if NodeList[node].level == 7: 
            if int(NodeList[node].n0) > l7_n0:
                l7_n0 = int(NodeList[node].n0)
            
            if int(NodeList[node].n1) > l7_n1:
                l7_n1 = int(NodeList[node].n1)

        if NodeList[node].level == 8: 
            if int(NodeList[node].n0) > l8_n0:
                l8_n0 = int(NodeList[node].n0)
            
            if int(NodeList[node].n1) > l8_n1:
                l8_n1 = int(NodeList[node].n1)

        if NodeList[node].level == 9: 
            if int(NodeList[node].n0) > l9_n0:
                l9_n0 = int(NodeList[node].n0)
            
            if int(NodeList[node].n1) > l9_n1:
                l9_n1 = int(NodeList[node].n1)

        if NodeList[node].level == 10: 
            if int(NodeList[node].n0) > l10_n0:
                l10_n0 = int(NodeList[node].n0)
            
            if int(NodeList[node].n1) > l10_n1:
                l10_n1 = int(NodeList[node].n1)

        if NodeList[node].level == 11: 
            if int(NodeList[node].n0) > l11_n0:
                l11_n0 = int(NodeList[node].n0)
            
            if int(NodeList[node].n1) > l11_n1:
                l11_n1 = int(NodeList[node].n1)

        if NodeList[node].level == 12: 
            if int(NodeList[node].n0) > l12_n0:
                l12_n0 = int(NodeList[node].n0)
            
            if int(NodeList[node].n1) > l12_n1:
                l12_n1 = int(NodeList[node].n1)

        if NodeList[node].level == 13: 
            if int(NodeList[node].n0) > l13_n0:
                l13_n0 = int(NodeList[node].n0)
            
            if int(NodeList[node].n1) > l13_n1:
                l13_n1 = int(NodeList[node].n1)

        if NodeList[node].level == 14: 
            if int(NodeList[node].n0) > l14_n0:
                l14_n0 = int(NodeList[node].n0)
            
            if int(NodeList[node].n1) > l14_n1:
                l14_n1 = int(NodeList[node].n1)

        if NodeList[node].level == 15: 
            if int(NodeList[node].n0) > l15_n0:
                l15_n0 = int(NodeList[node].n0)
            
            if int(NodeList[node].n1) > l15_n1:
                l15_n1 = int(NodeList[node].n1)

        if NodeList[node].level == 16: 
            if int(NodeList[node].n0) > l16_n0:
                l16_n0 = int(NodeList[node].n0)
            
            if int(NodeList[node].n1) > l16_n1:
                l16_n1 = int(NodeList[node].n1)
                
        if NodeList[node].level == 17: 
            if int(NodeList[node].n0) > l17_n0:
                l17_n0 = int(NodeList[node].n0)
            
            if int(NodeList[node].n1) > l17_n1:
                l17_n1 = int(NodeList[node].n1)

    output_file.write("Circuit Level,n0,n1\n")
    output_file.write("0,"  + str(l0_n0) + "," + str(l0_n1)   + "\n")
    output_file.write("1,"  + str(l1_n0) + "," + str(l1_n1)   + "\n")
    output_file.write("2,"  + str(l2_n0) + "," + str(l2_n1)   + "\n")
    output_file.write("3,"  + str(l3_n0) + "," + str(l3_n1)   + "\n")
    output_file.write("4,"  + str(l4_n0) + "," + str(l4_n1)   + "\n")
    output_file.write("5,"  + str(l5_n0) + "," + str(l5_n1)   + "\n")
    output_file.write("6,"  + str(l6_n0) + "," + str(l6_n1)   + "\n")
    output_file.write("7,"  + str(l7_n0) + "," + str(l7_n1)   + "\n")
    output_file.write("8,"  + str(l8_n0) + "," + str(l8_n1)   + "\n")
    output_file.write("9,"  + str(l9_n0) + "," + str(l9_n1)   + "\n")
    output_file.write("10," + str(l10_n0) + "," + str(l10_n1)  + "\n")
    output_file.write("11," + str(l11_n0) + "," + str(l11_n1)  + "\n")
    output_file.write("12," + str(l12_n0) + "," + str(l12_n1)  + "\n")
    output_file.write("13," + str(l13_n0) + "," + str(l13_n1)  + "\n")
    output_file.write("14," + str(l14_n0) + "," + str(l14_n1)  + "\n")
    output_file.write("15," + str(l15_n0) + "," + str(l15_n1)  + "\n")
    output_file.write("16," + str(l16_n0) + "," + str(l16_n1)  + "\n")
    output_file.write("17," + str(l17_n0) + "," + str(l17_n1)  + "\n")

# def closeAll():
#     while True:
#         k = cv.waitKey(0)
#         if k == ord('q'):
#             break       

#     cv.destroyAllWindows()   