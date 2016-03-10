"""
Ahmed Abdulkareem
02/10/2015
Final Project
Memory Implementation
All rights reserved
"""

import config

# Memory Space
MEM_SPACE = {}

def Mem(addr, din = 0, we = False):
    """
    din  --> input: data in
    addr --> input: address
    we   --> input: write enable
    CAS Latency: 2 clock cycles

    returns: data, and valid bit
    """
    data_out = {}

    global MEM_SPACE
    addr = addr.lower()

    if addr.startswith('0x'):
        addr = addr[2:]

    if we:
        din = din.lower()
        MEM_SPACE[addr] = []
        
        if din.startswith('0x'):
            din = din[2:]

        # convert to 32 bits if it isn't already
        while len(din) < 8:
            din = '0' + din

        # store each byte
        i = 0
        while i <= 6:
            MEM_SPACE[addr].append(din[i:i+2])
            i += 2
    elif addr in MEM_SPACE:
        data_out["DATA"] = MEM_SPACE[addr]
        data_out["VALID"] = True
    else:
        data_out["VALID"] = False
        data_out["DATA"] = False

    config.GLOBAL_CLOCK += 2 * config.CLOCK_CYCLE
    return data_out


if __name__ == "__main__":
    """
    for testing purposes
    """
    
    from random import randrange

    print("Filling memory..")
    for i in range(5):
        data = hex(randrange(100))
        print("Writing %s to address %s" % (data, hex(i*4)))
        Mem(hex(i*4)[2:], din = data, we = True)

    print("\n-----------------")
    for i in range(6):
        print("Value at address %s: %s and it's %s" % (hex(i*4), Mem(hex(i*4))["DATA"], "valid" if Mem(hex(i*4))["VALID"] else "not valid"))
