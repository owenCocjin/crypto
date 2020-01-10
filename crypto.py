#!/usr/bin/python3
## Author:	Owen Cocjin
## Version:	1.0
## Date:	10/01/20
## Notes:

from progMenu import menu, vprint, printFAA
from CryptoPack import *
from CryptoPack.crypto_entries import *
PARSER=menu.parse(True)
vprint.setVerbse=(menu.findFlag(['v', "verbose"]))

def main():
	if not PARSER["mode"] or not PARSER["word"] or not PARSER["key"]:
		hFunc()

	if PARSER["mode"] in ['0', "shift"]:
		shifted=ShiftCipher(PARSER["word"], PARSER["key"])
		print(shifted)

if __name__=="__main__":
	main()
