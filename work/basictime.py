# import csv

p = "./work/STFILE.CSV"
with open(p, "r", encoding="ms932", errors="", newline="") as f:
    s = f.read()

print(s[:100])