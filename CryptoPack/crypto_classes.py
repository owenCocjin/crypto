## Author:	Owen Cocjin
## Version:	1.0
## Date:	10/01/20
## Notes:

from cryptoPack.crypto_funcs import feea

class Crypt():
	def __init__(self, name, word, key, letters=None):
		self.name=name
		self.word=word
		self.key=key
		self.converted=""
		#letters are more for future uses. Somewhat useless now :(
		self.letters=[chr(i+97) for i in range(26)] if letters==None else letters

	def __str__(self):
		return f"{self.name}\n{self.word} | {self.key}"

	def patdown(self, word=None):
		'''Removes non-alpha chars and makes all chars lowercase (because most of these ciphers only work on lowercase charset)'''
		return ''.join([c.lower() if 0<=ord(c)-65<=25 or 0<=ord(c)-97<=25 else '' for c in (word if word else self.word)])

	def encry(self):
		'''Encrypt word with key'''
		self.converted="DEFAULT ENCRYPT"
		return self.converted

	def decry(self):
		'''Decrypt word with key'''
		self.converted="DEFAULT DECRYPT"
		return self.converted

	def setName(self, new):
		self.name=new
	def getName(self):
		return self.name

	def setWord(self, new):
		self.name=new
	def getName(self):
		return self.name

	def setKey(self, new):
		self.key=new
	def getKey(self):
		return self.key

	def setConverted(self, new):
		self.converted=new
	def getConverted(self):
		return self.converted


#----------------------#
#    CRYPTO CLASSES    #
#----------------------#

class ShiftCipher(Crypt):
	def __init__(self, word='', key=None):
		Crypt.__init__(self, "Shift Cipher", self.patdown(word), key)
		self.encry()

	def __str__(self):
		l1=f"\033[32mMODE: \033[0m{self.name}"
		l2=f"\033[33mKEY:  \033[0m{self.key}"
		l3=f"{self.word} -> {self.converted}"
		return f"{l1}\n{l2}\n{l3}\n"

	def encry(self):
		'''f(M)=(M+b)mod26'''
		self.converted=''.join([self.letters[(self.letters.index(c)+self.key)%26] for c in self.word])
		return self.converted

class AffineCipher(Crypt):
	def __init__(self, word='', key=None, d=False):
		Crypt.__init__(self, "Affine Cipher", self.patdown(word), key)
		self.encry() if not d else self.decry()
		self.cryMode="E" if not d else "D"

	def __str__(self):
		l1=f"\033[32mMODE: \033[0m{self.name} ({self.cryMode})"
		l2=f"\033[33mKEY:  \033[0ma={self.key[0]} | b={self.key[1]}"
		l3=f"{self.word} -> {self.converted}"
		return f"{l1}\n{l2}\n{l3}\n"

	def encry(self):
		'''f(M)=(aM+b)mod26'''
		self.converted=''.join([self.letters[(self.key[0]*(ord(c)-97)+self.key[1])%26] for c in self.word])
		return self.converted

	def decry(self):
		'''f(M)=inverse(a)(C-b)mod26'''
		inverse=feea(26, self.key[0])[1]
		self.converted=''.join([self.letters[inverse*((ord(c)-97)-self.key[1])%26] for c in self.word])
		return self.converted

class VigenereCipher(Crypt):
	def __init__(self, word='', key=None, d=False):
		Crypt.__init__(self, "Vigenere Cipher", self.patdown(word), key)
		self.cryMode="E" if not d else "D"
		self.encry() if not d else self.decry()

	def __str__(self):
		l1=f"\033[32mMODE: \033[0m{self.name} ({self.cryMode})"
		l2=f"\033[33mKEY:  \033[0m{self.key}"
		l3=f"{self.word} -> {self.converted}"
		return f"{l1}\n{l2}\n{l3}\n"

	def encry(self):
		'''f(M)=(M+k)mod26'''
		self.converted=''
		for i, c in enumerate(self.word):
			self.converted+=self.letters[((ord(c)-97)+self.key[i%len(self.key)])%26]
		return self.converted

	def decry(self):
		'''f(M)=(M-k)mod26'''
		self.converted=''
		for i, c in enumerate(self.word):
			self.converted+=self.letters[((ord(c)-97)-self.key[i%len(self.key)])%26]
		return self.converted

class TranspoCipher(Crypt):
	def __init__(self, word='', key=None):
		Crypt.__init__(self, "Transposition Cipher", self.patdown(word), key)
		self.encry()

	def __str__(self):
		l1=f"\033[32mMODE: \033[0m{self.name}"
		l2=f"\033[33mKEY:  \033[0m{self.key}"
		l3=f"{self.word} -> {self.converted}"
		return f"{l1}\n{l2}\n{l3}\n"

	def encry(self):
		'''Uses the key as a permutation, mutates the word by blocks'''
		self.converted=''

		#Set the proper length of the word (multiple of len(key))
		modded=len(self.word)%len(self.key)
		self.word+='_'*(len(self.key)-modded) if modded!=0 else ''

		#Mutate thhe word given the key (permutation)
		for i in range(len(self.word)//len(self.key)):
			self.converted+=f"{''.join([self.word[i*len(self.key)+c-1] for c in self.key])} "

		return self.converted

#------------#
#    MISC    #
#------------#

class Term():
	'''Define a term for a polynomial'''
	def __init__(self, t):
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


if __name__=="__main__":
	p=5
	p1=Polynomial(*[Term(i) for i in ["x", "-1"]])
	p1=p1**p
	print(f"p1: {p1}")
	p2=Polynomial(*[Term(i) for i in [f"x^{p}", "-1"]])
	print(f"p2: {p2}")
	rec=p1-p2
	for i in rec:
		print(f"{i.getCoeff()}%{p}->{i.getCoeff()%p}")
	print(rec)
