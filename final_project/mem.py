"""
Ahmed Abdulkareem
02/10/2015
Final Project
Memory Implementation
All rights reserved
"""

from myhdl import always

def mem_space(dout, din, addr, we, en, clk):

    """
    dout --> output: content of a specified addr
    din  --> input : content to go to a specified addr
    addr --> input : specified address to write to or read from
    we   --> input : write enable, should be true to write
    en   --> input : enables memory
    clk  --> input : clock
    """

    mem = {} # memory space

    @always(clk.posedge)
    def access():
        if en: # if enabled 
            if we: # if it's a write
                mem[addr.val] = din.val
            elif addr.val in mem: # if it's a read
                dout.next = mem[addr.val]

    return access
