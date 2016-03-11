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
    decoded_bin = bin(int(''.join(instruction), 16))[2:]

    while len(decoded_bin) < 32:
        decoded_bin = '0' + decoded_bin
    
    opcode = hex(int(decoded_bin[0:5], 2))[2:]
    
    if opcode in config.ISA:
        decoded['OPCODE'] = config.ISA[opcode]
    
    src1 = hex(int(decoded_bin[5:15], 2))[2:]
    src2 = hex(int(decoded_bin[15:24], 2))[2:]
    dest = hex(int(decoded_bin[24:32], 2))[2:]

    #src1 = extend_to_32(src1)
    #src2 = extend_to_32(src2)
    #dest = extend_to_32(dest)
    
    decoded['SRC1'] = src1
    decoded['SRC2'] = src2
    decoded['DEST'] = dest
    
    config.GLOBAL_CLOCK += 2 # 2 clock cycles (because we have latency of 2 for our memroy)

    return decoded

def extend_to_32(data):

    while len(data) < 8:
        data = '0' + data

    return data

if __name__ == '__main__':

    for i in range(14):
        print(decode(['%s0' % hex(i)[2:], '00', '00', '00'])['OPCODE'])
