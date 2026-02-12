#!/usr/bin/env python3
import sys
param = sys.argv[1:]
if param == 0:
    print("none")
else:
    for p in param:
        if not p.endswith("ism"):
            print(p + "ism")