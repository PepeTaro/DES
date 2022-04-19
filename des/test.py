import random
from des import *

def test5(s):
    key = "{:064b}".format(random.randrange(0,2**64))
    IV = "{:064b}".format(random.randrange(0,2**64))
    cipher = enc(s,key,IV)
    plain  = dec(cipher,key,IV)

    if(s == plain):
        print("Sucess")
        return True
    else:
        print("[!] ERROR!!")
        return False


def test4(s):
    key = "{:064b}".format(random.randrange(0,2**64))
    IV = "{:064b}".format(random.randrange(0,2**64))    
    m = ""
    for c in s:
        m += "{:08b}".format(ord(c))
        
    pad_len = 64 - len(m)%64
    m = "0"*pad_len + m    
    
    cipher = enc_cbc(m,key,IV)
    
    plain = dec_cbc(cipher,key,IV)
    
    d = ""
    for i in range(len(plain)//8):
        n = int(plain[8*i:8*(i+1)],2)
        if(n == 0): continue
        d += chr(n)

    if(m == plain and s == d):
        print("Sucess")
        return True
    else:
        print("[!] ERROR!!")
        return False
    
def test3():
    key = "{:064b}".format(random.randrange(0,2**64))
    IV = "{:064b}".format(random.randrange(0,2**64))
    s   = "HELLO WORLD\n\rARE YOU OK?\nHEY IM GONNA BE DEAD BUT THIS MESSAGE IS ENCRYOTED\n SO NOONE CAN SEE THIS!! HEHEHEHE"
    #s = "HELLOWOL\n"
    print("plain text: ",s)

    m = ""
    for c in s:
        m += "{:08b}".format(ord(c))
        
    pad_len = 64 - len(m)%64
    m = "0"*pad_len + m    
    print(pad_len,len(m)%64)
    
    cipher = enc_cbc(m,key,IV)
    #print(cipher)
    
    plain = dec_cbc(cipher,key,IV)
    d = ""
    for i in range(len(plain)//8):
        n = int(plain[8*i:8*(i+1)],2)
        if(n == 0): continue
        d += chr(n)

    print("decrypted text: ",d)
    
    #print(m,"\n\n",plain,"\n\n",len(m),len(plain))
    print("Success? : ",m == plain)

    #print(len(s),len(d))
    print("Success? : ",s == d)
    
def test2():
    s = "abcdefgh"
    bits64 = ascii_to_bits64(s)
    
    key = Block(64,random.randrange(0,2**64))
    print("Key: ",key)
    x = Block(64,bits64)
    print("Plain text: ",x)
    y = enc(x,key)
    print("enc text: ",y)
    z = dec(y,key)
    print("dec text: ",z)

    print("Are enc and dec equal: ",x == z)

    print(bits64_to_ascii(z))    
    
def test():
    key = "{:064b}".format(random.randrange(0,2**64))
    print("Key: ",key)
    x = "{:064b}".format(random.randrange(0,2**64))
    print("Plain text: ",x)
    y = des_enc(x,key)
    print("enc text: ",y)
    z = des_dec(y,key)
    print("dec text: ",z)
    
    print("Are enc and dec equal: ",x == z)    

def main():
    #test()
    #test2()
    #test3()

    l = ["message","","fuckyou","HELLOWORLD ARE \n\r YOU OK????","HELLOW ROLD ARE YOU OK BITCH????"]
    
    for s in l:
        #m = test4(s)
        m = test5(s)
        if(not m):
            return    
    
if __name__ == '__main__':
    main()
