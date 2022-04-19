import sys
sys.path.insert(1,'./rsa')
sys.path.insert(1,'./des')

import number_theory
import rsa
import des
import random

def test():
    key = random.randrange(0,2**64)
    IV  = random.randrange(0,2**64)
    s   = "HELLO WORLD\n\rARE YOU OK?\nHEY IM GONNA BE DEAD BUT THIS MESSAGE IS ENCRYOTED\n SO NOONE CAN SEE THIS!! HEHEHEHE"

    print("[*] Sending the following message: ",s)
    print("[*] Generating the keys")
    
    [(n,e),(d,p,q)] = rsa.generate_keys1024()
    c = rsa.encrypt(key,n,e)
    m = rsa.decrypt(c,n,d)
    print("[*] Key Exchange Success?: ",key==m)    

    key = "{:064b}".format(key)
    IV = "{:064b}".format(IV)
    e = des.enc(s,key,IV)
    d = des.dec(e,key,IV)        
    print("[*] DES encryption and decryption Success?: ",s == d)

    
def main():
    test()
    
if __name__ == '__main__':
    main()
