import random
from ip import *

def main():
    for i in range(100):
        x = random.randrange(0,2**64)
        b = "{:64b}".format(x)
        #print(b)
        c = IP(b)
        #print(c)
        d = IPinv(c)
        #print(d)
        
        if(b != d):
            print("\n[!] Error:",b,d)
        else:
            print("=",end="")
        
    print("\n[*] No Error!")
    
if __name__ == '__main__':
    main()
