# Crypto

> A compilation library/script for all cryptography concepts and algos learned as part of the ISS program.
> **Note:** This script has been tested and is intended for use in Bash. The specific area of concern is in the console printing; Script prints in colour using ANSI escape chars. Some terminals might not support these, but Bash does.

## Installation

- Clone this repo. **Note:** this repo uses a submodule, meaning in addition to cloning, you must initialize the submodule. Here are some options to doing this:
	+ Clone using `git clone --recurse-submodules https://...`
	+ Initialize after cloning: `git submodule update --init --recursive`

- Run script (in path):
```
./crypto.py -h  #Shows help menu
```

~~OR~~

- ~~Copy the *CryptoPack* folder to your python path. Your python path can be found by printing it using sys:~~
> ~~The convention is to put public repositories in `/usr/lib/pythonX.X/dist-packages`. If you don't have the *dist-package* folder, you can realistically put it anywhere else in the path, but I would suggest `/usr/lib/pythonX.X/site-packages`, which is the default PIP directory.~~
> ~~NOTE: If copying into path, make sure you install ```progMenu``` to the path as well, as some~~
```
$ python -c 'import sys; print(sys.path)'
['', '/usr/lib/python3.7', '/other/paths']
```

<br/>

## Usage

- If running script, use `./crypto.py -h` to show all commands.
- ~~If installed as a library (moved *CryptoPack* to python path), use as any other library:~~

```
from CryptoPack import feea  #Fast Euclidean Algo
print(feea)
```
