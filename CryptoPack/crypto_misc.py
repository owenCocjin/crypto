## Author:	Owen Cocjin
## Version:	1.0
## Date:	14/01/20
## Notes:

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
		[print(i) for i in tempTerms]
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

#-----------------#
#    FUNCTIONS    #
#-----------------#
def keyz26(key):
	'''Turns a string into a list of ints'''
	return [(ord(c)-97) for c in key]
