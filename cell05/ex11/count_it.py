#!/usr/bin/env python3
import sys
parems = sys.argv[1:]
if len(parems) == 0:
    print("0")
else:
    print(f"parameters: {len(parems)}")
    for p in parems:
        print(f"{p}: {len(p)}")