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
from random import randrange

#instruction format
#0001 1000 0000 0000 0000 0010 0000 0011
#00110 000000001 000000000 000000101
# opc   src1       src2       dest
def CPU(args):
    
    #Memory.Mem('0x0', din = '0x20000102', we = True) # ADD R2, R1, R0
    #Memory.Mem('0x4', din = '0x20000203', we = True) # ADD R3, R2, R1
    #for i in range(16):
        #Memory.Mem(hex((i + 20) * 4), din = hex(randrange(1000)), we = True)
    Memory.Mem(hex(4*100), din = '0x1', we = True)
    Memory.Mem(hex(4*101), din = '0x3', we = True)
    Memory.Mem(hex(4*102), din = '0x5', we = True)
    Memory.Mem(hex(4*103), din = '0x9', we = True)
    config.REGISTER[0] = 4*100
    config.REGISTER[1] = 4*101
    config.REGISTER[2] = 4*102
    config.REGISTER[3] = 4*103
    config.REGISTER[9] = 1
    config.REGISTER[10] = -4
    """
    Memory.Mem('0x0', din = '0x30000004', we = True) # LOAD R4, [R0]
    Memory.Mem('0x4', din = '0x30040005', we = True) # LOAD R5, [R1]
    Memory.Mem('0x8', din = '0x281408063', we = True) # MULT R6, R5, R4
    Memory.Mem('0xC', din = '0x30080C04', we = True) # LOAD R4, [R2]
    Memory.Mem('0x10', din = '0x300C0805', we = True) # LOAD R5, [R3]
    Memory.Mem('0x14', din = '0x28100A07', we = True) # MULT R7, R4, R5
    Memory.Mem('0x18', din = '0xF8080C04', we = True) # MULT R7, R4, R5
    Memory.Mem('0x1C', din = '0x181C0C08', we = True) # ADD R8, R6, R7
    Memory.Mem('0x20', din = '0x48201208', we = True) # BEQ R8, R9
    Memory.Mem('0x24', din = '0xF8080C04', we = True) # LOOP
    Memory.Mem('0x28', din = '0x20040601', we = True) # SUB R1, R1, R3
    Memory.Mem('0x2C', din = '0x48041209', we = True) # BEQ R1, R9
    """
    Memory.Mem('0x0', din = '0xF8080C04', we = True) # LOOP
    Memory.Mem('0x4', din = '0x1828120A', we = True) # ADD R10, R10, R9
    Memory.Mem('0x8', din = '0x5828120A', we = True) # BEQ R10
    #Memory.Mem('0x8', din = '0x38180007', we = True) # STR R6, [R7]
    Memory.Mem('0xC', din = '0x68000000', we = True) # HALT
    print(config.REGISTER)
    print(Memory.MEM_SPACE)

    # loop until HALT
    decoded = {'OPCODE': 'None'}
    while 'OPCODE' in decoded and decoded['OPCODE'] != 'HALT':
        instruc = fetch(hex(config.PC))  # fetch 
        decoded = decode(instruc['DATA']) # decode
        print('INSTRUCTION: %s, SRC1: %s, SRC2: %s, DEST: %s' % (decoded['OPCODE'], int(decoded['SRC1'], 16), int(decoded['SRC2'], 16), int(decoded['DEST'], 16)))
        execute(decoded) # execute
        ALU.ALU(0, 0, 'ADD') # add 4 to pc
        config.PC += 4
    
    print(Memory.MEM_SPACE)
    print(config.REGISTER)
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
    
    # if opcode is LOAD
    elif opcode == 'LOAD':
        reg = int(decoded_ins['SRC1'], 16)
        load(int(decoded_ins['DEST'], 16), hex(config.REGISTER[reg])) 

    # if opcode is STR
    elif opcode == 'STR':
        register = int(decoded_ins['SRC1'], 16)
        value = hex(config.REGISTER[register])
        addr = hex(config.REGISTER[int(decoded_ins['DEST'], 16)])
        store(value, addr)

    # if opcode is BEQ
    elif opcode == 'BEQ':
        equal = ALU.ALU(config.REGISTER[int(decoded_ins['SRC1'], 16)], config.REGISTER[int(decoded_ins['SRC2'], 16)], 'SUB')['STATUS']
        if equal == 'ZERO':
            config.PC = config.JUMPS.pop()
        config.GLOBAL_CLOCK += 1 # compare latency (XOR)

    # if opcode is BP, BN, BZ
    elif opcode == 'BP':
        value = config.REGISTER[int(decoded_ins['SRC1'], 16)]
        if value > 0:
            config.PC = config.JUMPS.pop()
        config.GLOBAL_CLOCK += 1 # compare latency (XOR)
    
    # if opcode is BN
    elif opcode == 'BN':
        value = config.REGISTER[int(decoded_ins['SRC1'], 16)]
        if value < 0:
            config.PC = config.JUMPS.pop()
        config.GLOBAL_CLOCK += 1 # compare latency (XOR)
    
    # if opcode is BZ
    elif opcode == 'BZ':
        value = config.REGISTER[int(decoded_ins['SRC1'], 16)]
        if value == 0:
            config.PC = config.JUMPS.pop()
        config.GLOBAL_CLOCK += 1 # compare latency (XOR)

        

def load(dest, addr):
    """
    function to load value at specified address
    dest --> input: destination register
    addr --> input: address in memory
    """
    config.REGISTER[dest] = int(''.join(Memory.Mem(addr)['DATA']), 16)

def store(value, addr):
    """
    function to store given value
    at a specified address
    value --> input: register with value
    addr  --> input: address in memory
    """
    Memory.Mem(addr, din = value, we = True)



# -------------------------------------
# Parser
# -------------------------------------
parser = argparse.ArgumentParser(description = 'CPU Simulator')
parser.add_argument('-mem', metavar = 'Mem File', help = "path to memory image")
parser.set_defaults(func = CPU)

if __name__ == "__main__":
    args = parser.parse_args()
    args.func(args)
