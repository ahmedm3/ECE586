"""
Ahmed Abdulkareem
02/10/2015
Final Project
ALU Implementation
All rights reserved
"""

from myhdl import enum, Signal, intbv, always, delay, instance, instances, traceSignals, Simulation

ALU_OPS = enum(
    "ADD",
    "SUBTRACT",
    "MULTIPLY",
    "OR",
    "AND",
    "XOR"
    )

ALU_STATUSES = enum(
    "ZERO",
    "NEGATIVE",
    "POSITIVE"
    )

ALU_STATUS = [{}]


def ALU(A, B, result, status, clk, opcode, width=8):
    """
    ALU Implementation

    A      --> integer input (operand)
    B      --> integer input (operand)
    result --> output results of operation
    status --> output status (positive, zero, negative)
    clk    --> input clock
    opcode --> specifies the operation (look at ALU_OPS)
    """

    DELAY = 70

    #result = Signal(intbv(0)[width * 2 - 1:]) # make results to be a vector of size width

    #@always(clk.posedge)
    @instance
    def alu():
        while True:
            if opcode.val == ALU_OPS.OR:
                #yield delay(DELAY)
                yield clk.posedge
                result.next = A | B
            elif opcode.val == ALU_OPS.AND:
                yield clk.posedge
                result.next = A & B
            elif opcode.val == ALU_OPS.XOR:
                yield clk.posedge
                result.next = A ^ B
            elif opcode.val == ALU_OPS.ADD:
                yield clk.posedge
                result.next = A + B
            elif opcode.val == ALU_OPS.SUBTRACT:
                yield clk.posedge
                result.next = A - B
            elif opcode.val == ALU_OPS.MULTIPLY:
                yield delay(DELAY)
                result.next = A * B

            # check if anything happened (Zero, negative, etc..)
            if result.next < 0:
                status.next = Signal(ALU_STATUSES.NEGATIVE)
            elif result.next > 0:
                status.next = Signal(ALU_STATUSES.POSITIVE)
            elif result.next == 0:
                status.next = Signal(ALU_STATUSES.ZERO)

    return alu

if __name__ == "__main__":
    WIDTH = 8    
    def test_ALU():
        
        clk = Signal(bool(0))
        A, B = [Signal(intbv(-(2**(WIDTH-1)))) for i in range(2)]
        result = Signal(intbv(0))
        status = Signal(ALU_STATUSES.NEGATIVE)
        op = Signal(ALU_OPS.OR)
        alu_inst = ALU(A, B, result, status, clk, op)

        @always(delay(10))
        def clkdriver():
            clk.next = not clk

        A.next = 5
        B.next = 10

        return instances()

    tb = traceSignals(test_ALU)
    sim = Simulation(tb)
    sim.run(1000)

