## Author:	Owen Cocjin
## Version:	1.3.1
## Date:	31/01/20
## Notes:
##	- Added division to Term and Polynomial
##	- Added TermError class for general errors with Terms
##	- Moved _clean() to Polynomial.__init__ so all Polynomials are formatted the same
##	- Added __gt__, __lt__, __ge__, __le__ to Term
##	- Fixed error with iterating through Polynomials (didn't reser internal counter)
##	- Added fme() (fast modular exponentiation)
##	- Added subtraction of Polynomials
##	- Added subscripting of Polynomials
##	- Added division of Polynomials

from . import *
import math
#---------------#
#    CLASSES    #
#---------------#
class Polynomial():
	def __init__(self, *term):  #term is a tuple
		'''Tries to turn whatever is passed into a Term, fails otherwise (creates a Term(0)).
Always auto cleans when initialized ( see help(Polynomial.clean()) )'''
		try:
			term=[Term(0)] if len(term)==0 else term  #Nothing was passed
			self.terms=[Term(i) if type(i)!=Term else i for i in term]
			self._clean()
		except Exception as e:
			print(f"[|X: Polynomial:__init__]: Invalid term: {e}!")
			self.terms=[Term(0)]
			return
		self.degree=self.maxDegree()
		self._iterC=0

	def __str__(self):
		return '('+' + '.join([f"({i.getPackage()})" for i in self.terms]).strip(' + ')+')'

	def __repr__(self):
		return str(self)

	def __len__(self):
		return len(self.terms)

	def __iter__(self):
		self._iterC=0
		return self

	def __next__(self):
		if self._iterC<len(self.terms):
			toRet=self.terms[self._iterC]
			self._iterC+=1
		else:
			raise StopIteration
		return toRet

	def __getitem__(self, i):
		if type(i)==slice:
			start=0 if not i.start else i.start
			stop=len(self) if not i.stop else i.stop
			step=1 if not i.step else i.step
			return Polynomial(*self.terms[start:stop:step])
		else:
			return self.terms[i]

	def __add__(self, other):
		'''Returns a Polynomial with added terms'''
		try:
			if type(other) not in [Polynomial, Term]:
				raise ValueError(f"Can't add Polynomial to type {type(other)}!")
		except ValueError as e:
			print(f"[|X: Polynomial:__add__]: {e}")
			return self

		tempTerms=[i for i in self.terms]
		if type(other)==Term:
			tempTerms.append(other)
		elif type(other)==Polynomial:
			[tempTerms.append(i) for i in other.getTerms()]

		return Polynomial(*tempTerms)

	def __sub__(self, other):
		if type(other)==list:
			other=Polynomial(*other)
		elif type(other)==Polynomial:
			pass
		else:
			other=Polynomial(other)

		maxDegree=self.degree if self.degree>other.getDegree() else other.getDegree()
		sTerms=Polynomial(*self.terms)
		oTerms=Polynomial(*other.getTerms())
		for i in range(maxDegree+1):
			sTerms+=Term(f"0x^{i}")
			oTerms+=Term(f"0x^{i}")
		return Polynomial(*[sTerms[i]-oTerms[i] for i in range(len(sTerms))]).deepclean()

	def __mul__(self, other):
		'''Returns a Polynomial with multiplied terms'''
		other=Polynomial(other) if type(other)==Term else Polynomial(other)
		tempTerms=[]
		for i in self.terms:
			[tempTerms.append(i*j) for j in other.getTerms()]
		return Polynomial(*tempTerms)

	def __truediv__(self, other):
		'''Returns a tuple of Polynomials (result, remainder) of divided terms'''
		other=Polynomial(other) if type(other) in [Term, int] else other
		maxDegree=self.degree if self.degree>other.getDegree() else other.getDegree()
		toRet=[]
		oTerms=Polynomial(*other.getTerms())

		#Fill missing terms
		remainder=self+Polynomial(*[Term(f"0x^{i}") for i in range(maxDegree+1)])

		#Actual calc
		for i in range(len(remainder)-1):
			toRet.append(remainder[0]/oTerms[0])  #Divide sTerms[0] by oTerms[0] and add result to toRet
			remainder-=oTerms*toRet[-1]  #Multiply divisor by recent answer, and subtract from remainder

		return Polynomial(*toRet).deepclean(), Polynomial(*remainder).deepclean()

	def __pow__(self, n):
		'''Multiplies itself n times. Returns a Polynomial'''
		origPoly=Polynomial(*self.terms)
		tempPoly=origPoly
		for i in range(n-1):
			tempPoly=origPoly*tempPoly
		return tempPoly

	def __neg__(self):
		return self*-1

	def _clean(self, deepclean=False):
		'''Removes "0" terms if deepclean==True and adds like terms'''
		self.terms.sort(reverse=True)
		#Combine all like terms
		cur=self.terms[0]
		toRet=[]
		for i in self.terms[1:]:
			if i.degree==cur.degree:  #Add to cur if same degree
				cur+=i
			else:  #Save cur to toRet list
				toRet.append(cur)
				cur=i
		toRet.append(cur)  #Add the final Term

		#Remove "0" terms if deepclean is True
		if deepclean==True:
			c=0
			while c<len(toRet):
				if toRet[c].getCoeff()==0:
					toRet=toRet[:c]+toRet[c+1:]
					c-=1
				c+=1
		self.terms=toRet
		self.terms.sort(reverse=True)
		return self

	def deepclean(self):
		'''Just clean but removes "0" Terms'''
		self._clean(deepclean=True)
		return self

	def maxDegree(self):
		'''Returns the highest degree'''
		m=0
		for i in self.terms:
			m=i.getDegree() if i.getDegree()>m else m
		return m

	def setTerms(self, new):
		self.terms=new
	def getTerms(self):
		return self.terms
	def setDegree(self, new):
		self.degree=new
	def getDegree(self):
		return self.degree

class Term():
	'''Define a term for a polynomial'''
	def __init__(self, t="0"):
		t=str(t)  #Make t a string
		self.coeff=self.degree=0
		#Try to figure out passed string "t"
		try:
			x=t.find('x')  #Find x, if it exists
			c=t.find('^')  #Find ^, if it exists

			#Set coefficient and degree depending on if x and ^ were found
			self.coeff=int(t[:x]) if x>0 else 1
			self.degree=int(t[c+1:]) if c>-1 else 1

			#Assume entire t is coefficient if x and ^ weren't found
			if x==c==-1:
				self.coeff=int(t)
				self.degree=0

			#Errors for certain conditions
			elif x==-1 and c>=0:  #Missing x, which is never going to be a valid Term
				raise CoeffError(f"Invalid coefficient declaration: {t} (missing x)!")
				self.coeff=1
			elif self.degree<0:
				raise DegreeError(f"Invalid degree passed: {self.coeff}x^{self.degree} (degree must be >=0)!")
				self.degree=0
			elif x!=len(t)-1 and c==-1:
				raise DegreeError(f"Invalid degree passed: {self.coeff}x^{self.degree} (invalid degree declaration)!")
				self.degree=0
			elif c>0 and x==-1:
				raise CoeffError(f"Invalid coefficient passed: {self.coeff}x^{self.degree} (invalid coefficient declaration)!")
				self.coeff=1

		except DegreeError as e:
			print(f"[|X: Term:__init__]: {e}")
		except CoeffError as e:
			print(f"[|X: Term:__init__]: {e}")
		except Exception as e:
			print(f"[|x: Term:__init__]: Invalid term passed: {t} ({e})!")
			self.coeff=self.degree=0

	def __str__(self):
		'''Returns a formatted term'''
		t=f"x^{self.degree}" if self.degree>0 else ''
		return f"({self.coeff}{t})"

	def __repr__(self):
		return str(self)

	def __add__(self, other):
		'''Adds if degree the same. Returns a Term object'''
		if self.degree==other.getDegree():
			return Term(f"{self.coeff+other.getCoeff()}x^{self.degree}")
		else:
			return None

	def __sub__(self, other):
		'''Subtracts if degree the same. Returns a Term object'''
		if self.degree==other.getDegree():
			return Term(f"{self.coeff-other.getCoeff()}x^{self.degree}")

	def __mul__(self, other):
		'''Multiply terms'''
		if type(other)==Polynomial:
			return other*self
		other=Term(str(other)) if type(other)==int else other
		return Term(f"{self.coeff*other.getCoeff()}x^{self.degree+other.getDegree()}")

	def __truediv__(self, other):
		'''Divide only if my local coeff is divisible by other's coeff'''
		other=Term(str(other)) if type(other)==int else other
		#Handle zero division
		if self.coeff==0:  #If this term is a filler, return the negative of other
			return Term(f"{other.getCoeff()*-1}x^{other.getDegree()}")
		elif other.getCoeff()==0:  #If other is a filler, return self
			return self

		#Error handling
		try:
			if divmod(self.coeff, other.getCoeff())[1]!=0:
				raise ValueError(f"Self's coeff ({self.coeff}) isn't divisible by other's coeff ({other.getCoeff()})!")
			elif other.getDegree()>self.degree:
				raise ValueError(f"Other's degree ({other.getDegree()}) can't be greater than mine ({self.degree})!")
		except ValueError as e:
			print(f"[|X: Term:__truediv__]: {e}")
			return None
		return Term(f"{self.coeff//other.getCoeff()}x^{self.degree-other.getDegree()}")

	def __neg__(self):
		return self*-1

	def __eq__(self, other):
		return (self.coeff, self.degree)==(other.getCoeff(), other.getDegree())

	def __gt__(self, other):
		return True if self.degree>other.getDegree() or self.coeff>other.getCoeff() and self.degree==other.getDegree() else False

	def __lt__(self, other):
		return True if self.degree<other.getDegree() or self.coeff<other.getCoeff() and self.degree==other.getDegree() else False

	def __ge__(self, other):
		return True if self.degree>=other.getDegree() or self.coeff>=other.getCoeff() and self.degree==other.getDegree() else False

	def __le__(self, other):
		return True if self.degree<=other.getDegree() or self.coeff<=other.getCoeff() and self.degree==other.getDegree() else False

	def stats(self):
		'''Returns __dict__, but a little prettier than just calling __dict__'''
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
		return str(self).strip("()")


#-----------------#
#    FUNCTIONS    #
#-----------------#
def fme(b, e, n):
	'''Fast Modular Exponentiation.
b=Base
e=Exponent
n=Mod'''
	toRet=1
	for t in [b**(2**i)%n for i, j in enumerate(bin(e)[:1:-1]) if j=='1']:
		toRet*=t
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
