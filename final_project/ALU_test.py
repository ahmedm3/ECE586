"""
Ahmed Abdulkareem
02/10/2015
Final Project
ALU Implementation
All rights reserved
"""

from random import randrange
from ALU_imp import ALU, ALU_OPS, ALU_STATUSES
from myhdl import Signal, intbv, traceSignals, Simulation
from myhdl import always, delay, instances, instance
from sys import argv

# width of ALU 
WIDTH = 8
opcode = Signal(ALU_OPS.OR)

def test_ALU():

    A, B = [Signal(intbv(0)[WIDTH:]) for i in range(2)]
    result = Signal(intbv(0)[WIDTH * 2 - 1:])
    clk = Signal(bool(0))
    status = Signal(ALU_STATUSES.NEGATIVE) # Intialize to negative (doesn't matter)

    ERR = False # will be true when an error occurs

    ALU_inst = ALU(A, B, result, status, clk, opcode)

    @always(delay(10))
    def clkgen():
        clk.next = not clk

    @always(clk.negedge)
    def stimulus():
        if A.val != (2**WIDTH - 1):
            A.next += 1
        else:
            A.next = 0
            if B.val != (2**WIDTH - 1):
                B.next += 1
        #if A == (2**WIDTH - 1):
            #A.next = 0
            #B.next += 1
        #if B == (2**WIDTH - 1):
            #B.next = 0

    @instance
    def self_check():
        while True:
            yield clk.posedge
            yield delay(5)
            if opcode.val == Signal(ALU_OPS.OR):
                if result.val != (A | B):
                    print("Error: %d | %d -> %d ?" % (A.val, B.val, result.val))
                    ERR = True
            elif opcode.val == Signal(ALU_OPS.AND):
                if result.val != (A.val & B.val):
                    print("Error: %d & %d -> %d ?" % (A.val, B.val, result.val))
                    ERR = True
            elif opcode.val == Signal(ALU_OPS.XOR):
                if result.val != (A.val ^ B.val):
                    print("Error: %d & %d -> %d ?" % (A.val, B.val, result.val))
                    ERR = True
    if ERR:
        print("There was an error!")
        exit(1)
    return instances()

def simulate(timesteps):

    tb = traceSignals(test_ALU)
    sim = Simulation(tb)
    sim.run(timesteps)


if __name__ == "__main__":

    if len(argv) > 1:
        if argv[1].lower() == "and":
            opcode = Signal(ALU_OPS.AND)
        elif argv[1].lower() == "or":
            opcode = Signal(ALU_OPS.OR)
        elif argv[1].lower() == "xor":
            opcode = Signal(ALU_OPS.XOR)
    simulate(20 * (2**(2*WIDTH) - 1) + 20)
