#!/usr/bin/python3
## Author:	Owen Cocjin
## Version:	1.3
## Date:	08/02/20
## Notes:
##	- Fixed import of progMenu

from progMenu.progMenu import menu, vprint, printFAA
from cryptoPack import *
from cryptoPack.crypto_entries import *
PARSER=menu.parse(True)
vprint.setVerbose(menu.findFlag(['v', "verbose"]))

def main():
	vprint(PARSER)
	printFAA()
	decrypt=bool(PARSER["decrypt"])
	mode=PARSER["mode"]
	word=PARSER["word"]
	key=PARSER["key"]
	if PARSER["generate"] and key:  #Generate keys if g flas and keys not empty
		print(PARSER["generate"](key))
		exit()
	if not mode or not word or not key:  #Print help if any of key, mode, or word are missing
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
		print(RSAcrypto(word, key, decrypt))
	else:  #Print help if invalid mode passed
		hFunc()

if __name__=="__main__":
	#main()
	try:
		main()
	except Exception as e:
		print(f"[|X: crypto:__main__]:{type(e).__name__}: {str(e).strip(chr(34))}")
