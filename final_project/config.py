"""
Ahmed Abdulkareem
02/10/2015
Final Project
Config Implementation
All rights reserved
"""

# initial values of clock
# and pc
GLOBAL_CLOCK = 0
CLOCK_CYCLE = 32 * 10
PC = 0
ISA = {'0': 'AND', '1': 'OR', '2': 'XOR', '3': 'ADD', 
       '4': 'SUB', '5': 'MULT', '6': 'PUSH', '7': 'POP',
       '8': 'BZ', '9': 'BEQ', 'a': 'BP', 'b': 'BN', 
       'c': 'JR', 'd': 'HALT'}
