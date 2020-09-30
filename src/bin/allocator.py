import os
os.chdir(os.path.join(os.getcwd(), "MV2"))
import allocator
import time
import argparse


if __name__=="__main__":
    a = allocator.Allocator()
    while True:
        time.sleep(1)
