## Author:	Owen Cocjin
## Version:	1.1
## Date:	16/01/20
## Notes:
##	- Moved patdown to crypto_misc
##	- Added RSAcrypto

from .crypto_funcs import feea, et, ea
from .crypto_misc import patdown, keyz26, isPrime
from progMenu import vprint

class Crypt():
	def __init__(self, name, word, key, d=None, letters=None):
		self.name=name
		self.word=word
		self.key=key
		self.converted=""
		self.d=d
		self.cryMode="E" if not d else "D"
		#letters are more for future uses. Somewhat useless now :(
		self.letters=[chr(i+97) for i in range(26)] if letters==None else letters

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

class ShiftCipher(Crypt):
	def __init__(self, word='', key=None):
		Crypt.__init__(self, "Shift Cipher", word, key)
		self.encry()

	def encry(self):
		'''f(M)=(M+b)mod26'''
		self.converted=''.join([self.letters[(self.letters.index(c)+self.key)%26] for c in self.word])
		return self.converted

class AffineCipher(Crypt):
	def __init__(self, word='', key=None, dFlag=False):
		Crypt.__init__(self, "Affine Cipher", word, key, dFlag)
		self.encry() if not dFlag else self.decry()

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
	def __init__(self, word='', key=None, dFlag=False):
		Crypt.__init__(self, "Vigenere Cipher", word, key, dFlag)
		self.encry() if not dFlag else self.decry()

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
		Crypt.__init__(self, "Transposition Cipher", word, key)
		self.encry()

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

class RSAcrypto(Crypt):
	'''Takes a word or list of ints as word, and e/d and n as key.
Decryption MUST be list of ints (given by encryption)'''
	def __init__(self, word='', key=None, decrypt=None):
		Crypt.__init__(self, "RSA", word, key, decrypt)
		self.letters=['']+self.letters
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
		temp=[ord(i)-96 for i in self.word] if type(self.word)==str else self.word

		for m in temp:
			vprint(f"{m}: {self.letters[(m)%27]}={m**self.e%self.n}")
			self.converted.append(m**self.e%self.n)

		vprint(self.converted)
		self.converted=','.join([str(i) for i in self.converted]) if 'E'==self.cryMode else self.converted
		return self.converted

	def decry(self):
		'''Pretty much encrypts, but returns a string instead of an int list'''
		self.encry()
		self.converted=''.join([self.letters[i%27] for i in self.converted])
		return self.converted

	def generate(self):
		'''Generated a private/public keypair given p & q. Return e, d, n'''
		if not isPrime(self.key[0])[0]*isPrime(self.key[1])[0]:
			print("[|X: crypto_classes:RSAcrypto:generate]: Invalid keys (both p and q MUST be prime)!")
			exit()
		self.n=self.key[0]*self.key[1]
		totient=et(self.n)
		#Get e (second largest coprime between n and et(n). If largest, e and d will always be the same)
		for i in reversed(et(totient[0])[1][:-1]):
			if i in totient[1]:
				self.e=i
				break

		#Get d
		counter=2
		while True:
			if self.e*counter%totient[0]==1:
				self.d=counter
				break
			counter+=1

		return self.e, self.d, self.n


#-------------#
#    NOTES    #
#-------------#
'''
Template Crypto class:

class ClassName(Crypt):
	def __init__(self, word='', key=None, d=False):
		Crypt.__init__(self, "NAMEHERE", patdown(word), key)
		self.cryMode="E" if not d else "D"
		self.encry() if not d else self.decry()

	def __str__(self):
		l1=f"\033[32mMODE: \033[0m{self.name}"
		l2=f"\033[33mKEY:  \033[0m{self.key}"
		l3=f"{self.word} -> {self.converted}"
		return f"{l1}\n{l2}\n{l3}\n"

	def encry(self):
		PUT ENCRYPTION ALGO HERE!

	def decry(self):
		PUT DECRYPTION ALGO HERE (if any)!
'''
if __name__=="__main__":
	pass
