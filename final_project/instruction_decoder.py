"""
Ahmed Abdulkareem
02/10/2015
Final Project
Instruction Decoder Implementation
All rights reserved
"""

import config

def decode(instruction):
    """
    Instruction Format: 
    decodes instruction
    instruction --> input: list of four elements (32 bits)

    returns: decoded instruction
    """

    decoded = {}
    opcode = instruction[0][0]
    
    if opcode in config.ISA:
        decoded['OPCODE'] = config.ISA[opcode]

    return decoded

if __name__ == '__main__':

    for i in range(14):
        print(decode(['%s0' % hex(i)[2:], '00', '00', '00'])['OPCODE'])
