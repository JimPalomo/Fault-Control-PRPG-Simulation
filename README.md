## ECE 464 Combined Project

### Description
The project covers three major projects done in ECE 464: Testing, Reliability, and Security of Digital Systems. The main topics covered in these projects are Fault Simulation, Controllability / Monte Carlo (MC), and Psuedo-Random Pattern Generation (PRPG) on bench c432.bench.

### Functionality: 
1: Fault Simulation
- A. Normal Circuit Simulation: the circuit will be simulated provided the user's test vector (TV)

- B. Single TV single fault: determines if a single fault is detected at an output node (e.g. a-1 or d-a-1) provided user TV

- C. Single TV all faults: given one user test vector, all possible faults are simulated based on the circuit

- D. Best 5 TV for all faults: generate 5 total test vectors (4 additional) that covers as much faults as possible

2: Controllability & Monte Carlo (MC): 
- Simulate controllability and Monte Carlo
- Controllability: the ability to control a value (0 or 1) whether input, output, or intermediate wire/node
- Monte Carlo: simulates as much test vectors (exhaustively if <=10 INPUT nodes otherwise 1000 randomly generated TV) to produce the number of times a 0 or 1 has occurred at a node.

3: Psuedo-Random Pattern Generation (PRPG) on bench c432.bench
- Generate data for all possible faults within a circuit based on an LFSR design to generate input Test Vectors 
- Data acquired covers Fault, Controllability, and Monte Carlo (MC) simulations
- Capable of being used for research purposes of distinguishing how the location of a node within a circuit affects the ease of controlling the value (through controllability, MC, node level, etc)
- Available taps: h=1 | h=1, 3, 5 | h=2, 4, 6 | h=6, 7, 8


### Available bench files: 
- c17, c432, c499, c880, c1355, c1908, c2670, c3540, c5315, c6288, hw1, hw2.2, hw2, p2


### Improvements:
- Let the user enter custom LFSR tap 

### Example
![alt text](https://github.com/JimPalomo/Fault-Control-PRPG-Simulation/blob/master/assets/sample-1.png)
![alt text](https://github.com/JimPalomo/Fault-Control-PRPG-Simulation/blob/master/assets/sample-2.png)
