#!/usr/bin/env python3
import sys
import re
params = sys.argv[1:]
if len(params) != 2:
    print("none")
else:
    keyword = params[0]
    text = params[1]
    ans = re.findall(keyword, text)

    if len(ans) == 0:
        print("none")
    else:
        print(len(ans))