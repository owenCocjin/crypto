## Author:	Owen Cocjin
## Version:	1.12
## Date:	16/01/20
## Notes:
##	- Updated Terms to allow blank Terms initialization (makes a '0' term)
##	- Added patdown

from . import *
import math
#---------------#
#    CLASSES    #
#---------------#
class Polynomial():
	def __init__(self, *term):
		self.terms=list(term)
		self.iterC=0

	def __str__(self):
		return '('+' + '.join([f"({i.getPackage()})" for i in self.terms]).strip(' + ')+')'

	def __iter__(self):
		return self

	def __next__(self):
		if self.iterC<len(self.terms):
			toRet=self.terms[self.iterC]
			self.iterC+=1
		else:
			raise StopIteration
		return toRet

	def __add__(self, other):
		'''Returns a Polynomial with added terms'''
		try:
			if type(other) not in [Polynomial, Term]:
				raise ValueError(f"Can't add Polynomial to type {type(other)}!")
		except ValueError as e:
			print(f"[|X: Polynomial]: {e}")
			return self

		tempTerms=[i for i in self.terms]
		if type(other)==Term:
			tempTerms.append(other)
		elif type(other)==Polynomial:
			[tempTerms.append(i) for i in other.getTerms()]

		return Polynomial(*tempTerms).clean()

	def __sub__(self, other):
		'''Subtracts other from self by inverting all term signs in other, then adding'''
		tempTerms=other.getTerms()
		tempTerms=[i*-1 for i in tempTerms]
		toRet=self+Polynomial(*tempTerms)
		return Polynomial(*toRet)

	def __mul__(self, other):
		'''Returns a Polynomial with multiplied terms'''
		other=Polynomial(other) if type(other)==Term else other
		tempTerms=[]
		for i in self.terms:
			[tempTerms.append(i*j) for j in other.getTerms()]
		return Polynomial(*tempTerms).clean()

	def __pow__(self, n):
		'''Multiplies itself n times. Returns a Polynomial'''
		origPoly=Polynomial(*self.terms)
		tempPoly=origPoly
		for i in range(n-1):
			tempPoly=origPoly*tempPoly
		return tempPoly.clean()

	def maxDegree(self):
		'''Returns the highest degree'''
		m=0
		for i in self.terms:
			if i.getDegree()>m:
				m=i.getDegree()
		return m

	def clean(self):
		'''Removes "0" terms and adds like terms'''
		#Combine all like terms
		endTerms=[Term(f"0x^{i}") for i in range(self.maxDegree()+1)]  #Make a list of empty Terms with all degrees from 0->degree of polynomial
		for i in self.terms:
			endTerms[i.getDegree()]+=i

		#Remove "0" terms
		c=0
		while c<len(endTerms):
			if endTerms[c].getCoeff()==0:
				endTerms=endTerms[:c]+endTerms[c+1:]
				c-=1
			c+=1
		self.terms=endTerms
		return self

	def setTerms(self, new):
		self.terms=new
	def getTerms(self):
		return self.terms

class Term():
	'''Define a term for a polynomial'''
	def __init__(self, t="0"):
		t=str(t)  #Make t a string
		#Try to figure out passed string "t"
		try:
			self.x=t.find('x')  #Find x, if it exists
			self.c=t.find('^')  #Find ^, if it exists

			#Set coefficient and degree depending on if x and ^ were found
			self.coeff=int(t[:self.x]) if self.x>0 else 1
			self.degree=int(t[self.c+1:]) if self.c>-1 else 1

			#Assume entire t is coefficient if x and ^ weren't found
			if self.x==self.c==-1:
				self.coeff=int(t)
				self.degree=0

			#Errors for certain conditions
			elif self.degree<0:
				raise ValueError(f"Invalid term passed: {self.coeff}x^{self.degree} (degree must be >=0. Setting to 0)!")
				self.degree=0
			elif self.x!=len(t)-1 and self.c==-1:
				raise ValueError(f"Invalid term passed: {self.coeff}x^{self.degree} (invalid degree declaration. Setting to 0)!")
				self.degree=0
			elif self.c>0 and self.x==-1:
				raise ValueError(f"Invalid term passed: {self.coeff}x^{self.degree} (invalid coefficient declatration. Setting to 1)!")
				self.coeff=1
		except ValueError as e:
			print(f"[|X: Term]: {e}")
			return
			#exit(1)

	def __str__(self):
		'''Returns (BLANK) if either coeff or degree are None (this is probably due to an incorrect term being set)'''
		t=f"x^{self.degree}" if self.degree>0 and self.coeff!=0 else ''
		return f"({self.coeff}{t})"

	def __add__(self, other):
		'''Adds if degree the same. Returns a Term object'''
		if self.degree==other.getDegree():
			return Term(f"{self.coeff+other.getCoeff()}x^{self.degree}")
		else:
			return False

	def __sub__(self, other):
		'''Subtracts if degree the same. Returns a Term object'''
		if self.degree==other.getDegree():
			return Term(f"{self.coeff-other.getCoeff()}x^{self.degree}")

	def __mul__(self, other):
		'''Multiply terms'''
		other=Term(str(other)) if type(other)==int else other
		return Term(f"{self.coeff*other.getCoeff()}x^{self.degree+other.getDegree()}")

	def __eq__(self, other):
		return (self.coeff, self.degree)==(other.getCoeff(), other.getDegree())

	def stats(self):
		'''Prints __dict__, but a little prettier than just calling __dict__'''
		return self.__dict__

	def setCoeff(self, new):
		self.coeff=new
	def getCoeff(self):
		return self.coeff

	def setDegree(self, new):
		'''Degree can't be negative'''
		self.degree=int(new) if new>=0 else None
	def getDegree(self):
		return self.degree

	def getPackage(self):
		'''Returns self as a string (can be used as input for another Term)'''
		t=f"x^{self.degree}" if self.degree>0 and self.coeff!=0 else ''
		return f"{self.coeff}{t}"


#-----------------#
#    FUNCTIONS    #
#-----------------#
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
