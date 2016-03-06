"""
Ahmed Abdulkareem
02/10/2015
Final Project
IDEA Implementation
"""

import os,sys
#import ALU_imp

def makehex(value, size = 4):
        """
        function to make hex values
        not needed at the moment but 
        could be used when using ascii
        values instead of hex
        """
	temp = hex(value)[2:]
	if temp[-1] == 'L': temp= temp[:-1]
	return temp.zfill(size)

def pkcs5(hexdata):
        """
        function to pad hex data
        """
        
	pad = hex(8-(len(hexdata)//2)%8)[2:]
	while len(pad) < 2:
		pad = '0'+ pad
	for x in range(int(pad,16)):
		hexdata+= str(pad)
	return hexdata

def add(a,b):
	return (a + b) % (2**16)

def mult(value1,value2):
	if value1 == 0:
		value1 = 65536
	if value2 == 0:
		value2 = 65536
	value1 = (value1*value2) % 65537
	if value1 == 65536:
		value1 = 0;
	return value1

def invmod(b):
	a=65537
	x = 0 ; lastx = 1
	y = 1 ; lasty = 0
	while b != 0:
		quotient = a // b
		temp = b
		b = a % b
		a = temp
		temp = x
		x = lastx-quotient*x
		lastx = temp
		temp = y
		y = lasty-quotient*y
		lasty = temp
	while lasty < 0:
		lasty += 65537
	return lasty

def two_comp(a):
	return (a^0xffff) + 1

def keygen(key, mode, makefile='n'):
	temp =[]
	for x in range(7):
		for y in range(8):
			temp += [key[4*y:4*y+4]]
		key = bin(int(key,16))[2:]
		while len(key) < 128:
			key = '0'+key
		key = makehex(int(key[25:]+key[0:25],2),32)
	temp = temp[0:52]
	key = [int(x,16) for x in temp]
	key = [key[0:6],key[6:12],key[12:18],key[18:24],key[24:30],key[30:36],key[36:42],key[42:48],key[48:52]]
	if makefile == 'y':
		file.write('\nKey Expansion:\n')
		for x in range(8):
			for y in range(6):
				file.write(makehex(key[x][y]) + ' ')
			file.write('\n')
		for x in range(4):
			file.write(makehex(key[8][x]) + ' ')
	if mode == 'd':
		temp =[]
		for x in range(8):
			for y in range(6):
				temp += [key[x][y]]
		temp += [key[8][0],key[8][1],key[8][2],key[8][3]]
		key = []
		for x in range(8):
			key += [	invmod(temp[48-6*x]),
					two_comp(temp[50-6*x]),
					two_comp(temp[49-6*x]),
					invmod(temp[51-6*x]),
					temp[46-6*x],
					temp[47-6*x]
					]
		key += [invmod(temp[0]),two_comp(temp[1]),two_comp(temp[2]),invmod(temp[3])]
		key = [key[0:6],key[6:12],key[12:18],key[18:24],key[24:30],key[30:36],key[36:42],key[42:48],key[48:]]
		t = key[0][2]
		key[0][2] = key[0][1]
		key[0][1] = t
		if makefile == 'y':
			file.write('\n\nSince decrypting:\n')
			for x in range(8):
				for y in range(6):
					file.write(makehex(key[x][y]) + ' ')
				file.write('\n')
			for x in range(4):
				file.write(makehex(key[8][x]) + ' ')
	return key

def IDEA(data, key, mode, makefile='n'):
	if makefile == 'y':
		file.write('International Data Encryption Algorithm work\n\nInput: ' + data + '\nKey:   ' + key + '\n')
	key = keygen(key,mode,makefile)
	times = len(data)//16
	ctext = ''
	for r in range(times):
		input = data[16*r:16*(r+1)]
		x1 = int(input[:4],16)
		x2 = int(input[4:8],16)
		x3 = int(input[8:12],16)
		x4 = int(input[12:],16)
		if makefile == 'y':
			file.write('\n\nBlock ' + str(r+1))
		for x in range(8):
			t1 = mult(x1,key[x][0])
			t2 = add(x2,key[x][1])
			t3 = add(x3,key[x][2])
			t4 = mult(x4,key[x][3])
			t5 = t1^t3
			t6 = t2^t4
			t7 = mult(t5,key[x][4])
			t8 = add(t6,t7)
			t9 = mult(t8,key[x][5])
			t10 = add(t7,t9)
			if makefile == 'y':
				file.write('\nRound ' + str(x + 1) + '\n\tt1 = ' + makehex(t1) + ' = ' + makehex(x1) + ' * ' + makehex(key[x][0]) + '\n\tt2 = ' + makehex(t2) + ' = ' + makehex(x2) + ' + ' + makehex(key[x][1]) + '\n\tt3 = ' + makehex(t3) + ' = ' + makehex(x3) + ' + ' + makehex(key[x][2]) + '\n\tt4 = ' + makehex(t4) + ' = ' + makehex(x4) + ' * ' + makehex(key[x][3]) + '\n\tt5 = ' + makehex(t5) + ' = ' + makehex(t1) + ' ^ ' + makehex(t3) + '\n\tt6 = ' + makehex(t6) + ' = ' + makehex(t2) + ' ^ ' + makehex(t4) + '\n\tt7 = ' + makehex(t7) + ' = ' + makehex(t5) + ' * ' + makehex(key[x][4]) + '\n\tt8 = ' + makehex(t8) + ' = ' + makehex(t6) + ' + ' + makehex(t7) + '\n\tt9 = ' + makehex(t9) + ' = ' + makehex(t8) + ' * ' + makehex(key[x][5]) + '\n\tta = ' + makehex(t10) + ' = ' + makehex(t7) + ' + ' + makehex(t9) + '\n')
			x1 = t1^t9
			x2 = t3^t9
			x3 = t2^t10
			x4 = t4^t10
			if makefile == 'y':
				file.write('\n	x1 = ' + makehex(x1) + ' = ' + makehex(t1) + ' ^ ' + makehex(t9) + '\n	x2 = ' + makehex(x2) + ' = ' + makehex(t3) + ' ^ ' + makehex(t9) + '\n	x3 = ' + makehex(x3) + ' = ' + makehex(t2) + ' ^ ' + makehex(t10)+ '\n	x4 = ' + makehex(x4) + ' = ' + makehex(t4) + ' ^ ' + makehex(t10) + '\n')
		temp = x2
		x2 = x3
		x3 = temp
		x1 = mult(x1,key[8][0])
		x2 = add(x2,key[8][1])
		x3 = add(x3,key[8][2])
		x4 = mult(x4,key[8][3])
		temp = makehex(x1)+makehex(x2)+makehex(x3)+makehex(x4)
		if makefile == 'y':
				file.write('\n\nOutput:' + temp)
		ctext += temp
	if makefile == 'y':
		file.write('\n\nFinal Output: ' + ctext)
	return ctext

if __name__=="__main__":

        #data = '05320a6414c819fa'
        #data = '65be87e7a2538aed'
        data = '6565784FDE123476'
        key  = '006400c8012c019001f4025802bc0320'

        print(IDEA(data, key, 'e'))

