"""
Ahmed Abdulkareem
02/10/2015
Final Project
ALU Test Bench Implementation
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

    #A, B = [Signal(intbv(0)[WIDTH:]) for i in range(2)]
    #A, B = [Signal(intbv(-(2**(WIDTH-1)), min=-(2**(WIDTH-1)), max=2**(WIDTH-1)-1)[WIDTH:]) for i in range(2)]
    A, B = [Signal(intbv(-(2**(WIDTH-1)))) for i in range(2)]
    #result = Signal(intbv(0)[WIDTH * 2:], min=-(2**(WIDTH-1)) * (2**(WIDTH-1)-1), max=2**(WIDTH * 2))
    #result = Signal(intbv(0, min=-(2**(WIDTH-1)) * (2**(WIDTH-1)-1), max=2**(WIDTH * 2))[WIDTH * 2:])
    result = Signal(intbv(0))
    clk = Signal(bool(0))
    status = Signal(ALU_STATUSES.NEGATIVE) # Intialize to negative (doesn't matter)

    ERR = False # will be true when an error occurs

    ALU_inst = ALU(A, B, result, status, clk, opcode)

    @always(delay(10))
    def clkgen():
        clk.next = not clk

    #@always(clk.negedge)
    @always(delay(105))
    def stimulus():
        #if A.val != (2**WIDTH - 1):
        if A.val != (2**(WIDTH-1) - 1):
            A.next += 1
        else:
            #A.next = 0
            A.next = -(2**(WIDTH-1))
            #if B.val != (2**WIDTH - 1):
            if B.val != (2**(WIDTH-1) - 1):
                B.next += 1

    @instance
    def self_check():
        while True:
            #yield clk.posedge
            #yield delay(5)
            yield result
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
                    print("Error: %d ^ %d -> %d ?" % (A.val, B.val, result.val))
                    ERR = True
            elif opcode.val == Signal(ALU_OPS.ADD):
                if result.val != (A.val + B.val):
                    print("Error: %d + %d -> %d ?" % (A.val, B.val, result.val))
                    ERR = True
            elif opcode.val == Signal(ALU_OPS.SUBTRACT):
                if result.val != (A.val - B.val):
                    print("Error: %d - %d -> %d ?" % (A.val, B.val, result.val))
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
        elif argv[1].lower() == "add":
            opcode = Signal(ALU_OPS.ADD)
        elif argv[1].lower() == "subtract":
            opcode = Signal(ALU_OPS.SUBTRACT)
        elif argv[1].lower() == "multiply":
            opcode = Signal(ALU_OPS.MULTIPLY)

    simulate(20 * (2**(2*WIDTH) - 1) + 20)
