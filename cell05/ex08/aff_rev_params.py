#!/usr/bin/env python3
import sys
if len(sys.argv) < 2:
    print("none")
else:
    # slice เอาตั้งแต่ตัวที่ 1 ไปจนจบ (ตัดชื่อไฟล์ทิ้ง)
    params = sys.argv[1:]
    
    # ใช้ฟังก์ชัน reversed() เพื่อกลับด้าน List
    for param in reversed(params):
        print(param)