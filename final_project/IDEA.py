"""
Ahmed Abdulkareem
02/10/2015
Final Project
IDEA Implementation
All rights reserved
"""

from ALU_imp import ALU

def rol(val, r_bits, max_bits):

    return (val << r_bits%max_bits) & (2**max_bits-1) | ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))

def keygen(key):

    array = [[]]

    for i in range(8):
    #for i in range(4):
        key_list = [x for x in key]
        sub_keys = []
        
        # sub keys
        """
        Z1 = int(''.join(key_list[:4]), 16)
        Z2 = int(''.join(key_list[4:8]), 16)
        Z3 = int(''.join(key_list[8:12]), 16)
        Z4 = int(''.join(key_list[12:16]), 16)
        Z5 = int(''.join(key_list[16:20]), 16)
        Z6 = int(''.join(key_list[20:24]), 16)
        Z7 = int(''.join(key_list[24:28]), 16)
        Z8 = int(''.join(key_list[28:32]), 16)
        """
        
        sub_keys.append(int(''.join(key_list[:4]), 16))
        sub_keys.append(int(''.join(key_list[4:8]), 16))
        sub_keys.append(int(''.join(key_list[8:12]), 16))
        sub_keys.append(int(''.join(key_list[12:16]), 16))
        sub_keys.append(int(''.join(key_list[16:20]), 16))
        sub_keys.append(int(''.join(key_list[20:24]), 16))
        sub_keys.append(int(''.join(key_list[24:28]), 16))
        sub_keys.append(int(''.join(key_list[28:32]), 16))
        
        #for j in range(len(key_list)):
            #sub_keys.append(int(''.join(key_list[j]), 16))

        count = 0
        #while len(array[i]) <= 6:
        while len(array[i]) < 6:
            array[i].append(sub_keys[count])
            count += 1
        array.append([])
        #while count >= 6 and count < 8:
        while len(array[i + 1]) < 6 and count < 8:
            array[i + 1].append(sub_keys[count])
            count += 1

        if count < 8:
            array.append([])
            while len(array[i + 2]) < 6 and count < 8:
                array[i + 2].append(sub_keys[count])
                count += 1

        #key = rol(int(key, 16), 6, 32)
        key = rol(int(key, 16), 25, 128)
        key = hex(key)[2:]
        #while len(key) < 8:
        while len(key) < 32:
            key = '0' + key
        #print(key)
    #for i in range(len(array)):
        #array[i] = [hex(x) for x in array[i]]
        #array[i] = [bin(x) for x in array[i]]

    return array

    

def IDEA(data, key):

    """
    data --> 64-bit string        input: data to be encrypted
    key  --> 128-bit string (hex) input: key
    
    this function returns encrpyted data
    """
    
    data_list = [x for x in data]
    #print(data_list)
    #key_list  = [x for x in key]
    key = keygen(key)
    """
    for x in range(len(key)):
        key[x] = [hex(y) for y in key[x]]
    print(key)
    return
    """
    # sub data
    X1 = int(''.join(data_list[:4]), 16)
    X2 = int(''.join(data_list[4:8]), 16)
    X3 = int(''.join(data_list[8:12]), 16)
    X4 = int(''.join(data_list[12:16]), 16)
    """
    # sub keys
    Z1 = int(''.join(key_list[:4]), 16)
    Z2 = int(''.join(key_list[4:8]), 16)
    Z3 = int(''.join(key_list[8:12]), 16)
    Z4 = int(''.join(key_list[12:16]), 16)
    Z5 = int(''.join(key_list[16:20]), 16)
    Z6 = int(''.join(key_list[20:24]), 16)
    Z7 = int(''.join(key_list[24:28]), 16)
    Z8 = int(''.join(key_list[28:32]), 16)
    subkeys_list = [Z1, Z2, Z3, Z4, Z5, Z6, Z7, Z8]
    """
    for i in range(8):
        print("ROUND%d\nKEY: %s" % (i, hex(key[i][0]) + hex(key[i][1]) + hex(key[i][2]) + hex(key[i][3]) + hex(key[i][4]) + hex(key[i][5])))
        print("DATA: %s %s %s %s" % (hex(X1), hex(X2), hex(X3), hex(X4)))
        result_1 = mult(X1, key[i][0]) # first step
        result_2 = add(X2, key[i][1]) # second step
        result_3 = add(X3, key[i][2]) # third 
        result_4 = mult(X4, key[i][3]) # fourth
        result_5 = result_1 ^ result_3
        result_6 = result_2 ^ result_4
        result_7 = mult(result_5, key[i][4])
        result_8 = add(result_6, result_7)
        result_9 = mult(result_8, key[i][5])
        result_10 = add(result_7, result_9)
        X1 = result_1 ^ result_9
        X2 = result_3 ^ result_9
        X3 = result_2 ^ result_10
        X4 = result_4 ^ result_10

    results = []

    print("ROUND%d\nKEY: %s" % (8.5, hex(key[8][0]) + hex(key[8][1]) + hex(key[8][2]) + hex(key[8][3])))
    results.append(mult(X1, key[8][0]))
    results.append(add(X2, key[8][1]))
    results.append(add(X3, key[8][2]))
    results.append(mult(X4, key[8][3]))

    for i in range(len(results)):
        results[i] = hex(results[i])[2:]
    print(results)

def mult(A, B):

    if A == 0:
        A = 2**16
    if B == 0:
        B = 2**16
    
    #result = A * B - (2**16 + 1)
    return A * B % (2**16 + 1)

    while result > (2**16 + 1):
        result -= (2**16 + 1)

    return result

def add(A, B):

    #result = A + B - (2**16)
    return A + B % (2**16)
    
    while result > 2**16:
        result -= 2**16

    return result


IDEA('05320a6414c819fa', '006400c8012c019001f4025802bc0320')
#keygen('0123456789ABCDEF0123456789ABCDEF')
#keygen('DC6F3F59')
#print(bin(rol(0xC, 2, 4)))
