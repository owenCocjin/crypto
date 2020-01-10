#!/usr/bin/python3

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
