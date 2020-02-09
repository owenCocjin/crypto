## Author:	Owen Cocjin
## Version:	1.5
## Date:	08/02/20
## Notes:
##	- Migrated all of crypto_misc over here
##	- Added dlp()
##	- Added key_parse

from . import *
from progMenu import vprint
import math, time, re

#-----------------#
#    FUNCTIONS    #
#-----------------#
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

def fme(b, e, n, *, prnt=False):
	'''Fast Modular Exponentiation.
b=Base
e=Exponent
n=Mod'''
	toRet=1
	prnt=bool(prnt)
	binary=bin(e)
	for i, j in enumerate(binary[:1:-1]):
		print(f"{binary[2:-i-1]}\033[33m{j}\033[32m{binary[len(binary)-i:]}\033[0m\t({i}/{len(binary)-2})"*prnt, end='', flush=True)
		if j=='1':
			toRet*=b**(2**i)%n
		print(f"\033[1000D"*prnt, end='', flush=True)
	print(f"\033[32m{binary[2:]}\033[0m\t({i+1}/{len(binary)-2})"*prnt)
	return toRet%n

def isPrime(p, l=False):
	'''Return True if n is prime. If l==True, compute long way (x-1)^P-(x^p-1), but is 100% accurate'''
	if l:
		p1=Polynomial(Term("x"), Term("-1"))**p
		p2=Polynomial(Term(f"x^{p}"), Term(f"-1"))
		for i in p1-p2:
			if i.getCoeff()%p!=0:
				return False, -1
		return True, 1
	else:
		for i in range(2, (math.ceil(math.sqrt(p)) if p>5 else p)):
			if p%i==0:
				return False, i
		return True, 1

def key_parse(keys, *, no=0, delim=',', rules=None):
	'''Returns individual keys (keys=# of keys needed) as a list of ints, with optional specific rules (rules being a space seperated string):
co:\tKeys must be co-prime to each other (all of them!)
max:\tKeys can't be greater than arg 'max'
min:\tKeys can't be smaller than arg 'min'
pos:\tKeys must all be positive
set:\tKeys are part of a set (ints 1-n) and can't repeat
str:\tIndicates key is a lowercase-chars string. Convert to ints from range 0-25:a-z
strict:\tMust have exactly "no" number of keys
Arguments for certain rules can be passed through 'args' in the format: rule:arg (space seperated).
If rules are broken, RuleError is thrown with the broken rule (KINDA MESSED UP RN!).
Returns a single string 'x' if an error is thrown cuz i can't figure out a better way right now!'''
	#Split rules by space
	splitRules=rules.split() if rules else ''
	#Turn rules into a dictionary in format: key:value
	dictRules={}
	for i in splitRules:
		try:
			curValue, curKey=i.split(':')
		except ValueError:
			curValue=i
			curKey=None
		dictRules[curValue]=curKey

	#Convert keys into an int list
	if type(keys)==int or type(keys)==float:
		keys=[int(keys)]
	elif "str" in dictRules:
		keys=[ord(i)-97 for i in keys]
	else:
		keys=[int(i) for i in keys.split(delim)]

	#Rule checking
	if "co" in dictRules:
		for i, k1 in enumerate(keys):
			for k2 in keys[i+1:]:
				if ea(k1, k2)[0]!=1:
					raise RuleError(f"co ({k1}:{k2})")
	if "max" in dictRules:
		for i in keys:
			if i>int(dictRules["max"]): raise RuleError(f"max ({i})")
	if "min" in dictRules:
		for i in keys:
			if i<int(dictRules["min"]): raise RuleError(f"min ({i})")
	if "pos" in dictRules:
		for i in keys:
			if i<0:	raise RuleError(f"pos ({i})")
	if "set" in dictRules:
		for i in keys:
			if len(keys)<i or i<0 or keys.count(i)!=1: raise RuleError(f"set: ({i})")
	if "strict" in dictRules:
		if len(keys)!=no: raise RuleError(f"strict: (No. of keys!={no})")

	return keys[:no] if 0<no<len(keys) else keys
	#[|X: crypto_funcs:key_parse]:

def keyz26(key):
	'''Turns a string into a list of ints'''
	return [(ord(c)-97) for c in key]

def patdown(word):
	'''Removes non-alpha chars and makes all chars lowercase (because most of these ciphers only work on lowercase charset)'''
	return ''.join([c.lower() if 0<=ord(c)-65<=25 or 0<=ord(c)-97<=25 else '' for c in word])

def primeFactors(p):
	#!!!UNDER CONSTRUCTION!!!#
	'''Returns a list of primes, representing the prime factorization of p'''
	primes=[i for i in range(p) if isPrime(i+1)]
	return primes


#------------------#
#    GENERATION    #
#------------------#
def diffieHellman(key):
	'''Key is in format: p, g'''
	key=key_parse(key, no=2, rules="strict")
	p=key[0]
	g=key[1]
	a=int(input("Enter secret power: "))
	aKey=g**a%p
	print(f"Send this to other: \033[1m{aKey}\033[0m")
	bKey=int(input("Enter b: "))
	s=bKey**a%p
	return {'a':a, 'aKey':aKey, 's':s}

def dlp(key, tableName="table.txt", tableGen=True):
	'''Discrete Log Problem.
Returns x for a=g^x(mod n)'''
	#!!!UNDER CONSTRUCTION!!!#
	a, g, n=key_parse(key, no=3, rules="strict")
	table=[]
	m=math.ceil(math.sqrt(n-1))
	vprint(f"a: {a}")
	vprint(f"g: {g}")
	vprint(f"m: {m}")
	vprint(f"n: {n}")

	if tableGen:
		#Generate table
		vprint("Generating table... [     ]  ", end='')
		pastLen=0
		with open(tableName, "w+") as f:
			for i in range(m):
				f.write(f"{i}:{g**i%n}\n")
				toPrint=f"\033[{pastLen-5}D{int((i+1)/m*100)}% ({i+1}/{m})"
				pastLen=len(toPrint)
				vprint(toPrint, end='', flush=True)
				#time.sleep(0.1)
		vprint(f"\033[{pastLen+3}D\033[32mDone!\033[0m")

	#import table
	vprint("Importing table... ", end='')
	with open(tableName, 'r') as f:
		for l in f:
			table.append(int(l[:-1].split(':')[1]))
	vprint("Done!")

	#Find xb and xg
	c=feea(n, g**m)[1]
	vprint(f"c: {c}")
	for i in range(m):
		cur=a*c**i%n
		vprint(f"\033[1000DSearching for {cur} ({i})...", end='')
		if cur in table:
			xg=table.index(cur)
			xb=i
			vprint(f"\nFound! Xb: {xb}\tXg: {xg}")
			break

	x=xb*m+xg  #This is the solution
	vprint(f"x: {x}")
	vprint("Confirming x...")
	conf=fme(g, x, n, prnt=True)
	vprint(f"\n{conf} {'!' if conf!=a else '='}= {a}")
	return x

def rsaGen(key):
	'''Generated an RSA private/public keypair given p & q.
Return e, d, n as a dict (mostly for clarity).
NOTE: will ask for e which must be any int 1<e<phi(n). The program will choose the next valid e, if invalid.'''
	key=key_parse(key, no=2, rules="strict pos prime")
	if not isPrime(key[0])[0]*isPrime(key[1])[0]:
		raise KeyError(f"Invalid keys ({key[0] if not isPrime(key[0])[0] else key[1]} isn't prime)!")
	n=key[0]*key[1]
	e=d=0
	tot=(key[0]-1)*(key[1]-1)

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


#------------------#
#    EXCEPTIONS    #
#------------------#
class DegreeError(Exception):
	'''Raised when an invalid degree is passed'''
	pass

class CoeffError(Exception):
	'''Raised when an invalid coefficient is passed'''
	pass

class TermError(Exception):
	'''Raised for a general Term error'''
	pass

class RangeError(Exception):
	'''Raised if an invalid range string was passed to Letters'''
	pass

class RuleError(Exception):
	'''Raised when a rule was broken'''
	def __init__(self, rule):
		Exception.__init__(self, rule)

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
