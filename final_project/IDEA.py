"""
Ahmed Abdulkareem
02/10/2015
Final Project
IDEA Implementation
All rights reserved
"""

from ALU_imp import ALU

def keygen(key):

	key_list 


def IDEA(data, key):

	"""
	data --> 64-bit string        input: data to be encrypted
	key  --> 128-bit string (hex) input: key
	
	this function returns encrpyted data
	"""
	
	data_list = [x for x in data] 
	key_list  = [x for x in key]
	
	# sub data
	X1 = int(''.join(data_list[:4]), 16)
	X2 = int(''.join(data_list[4:8]), 16)
	X3 = int(''.join(data_list[8:12]), 16)
	X4 = int(''.join(data_list[12:16]), 16)

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

	for i in range(8):
		result_1 = mult(X1, Z1) # first step
		result_2 = add(X2, Z2) # second step
		result_3 = add(X3, Z3) # third 
		result_4 = mult(X4, Z4) # fourth
		result_5 = result_1 ^ result_3
		result_6 = result_2 ^ result_4
		result_7 = mult(result_5, Z5)
		result_8 = add(result_6, result_7)
		result_9 = mult(result_8, Z6)
		result_10 = add(result_7, result9)
		X1 = mult(result_1, result_9)
		X3 = mult(result_3, result_9)
		X2 = mult(result_2, result_10)
		X4 = mult(result_4, result_10)

		Z1 = Z7	

	results = []

	results.append(mult(X1, Z1))
	results.append(add(X2, Z2))
	results.append(add(X3, Z3))
	results.append(mult(X4, Z4))
	

def mult(A, B):

	if A == 0:
		A = 2**16
	if B == 0:
		B = 2**16
	
	result = A * B - (2**16 + 1)

	while result > (2**16 + 1):
		result -= (2**16 + 1)

	return result

def add(A, B):

	result = A + B - (2**16)
	
	while result > 2**16:
		result -= 2**16

	return result


IDEA('0123456789ABCDEF', '0123456789ABCDEF0123456789ABCDEF')
