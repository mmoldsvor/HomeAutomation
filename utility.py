import logging

class LogHandler:
    def __init__(self):
        pass

i = 5
for x in range(i):
    for y in range(x+1):
        print("*", end="")
    print()