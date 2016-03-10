"""
Ahmed Abdulkareem
02/10/2015
Final Project
ALU Implementation
All rights reserved
"""

import CPU

def ALU(A, B, opcode, width=32):
    """
    ALU Implementation

    A      --> integer input (operand)
    B      --> integer input (operand)
    opcode --> specifies the operation (look at ALU_OPS)
    width  --> specifies width of operands
    This function returns a dictionary with result and status
    """

    # result --> output results of operation
    result = 0
    # status --> output status (positive, zero, negative)
    status = ""

    # update results based on operation and 
    # increment the clock
    if opcode == "ADD":
        result = A + B
        CPU.GLOBAL_CLOCK += CPU.CLOCK_CYCLE
    elif opcode == "SUB":
        result = A - B
        CPU.GLOBAL_CLOCK += CPU.CLOCK_CYCLE
    elif opcode == "OR":
        result = A | B
        CPU.GLOBAL_CLOCK += CPU.CLOCK_CYCLE
    elif opcode == "AND":
        result = A & B
    elif opcode == "XOR":
        result = A ^ B
        CPU.GLOBAL_CLOCK += CPU.CLOCK_CYCLE
    elif opcode == "MULT":
        result = A * B
        CPU.GLOBAL_CLOCK += CPU.CLOCK_CYCLE * 32 

    # update status
    if result == 0:
        status = "ZERO"
    elif result > 0:
        status = "POSITIVE"
    else:
        status = "NEGATIVE"

    return {"RESULT": result, "STATUS": status}

if __name__ == "__main__":
    """
    for testing purposes
    """

    opcode_list = ["ADD", "SUB", "MULT", "XOR", "OR", "AND"]
    
    for opcode in opcode_list:
        print("Testing %s operation.." % opcode)
        print("%s Success!" % opcode)
        for i in range(10):
            for j in range(10):
                if opcode == "ADD":
                    if ALU(i, j, opcode)["RESULT"] != i + j:
                        print("ERROR: %d + %d != %d" % (i, j, ALU(i, j, "ADD")["RESULT"]))
                elif opcode == "SUB":
                    if ALU(i, j, opcode)["RESULT"] != i - j:
                        print("ERROR: %d - %d != %d" % (i, j, ALU(i, j, "SUBTRACT")["RESULT"]))
                elif opcode == "MULT":
                    if ALU(i, j, opcode)["RESULT"] != i * j:
                        print("ERROR: %d * %d != %d" % (i, j, ALU(i, j, "MULT")["RESULT"]))
                elif opcode == "OR":
                    if ALU(i, j, opcode)["RESULT"] != i | j:
                        print("ERROR: %d | %d != %d" % (i, j, ALU(i, j, "OR")["RESULT"]))
                elif opcode == "XOR":
                    if ALU(i, j, opcode)["RESULT"] != i ^ j:
                        print("ERROR: %d ^ %d != %d" % (i, j, ALU(i, j, "XOR")["RESULT"]))
                elif opcode == "AND":
                    if ALU(i, j, opcode)["RESULT"] != i & j:
                        print("ERROR: %d & %d != %d" % (i, j, ALU(i, j, "AND")["RESULT"]))

    print("Clock Cycles: %d" % (CPU.GLOBAL_CLOCK/CPU.CLOCK_CYCLE))

