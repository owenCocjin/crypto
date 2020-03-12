## Author:	Owen Cocjin
## Version:	1.2
## Date:	12/03/20
## Notes:
##	- Fixed import of progMenu

from progMenu.progMenu import menu, MenuEntry, vprint
from .crypto_funcs import diffieHellman, ea, key_parse, keyz26, patdown, rsaGen
from .crypto_errors import RuleError

#-------------#
#    FUNCS    #
#-------------#
def dFunc():
	return True

def gFunc():
	mode=menu.sgetAssigned(['m', "mode"])
	if mode in ['4', "rsa"]:
		return rsaGen
	if mode in ['5', "difhel"]:
		return diffieHellman
	if mode in ['6', 'dlp']:
		return dlp

	return False

def hFunc():
	print('''\033[33mUsage:\033[0m crypto --mode=<m> --word=<w> --key=<k> [-dhkmw] [OPTIONS]
\tA compilation of ciphers and crypto algos!
\033[33mArguments:\033[0m
\t-d, --decrypt\tDecrypt instead of encrypt (default)
\t-g, --generate\tGenerate keys (if applicable)
\t-h, --help\tPrints this page
\t-k, --key=<k>\tSets key based on mode. Takes from stdin if no arg
\t-m, --mode=<m>\tSets encryption mode:
\t\t\t\t- 0/shift: Shift Cipher
\t\t\t\t- 1/affine: Affine Cipher
\t\t\t\t- 2/transpo: Transposition Cipher
\t\t\t\t- 3/vigenere: Vigenere Cipher
\t\t\t\t- 4/rsa: RSA
\t\t\t\t- 5/difhel: Diffie-Hellman (Requires -g flag)
\t\t\t\t- 6/dlp: Discrete Log Problem (Requires -g flag)\n
\t-w, --word=<w>\tSets the plaintext word. Takes from stdin if no arg
''')
	exit(0)
	return True

def kFunc(k=None):
	'''Sets the key based on the mode'''
	k=input("Key: ") if not k else k
	return k

def mFunc(m):
	return m.lower()

def wFunc(w=None):
	w=w if w else input("Word: ")
	try:  #List of ints
		return [int(i.strip()) for i in w.split(',')]
	except Exception as e:  #String
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
