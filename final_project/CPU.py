"""
Ahmed Abdulkareem
02/10/2015
Final Project
CPU Implementation
All rights reserved
"""

import argparse
import Memory


GLOBAL_CLOCK = 0 # global clock
CLOCK_CYCLE = 32 * 10 # clock cycle
PC = 0 # program counter
STACK = []

def CPU(args):

    global PC

    Memory.Mem(0, din=0x54325, we=True)
    Memory.Mem(4, din=0x5AA25, we=True)
    Memory.Mem(8, din=0x5B00A5, we=True)

    #while True:
    print(fetch(PC))
    PC += 4
    print(fetch(PC))




def fetch(addr):
    """
    this function fetches an instruction
    from the address given
    addr --> input: address of instruction
    
    returns: The instruction fetched
    """

    return Memory.Mem(addr)

def decode():
    pass


# -------------------------------------
# Parser
# -------------------------------------
parser = argparse.ArgumentParser(description = 'CPU Simulator')
parser.add_argument('-mem', metavar = 'Mem File', help = "path to memory image")
parser.set_defaults(func = CPU)

if __name__ == "__main__":
    args = parser.parse_args()
    args.func(args)
