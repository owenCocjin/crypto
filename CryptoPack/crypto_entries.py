from progMenu import menu, MenuEntry

#-------------#
#    FUNCS    #
#-------------#
def dFunc():
	return True

def hFunc():
	print('''\033[33mUsage:\033[0m crypto --mode=<m> --word=<w> --key=<k> [-dhkmw] [OPTIONS]
\tA compilation of ciphers and crypto algos!
\033[33mArguments:\033[0m
\t-d, --decrypt\tDecrypt instead of encrypt (default)
\t-h, --help\tPrints this page
\t-k, --key\tSets key based on mode. Takes from stdin if no arg
\t-m, --mode\tSets encryption mode:
\t\t\t\t- 0/shift: Shift Cipher
\t\t\t\t- 1/affine: Affine Cipher
\t\t\t\t- 2/vige: Vigenere Cipher
\t\t\t\t- 3/trans: Transposition Cipher\n
\t-w, --word\tSets the plaintext word. Takes from stdin if no arg
''')
	exit(0)
	return True

def kFunc(k=None):
	'''Sets the key based on the mode'''
	k=input("Key: ") if not k else k
	mode=menu.sgetAssigned(['m', "mode"])
	#Try splitting into ints and stripping
	try:
		k=[int(i.strip()) for i in k.split(',')]
	except:
		print("[|X: kFunc:KeyError]: Invalid key!")
		exit()

	if mode in ['0', "shift"]:  #Single key
		return k[0]

	elif mode in ['1', "affine"]:  #Double key
		if len(k)<2:
			print("[|X: kFunc:KeyError]: Invalid key (2 required)!")
			exit()
		else:
			return k[:2]

	elif mode in ['3', "transpo"]:  #Keys in a set (0..len(key))
		for i in k:
			if len(k)<i or i<0 or k.count(i)!=1:
				print(f"[|X: kFunc:KeyError]: Invalid key!")
				exit()
			else:
				return k
	else:
		return k

def mFunc(m):
	return m.lower()

def wFunc(w=None):
	return w if w else input("Word: ")

#---------------#
#    ENTRIES    #
#---------------#
dEntry=MenuEntry("decrypt", ['d', "decrypt"], dFunc, 0)
hEntry=MenuEntry("help", ['h', "help"], hFunc, 0)
kEntry=MenuEntry("key", ['k', "key"], kFunc, 3)
mEntry=MenuEntry("mode", ['m', "mode"], mFunc, 1)
wEntry=MenuEntry("word", ['w', "word"], wFunc, 3)
