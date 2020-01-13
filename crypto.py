#!/usr/bin/python3
## Author:	Owen Cocjin
## Version:	1.0
## Date:	10/01/20
## Notes:

from progMenu import menu, vprint, printFAA
from cryptoPack import *
from cryptoPack.crypto_entries import *
PARSER=menu.parse(True)
vprint.setVerbose(menu.findFlag(['v', "verbose"]))

def main():
	vprint(PARSER)
	if not PARSER["mode"] or not PARSER["word"] or not PARSER["key"]:
		hFunc()

	if PARSER["mode"] in ['0', "shift"]:
		print(ShiftCipher(PARSER["word"], PARSER["key"]))

	elif PARSER["mode"] in ['1', "affine"]:
		print(AffineCipher(PARSER["word"], PARSER["key"], PARSER["decrypt"]))

	else:
		hFunc()

if __name__=="__main__":
	main()
