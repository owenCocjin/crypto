## Author:	Owen Cocjin
## Version:	1.2
## Date:	08/02/20
## Notes:
##	- Migrated crypto_misc classes over here
##	- Made each class handle their own keys (each class now utilizes key_parse with it's own specific rules!)

from .crypto_funcs import et, ea, feea, fme, isPrime, key_parse, keyz26, patdown

class Crypt():
	def __init__(self, name, word, key, d=None, letters=None):
		self.name=name
		self.word=word
		self.key=key
		self.converted=""
		self.d=d
		self.cryMode="E" if not d else "D"
		#letters are more for future uses. Somewhat useless now :(
		self.letters=[chr(i) for i in range(97, 123)] if letters==None else letters

	def __str__(self):
		l1=f"\033[32mMODE: \033[0m{self.name}"+f" ({self.cryMode})"*(True if self.d!=None else False)
		l2=f"\033[33mKEY:  \033[0m{self.key}"
		l3=f"{self.word} -> {self.converted}"
		return f"{l1}\n{l2}\n{l3}\n"

	def encry(self):
		'''Encrypt word with key and set self.converted to result'''
		self.converted="DEFAULT ENCRYPT"
		return self.converted

	def decry(self):
		'''Decrypt word with key and set self.converted to result'''
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
class AffineCipher(Crypt):
	'''Encrypts each letter (see encry) with key: [a, b], where a'''
	def __init__(self, word='', key=None, dFlag=False):
		key=key_parse(key, no=2)
		Crypt.__init__(self, "Affine Cipher", word, key, dFlag)
		self.encry() if not dFlag else self.decry()

	def __str__(self):
		l1=f"\033[32mMODE: \033[0m{self.name} ({self.cryMode})"
		l2=f"\033[33mKEY:  \033[0ma={self.key[0]} | b={self.key[1]}"
		l3=f"{self.word} -> {self.converted}"
		return f"{l1}\n{l2}\n{l3}\n"

	def encry(self):
		'''f(M)=(aM+b)mod26'''
		self.converted=''.join([self.letters[(self.key[0]*(self.letters.index(c))+self.key[1])%len(self.letters)] for c in self.word])
		return self.converted

	def decry(self):
		'''f(M)=inverse(a)(C-b)mod26'''
		inverse=feea(26, self.key[0])[1]
		self.converted=''.join([self.letters[inverse*((self.letters.index(c))-self.key[1])%len(self.letters)] for c in self.word])
		return self.converted

class RSAcrypto(Crypt):
	'''Takes a word or list of ints as word, and e/d and n as key.
Decryption MUST be list of ints (given by encryption)'''
	def __init__(self, word='', key=None, decrypt=None):
		key=key_parse(key, no=2, rules="strict pos")
		Crypt.__init__(self, "RSA", word, key, decrypt)
		self.letters=['', '']+[chr(i) for i in range(97, 123)]
		self.e=key[0]
		self.n=key[1]
		self.encry() if not decrypt else self.decry()

	def __str__(self):
		l1=f"\033[32mMODE: \033[0m{self.name} ({self.cryMode})"
		l2=f"\033[33mKEY:  \033[0me={self.e} | n={self.n}"
		l3=f"\033[33mKEY:  \033[0md={self.e} | n={self.n}"
		l4=f"{self.word} -> {self.converted}"
		return f"{l1}\n{l3 if 'D'==self.cryMode else l2}\n{l4}\n"

	def encry(self):
		'''m^e(mod n)'''
		self.converted=[]

		#Convert string to list of ints
		temp=[self.letters.index(i) for i in self.word] if type(self.word)==str else self.word
		for m in temp:
			#print(f"{m}: {self.letters[(m)%len(self.letters)]}={m**self.e%self.n}")
			self.converted.append(fme(m, self.e, self.n))#(m**self.e%self.n)

		#print(self.converted)
		self.converted=','.join([str(i) for i in self.converted]) if 'E'==self.cryMode else self.converted
		return self.converted

	def decry(self):
		'''Pretty much encrypts, but returns a string instead of an int list'''
		self.encry()
		self.converted=''.join([self.letters[i%len(self.letters)] for i in self.converted])
		return self.converted

class ShiftCipher(Crypt):
	'''Shifts each character by [key] characters'''
	def __init__(self, word='', key=None):
		key=key_parse(key, no=1)
		Crypt.__init__(self, "Shift Cipher", word, key[0])
		print(f"SHIFT CIPHER KEY: {key}")
		self.encry()

	def encry(self):
		'''f(M)=(M+b)mod26'''
		self.converted=''.join([self.letters[(self.letters.index(c)+self.key)%len(self.letters)] for c in self.word])
		return self.converted

class TranspoCipher(Crypt):
	'''Permutes a string with [key], where [key] is a set of ints'''
	def __init__(self, word='', key=None):
		key=key_parse(key, rules="set")
		Crypt.__init__(self, "Transposition Cipher", word, key)
		self.encry()

	def encry(self):
		'''Uses the key as a permutation, mutates the word by blocks'''
		self.converted=''

		#Set the proper length of the word (multiple of len(key))
		modded=len(self.word)%len(self.key)
		self.word+='_'*(len(self.key)-modded) if modded!=0 else ''

		#Mutate the word given the key (permutation)
		for i in range(len(self.word)//len(self.key)):
			for c in self.key:
				self.converted+=self.word[i*len(self.key)+c-1]

		return self.converted

class VigenereCipher(Crypt):
	'''Encrypts plaintext by applying the Shift cipher to each char, where the key is a string'''
	def __init__(self, word='', key=None, dFlag=False):
		try:
			key=key_parse(key, rules="pos")
		except:
			#Assume keys are comma-seperated ints
			key=key_parse(key, rules="str pos")
		Crypt.__init__(self, "Vigenere Cipher", word, key, dFlag)
		self.encry() if not dFlag else self.decry()

	def encry(self):
		'''f(M)=(M+k)mod26'''
		self.converted=''
		for i, c in enumerate(self.word):
			self.converted+=self.letters[(self.letters.index(c)+self.key[i%len(self.key)])%26]
		return self.converted

	def decry(self):
		'''f(M)=(M-k)mod26'''
		self.converted=''
		for i, c in enumerate(self.word):
			self.converted+=self.letters[(self.letters.index(c)-self.key[i%len(self.key)])%26]
		return self.converted


#--------------------#
#    MATH CLASSES    #
#--------------------#
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


#-------------#
#    NOTES    #
#-------------#
'''
Template Crypto class:

class ClassName(Crypt):
	def __init__(self, word='', key=None, d=False):
		Crypt.__init__(self, "NAMEHERE", patdown(word), key)
		self.cryMode="E" if not d else "D"
		self.encry() if not d else self.decry()  #Remove everything after self.encry() if no decryption function

	def __str__(self):
		l1=f"\033[32mMODE: \033[0m{self.name}"
		l2=f"\033[33mKEY:  \033[0m{self.key}"
		ln=f"{self.word} -> {self.converted}"
		return f"{l1}\n{l2}\n{ln}\n"

	def encry(self):
		#PUT ENCRYPTION ALGO HERE!
		pass

	def decry(self):  #Remove if no decryption function
		#PUT DECRYPTION ALGO HERE (if any)!
		pass
'''
if __name__=="__main__":
	pass
