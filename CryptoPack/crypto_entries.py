## Author:	Owen Cocjin
## Version:	1.1
## Date:	16/01/20
## Notes:
##	- Added 'generate' flag to generate keypairs (when applicable)

from progMenu import menu, MenuEntry
from .crypto_misc import keyz26, patdown
from .crypto_funcs import rsaGen

#-------------#
#    FUNCS    #
#-------------#
def dFunc():
	return True

def gFunc():
	mode=menu.sgetAssigned(['m', "mode"])
	if mode in ['4', "rsa"]:
		return rsaGen

	return False

def hFunc():
	print('''\033[33mUsage:\033[0m crypto --mode=<m> --word=<w> --key=<k> [-dhkmw] [OPTIONS]
\tA compilation of ciphers and crypto algos!
\033[33mArguments:\033[0m
\t-d, --decrypt\tDecrypt instead of encrypt (default)
\t-g, --generate\tGenerate keypairs (if applicable)
\t-h, --help\tPrints this page
\t-k, --key=<k>\tSets key based on mode. Takes from stdin if no arg
\t-m, --mode=<m>\tSets encryption mode:
\t\t\t\t- 0/shift: Shift Cipher
\t\t\t\t- 1/affine: Affine Cipher
\t\t\t\t- 2/vigenere: Vigenere Cipher
\t\t\t\t- 3/transpo: Transposition Cipher
\t\t\t\t- 4/rsa: RSA\n
\t-w, --word=<w>\tSets the plaintext word. Takes from stdin if no arg
''')
	exit(0)
	return True

def kFunc(k=None):
	'''Sets the key based on the mode'''
	k=input("Key: ") if not k else k
	mode=menu.sgetAssigned(['m', "mode"]).lower()
	#Try splitting into ints and stripping
	try:
		if k=='':
			raise Exception
		k=[int(i.strip()) for i in k.split(',')]
	except ValueError:
		#Turn into ints if string passed
		k=keyz26(k)
	except:
		print("[|X: kFunc:KeyError]: Invalid key!")
		exit()

	if mode in ['0', "shift"]:  #Single key
		return k[0]

	elif mode in ['1', '2', "affine", "rsa"]:  #Double key
		if len(k)<2:
			print("[|X: kFunc:KeyError]: Invalid key (2 required)!")
			exit()
		else:
			return k[:2]

	elif mode in ['2', "transpo"]:  #Keys in a set (0..len(key))
		for i in k:
			if len(k)<i or i<0 or k.count(i)!=1:
				print(f"[|X: kFunc:KeyError]: Invalid key!")
				exit()
		return k

	else:
		return k

def mFunc(m):
	return m.lower()

def wFunc(w=None):
	w=w if w else input("Word: ")
	try:  #List of ints
		return [int(i.strip()) for i in w.split(',')]
	except Exception as e:  #String
		print(e)
		return patdown(w)

#---------------#
#    ENTRIES    #
#---------------#
dEntry=MenuEntry("decrypt", ['d', "decrypt"], dFunc, 0)
gEntry=MenuEntry("generate", ['g', "generate"], gFunc, 0)
hEntry=MenuEntry("help", ['h', "help"], hFunc, 0)
kEntry=MenuEntry("key", ['k', "key"], kFunc, 3)
mEntry=MenuEntry("mode", ['m', "mode"], mFunc, 1)
wEntry=MenuEntry("word", ['w', "word"], wFunc, 3)
