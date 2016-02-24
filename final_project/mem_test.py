"""
Ahmed Abdulkareem
02/10/2015
Final Project
Memory Test Bench
All rights reserved
"""

from random import randrange
from myhdl import Signal, intbv, traceSignals, Simulation
from myhdl import always, delay, instances, instance
from mem import mem_space

def test_mem():

    # make signals
    din, dout, addr = [Signal(0) for i in range(3)]
    we, en = [Signal(bool(1)) for i in range(2)]
    clk = Signal(bool(0))

    # instantiate memory
    mem_inst = mem_space(dout, din, addr, we, en, clk)

    # generate clock
    @always(delay(10))
    def clkgen():
        clk.next = not clk

    @always(clk.negedge)
    def stimulus():
        din.next = Signal(randrange(20))
        addr.next = Signal(randrange(5))
        we.next = Signal(randrange(2))

    return instances()

def simulate(timesteps):

    tb = traceSignals(test_mem)
    sim = Simulation(tb)
    sim.run(timesteps)

simulate(1000)
