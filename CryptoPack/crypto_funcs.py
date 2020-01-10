#!/usr/bin/python3
## Author:	Owen Cocjin
## Version:	0.1
## Date:	09/01/20
## Notes:

def ea(a, b, log=-1):
	'''Euclidean Algorithm'''
	#Remainder
	r=a%b
	#Multiple   4178,
	m=int(a/b)
	#Save variables to log if required
	if type(log)==list:
		log.append([a, b, m, r])
	#Recursive if r!=0. Return A list with something (last log is discarded as it isn't used)
	return ea(b, r, log) if r!=0 else (b, log)

def et(r, flsh=False):
	'''Euler's totient. Returns the number of coprime ints to n and a list of them'''
	toRet=[]
	for i in range(r):
		if ea(i, r)[0]==1:
			print(i) if flsh else False  #Prints as numbers are generated. Useful for larger numbers
			toRet.append(i)
	return len(toRet), toRet

def feea(a, b, *, prnt=False, s=False):
	'''Fast Extended Euclidean Algorithm. Returns the gcd and inverse(b mod a). When s==True, assumes the greater number is mod, otherwise "a" is mod'''
	if s:  #Swaps if s==True. Mainly used if user input is not guaranteed correct
		a, b=(b, a) if a<b else (a, b)  #Swap if a smaller than b
	r=[a, b]
	s=[1, 0]
	t=[0, 1]

	#Keep calculating as long as the remainder isn't 1 or 0 (0 meaning there is no modular inverse)
	while r[-1]>1:
		s.append(s[-2]-r[-2]//r[-1]*s[-1])
		t.append(t[-2]-r[-2]//r[-1]*t[-1])
		r.append(r[-2]%r[-1])
	if prnt:
		print("r\ts\tt")
		[print(f"{a}\t{b}\t{c}") for a, b, c in zip(r, s, t)]
	return (r[-1], t[-1] if t[-1]>=0 else t[-1]%a) if r[-1]==1 else (t[-2], t[-2])  #Handles non-coprime pairs. Handles negative inverses (by modding them with whatever it thinks is the mod)

def flt(a, p, prnt=False):
	'''Fermat's Little Theorum'''
	toRet=a**(p-2)
	if prnt:
		print(f"{toRet:,}")
	return toRet


#------------#
#    MISC    #
#------------#
def keyz26(key):
	'''Turns a string into a list of ints'''
	return [(ord(c)-97) for c in key]


#-------------#
#    NOTES    #
#-------------#
'''
Calculate # of private keys {a, b} for a given Affine cipher:
	- et of whatever's modded * whatever's modded
	- et(n)*n
'''

if __name__=="__main__":
	aGCD, aLog=ea(7, 3, [])
	bGCD, bLog=ea(26, 15, [])
	cGCD, cLog=ea(1180, 482, [])

	#print(f"7, 3:\t\t{aGCD} | {aLog}")
	#print(f"\t\t{eea(1, 1, 1, aLog)}")

	#print(f"15, 5:\t\t{bGCD} | {bLog}")
	#print(f"\t\t{eea(1, 1, 1, bLog)}")

	print(f"26, 15:\t\t{bGCD} | {bLog}")
	print(f"\t\t{feea(26, 15)}")

	print(f"1180, 482:\t{cGCD} | {cLog}")
	print(f"\t\t{feea(1180, 482)}")
