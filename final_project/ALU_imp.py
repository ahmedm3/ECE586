"""
Ahmed Abdulkareem
02/10/2015
Final Project
ALU Implementation
All rights reserved
"""

from myhdl import enum, Signal, intbv, always

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

    #result = Signal(intbv(0)[width * 2 - 1:]) # make results to be a vector of size width

    @always(clk.posedge)
    def alu():
        if opcode.val == ALU_OPS.OR:
            result.next = A | B
        elif opcode.val == ALU_OPS.AND:
            result.next = A & B
        elif opcode.val == ALU_OPS.XOR:
            result.next = A ^ B
        elif opcode.val == ALU_OPS.ADD:
            result.next = A + B
        elif opcode.val == ALU_OPS.SUBTRACT:
            result.next = A - B
        elif opcode.val == ALU_OPS.MULTIPLY:
            result.next = A * B

        # check if anything happened (Zero, negative, etc..)
        if result.next < 0:
            status.next = Signal(ALU_STATUSES.NEGATIVE)
        elif result.next > 0:
            status.next = Signal(ALU_STATUSES.POSITIVE)
        elif result.next == 0:
            status.next = Signal(ALU_STATUSES.ZERO)

    return alu
