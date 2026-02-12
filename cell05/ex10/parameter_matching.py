#!/usr/bin/env python3
import sys
if len(sys.argv) != 2:
    print("none")
else:
    param = sys.argv[1]
    uinput = input("What was the parameter? ")
    if uinput == param:
        print("Good job!")
    else:
        print("Nope, sorry...")