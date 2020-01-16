#!/usr/bin/python3
## Author:	Owen Cocjin
## Version:	1.11
## Date:	16/01/20
## Notes:
##	- Updated flt()

from .crypto_misc import isPrime

def ea(a, b, log=-1):
	'''Euclidean Algorithm.
Returns gcd(a, b) and the log of all iterations (-1 if no list was passed)'''
	#Remainder
	r=a%b
	#Multiple
	m=int(a/b)
	#Save variables to log if required
	if type(log)==list:
		log.append([a, b, m, r])
	#Recursive if r!=0. Return A list with something (last log is discarded as it isn't used)
	return ea(b, r, log) if r!=0 else (b, log)

def et(r, prnt=False):
	'''Euler's totient.
Returns the number of coprime ints to n and a list of them'''
	toRet=[]
	for i in range(r):
		if ea(i, r)[0]==1:
			print(i) if prnt else False  #Prints as numbers are generated. Useful for larger numbers
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
	'''Fermat's Little Theorum. Returns the flt%p and boolean if p is prime.
If p is prime, for all int(a): a^p-a%p=0. Subjective to Carmichael Numbers (try 561 (3*11*17))'''
	toRet=a**p-a
	if prnt:
		print(f"{toRet:,}")
	return toRet%p, True if toRet%p==0 else False


#------------------#
#    GENERATION    #
#------------------#
def rsaGen(key):
	'''Generated an RSA private/public keypair given p & q. Return e, d, n'''

	if not isPrime(key[0])[0]*isPrime(key[1])[0]:
		print("[|X: crypto_classes:RSAcrypto:generate]: Invalid keys (both p and q MUST be prime)!")
		exit()
	n=key[0]*key[1]
	totient=et(n)
	#Get e (second largest coprime between n and et(n). If largest, e and d will always be the same)
	for i in reversed(et(totient[0])[1][:-1]):
		if i in totient[1]:
			e=i
			break

	#Get d
	counter=2
	while True:
		if e*counter%totient[0]==1:
			d=counter
			break
		counter+=1

	return {'e':e, 'd':d, 'n':n}


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
