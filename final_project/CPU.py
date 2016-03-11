"""
Ahmed Abdulkareem
02/10/2015
Final Project
CPU Implementation
All rights reserved
"""

import argparse
import Memory
import ALU
import instruction_decoder
import config

#instruction format
#0001 1000 0000 0000 0000 0001 0000 0010
#01101 000000000 000000000 000000000
#0110 1000 0000 0000 0000 0010 0000 0010
#0x18000202
# opc   src1       src2       dest
def CPU(args):
    
    Memory.Mem('0x0', din = '0x20000102', we = True)
    Memory.Mem('0x4', din = '0x68000000', we = True)

    #while True:
    decoded = {'OPCODE': 'None'}
    while 'OPCODE' in decoded and decoded['OPCODE'] != 'HALT':
        instruc = fetch(hex(config.PC))  
        decoded = decode(instruc['DATA'])
        print('INSTRUCTION: %s, SRC1: %s, SRC2: %s, DEST: %s' % (decoded['OPCODE'], int(decoded['SRC1'], 16), int(decoded['SRC2'], 16), int(decoded['DEST'], 16)))
        execute(decoded)
        ALU.ALU(0, 0, 'ADD')
        config.PC += 4
    
    print(config.REGISTER)
    #print("CLOCK: %d" % (config.GLOBAL_CLOCK)
    print("CLOCK: %d" % (config.GLOBAL_CLOCK/config.CLOCK_CYCLE))


def fetch(addr):
    """
    this function fetches an instruction
    from the address given
    addr --> input: address of instruction
    
    returns: The instruction fetched
    """

    return Memory.Mem(addr)

def decode(ins):
    """
    this function decodes instruction
    
    returns: instruction decoded
    """
    return instruction_decoder.decode(ins)

def execute(decoded_ins):
    """
    function to excute given instruction
    """
    
    opcode = decoded_ins['OPCODE']

    # if opcode is arithmetic operation
    if opcode == 'ADD' or opcode == 'SUB' or opcode == 'MULT' or opcode == 'XOR' or opcode == 'OR' or opcode == 'AND':
        config.REGISTER[int(decoded_ins['DEST'], 16)] = ALU.ALU(config.REGISTER[int(decoded_ins['SRC1'], 16)], config.REGISTER[int(decoded_ins['SRC2'], 16)], opcode)['RESULT']


# -------------------------------------
# Parser
# -------------------------------------
parser = argparse.ArgumentParser(description = 'CPU Simulator')
parser.add_argument('-mem', metavar = 'Mem File', help = "path to memory image")
parser.set_defaults(func = CPU)

if __name__ == "__main__":
    args = parser.parse_args()
    args.func(args)
