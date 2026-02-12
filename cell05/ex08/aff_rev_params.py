#!/usr/bin/env python3
import sys
if len(sys.argv) < 2:
    print("none")
else:
    params = sys.argv[1:]
    
    for param in reversed(params):
        print(param)