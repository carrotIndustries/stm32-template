#!/usr/bin/python3
import hashlib
import struct
import sys
if len(sys.argv) < 4 :
	print("wrong invocation")
	exit(1)
prefixlen = int(sys.argv[3], 0)

with open(sys.argv[1], "rb") as infile :
	fw=infile.read()
	with open(sys.argv[2], "wb") as outfile :
		if prefixlen > 0 :
			ha=hashlib.md5(fw).digest()
			le=len(fw)
			prefix=struct.pack("<I16s", le, ha).ljust(prefixlen, b"\0")
			outfile.write(prefix)
		outfile.write(fw)

