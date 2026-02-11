#!/usr/bin/env python3
print("Enter a number less than 25")
num = int(input())
if num > 25:
    print("Error")
else:
    while num <= 25:
        print(f"Inside the loop, my variable is {num}")
        num += 1