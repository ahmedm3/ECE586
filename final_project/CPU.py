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

STACK = []

def CPU(args):
    
    Memory.Mem('0x0', din = '0x00000000', we = True)
    Memory.Mem('0x4', din = '0x10000000', we = True)
    Memory.Mem('0x8', din = '0x30000000', we = True)
    Memory.Mem('0xc', din = '0xD0000000', we = True)

    #while True:
    decoded = {'OPCODE': 'None'}
    while 'OPCODE' in decoded and decoded['OPCODE'] != 'HALT':
        instruc = fetch(hex(config.PC))  
        decoded = decode(instruc['DATA'])
        print(decoded['OPCODE'])
        ALU.ALU(0, 0, 'ADD')
        config.PC += 4
    
    print("CLOCK: %d" % config.GLOBAL_CLOCK)


def fetch(addr):
    """
    this function fetches an instruction
    from the address given
    addr --> input: address of instruction
    
    returns: The instruction fetched
    """

    return Memory.Mem(addr)

def decode(ins):
    return instruction_decoder.decode(ins)


# -------------------------------------
# Parser
# -------------------------------------
parser = argparse.ArgumentParser(description = 'CPU Simulator')
parser.add_argument('-mem', metavar = 'Mem File', help = "path to memory image")
parser.set_defaults(func = CPU)

if __name__ == "__main__":
    args = parser.parse_args()
    args.func(args)
