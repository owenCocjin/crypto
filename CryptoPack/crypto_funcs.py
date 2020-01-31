## Author:	Owen Cocjin
## Version:	1.3.1
## Date:	31/01/20
## Notes:
##	- Added Diffie-Hellman keygen

from progMenu import vprint
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
	'''Fast Extended Euclidean Algorithm.
Returns the gcd and inverse(b mod a).
When s==True, assumes the greater number is mod, otherwise "a" is mod.
If a and b are not co-prime, will return gdc and -1'''
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
	return (r[-1], t[-1] if t[-1]>=0 else t[-1]%a) if r[-1]==1 else (r[-2], -1)  #Handles non-coprime pairs. Handles negative inverses (by modding them with whatever it thinks is the mod)

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
	'''Generated an RSA private/public keypair given p & q.
Return e, d, n as a dict (mostly for clarity).
NOTE: will ask for e which must be any int 1<e<phi(n). The program will choose the next valid e, if invalid.'''
	if not isPrime(key[0])[0]*isPrime(key[1])[0] or key[0]<1 or key[1]<1:
		if key[0]<1 or key[1]<1:
			print("[|X: crypto_classes:RSAcrypto:generate]: Invalid keys (both p and q must be > 1)!")
		else:
			print("[|X: crypto_classes:RSAcrypto:generate]: Invalid keys (both p and q MUST be prime)!")
		exit()
	vprint("Passed primality test!")
	n=key[0]*key[1]
	e=d=0
	vprint("Generating phi(n)...", end=' ')
	tot=(key[0]-1)*(key[1]-1)
	vprint("Done!")

	#Get e from user. If e isn't coprime, will count upwards (up to phi(n))
	try:
		e=int(input(f"Enter e (must be <{tot}): "))
		if e>=tot:
			raise Exception
		if ea(e, n)!=1 or ea(e, tot)!=1:
			while e<tot:
				e+=1
				if ea(e, n)[0]==1 and ea(e, tot)[0]==1:
					break
	except Exception:
		print(f"Invalid e entered (e can't be greater than {tot})!")
		exit()
	except:
		print("INVALID!")
		exit()

	d=feea(tot, e)[1]

	return {'e':e, 'd':d, 'n':n}

def diffieHellman(key):
	'''Key is in format: p, g'''
	p=key[0]
	g=key[1]
	a=int(input("Enter secret power: "))
	aKey=g**a%p
	print(f"Send this to other: \033[1m{aKey}\033[0m")
	bKey=int(input("Enter b: "))
	s=bKey**a%p
	return {'a':a, 'aKey':aKey, 's':s}

#-------------#
#    NOTES    #
#-------------#
'''
Calculate # of private keys {a, b} for a given Affine cipher:
	- et of whatever's modded * whatever's modded
	- et(n)*n

11, 17 (64): 42
11, 19 (48): 34
13, 19 (72): 57
17, 19 (96): 56
19, 23 (120): 96
37, 23 (240): 96
29, 37 (288): 171
'''
