#!/usr/bin/python3
## Author:	Owen Cocjin
## Version:	1.1
## Date:	15/01/20
## Notes:
##	- Added transpo, vigenere

from progMenu import menu, vprint, printFAA
from cryptoPack import *
from cryptoPack.crypto_entries import *
PARSER=menu.parse(True)
vprint.setVerbose(menu.findFlag(['v', "verbose"]))

def main():
	vprint(PARSER)
	decrypt=bool(PARSER["decrypt"])
	mode=PARSER["mode"]
	word=PARSER["word"]
	key=PARSER["key"]
	if not mode or not key:  #Print help if any of key, mode, or word are missing
		if PARSER["generate"]:
			pass
		else:
			hFunc()

	if mode in ['0', "shift"]:
		print(ShiftCipher(word, key))
	elif mode in ['1', "affine"]:
		print(AffineCipher(word, key, decrypt))
	elif mode in ['2', "transpo"]:
		print(TranspoCipher(word, key))
	elif mode in ['3', "vigenere"]:
		print(VigenereCipher(word, key, decrypt))
	elif mode in ['4', "rsa"]:
		if PARSER["generate"]:
			print(RSAcrypto('', key).generate())
		else:
			print(RSAcrypto(word, key, decrypt))
	else:  #Print help if invalid mode passed
		hFunc()

if __name__=="__main__":
	main()
