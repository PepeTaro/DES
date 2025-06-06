from key import *
from ip import *
from f import *
from math import log2,ceil

def split64to32(bits64):
    assert(len(bits64) == 64)
    l  = bits64[0:32]
    r  = bits64[32:64]
    return (l,r)

def concatenate32to64(l,r):
    assert(len(l) == 32)
    assert(len(r) == 32)
    result = l + r        
    return result

def enc_cbc(m,key,IV):
    """
    CBC(Cipher Block Chaining)モードを使用して暗号化。
    IVは、Initialization Vectorを意味する。
    """
    assert(len(key) == 64)
    assert(len(IV) == 64)

    n = len(m)
    result = ""
    
    y = des_enc(xor_str(m[0:64],IV),key)
    result += y
    m = m[64:]
    
    while(len(m) != 0):
        y = des_enc(xor_str(m[0:64],y),key)
        result += y
        m = m[64:]
    return result

def dec_cbc(m,key,IV):
    assert(len(key) == 64)
    assert(len(IV) == 64)
    
    n = len(m)
    i = 0
    result = ""
    
    x = xor_str(des_dec(m[0:64],key),IV)
    result += x
    prev = m[0:64]
    m = m[64:]
    
    while(len(m) != 0):
        x = xor_str(des_dec(m[0:64],key),prev)
        result += x
        prev = m[0:64]
        m = m[64:]
    return result

def des_enc(x,key):
    assert(len(x) == 64)
    assert(len(key) == 64)    
    subkeys = enc_key_schedule(key)        # 暗号化用Key Scheduleからsubkeyを取得。
    x = IP(x)                              # インプットであるxを置換する。
    (l,r) = split64to32(x)                 # xを64bitsから32bitsに分離(上位32bitsをl、下位32bitsをrとしている)。
    for i in range(16):                    # 16は16ラウンドを意味する。
        tmp = xor_str(f(r,subkeys[i]),l)   # Forループは以下の演算をしている: L_{i} = R_{i-1},R_{i} = L_{i-1} ^ f(R_{i-1},k_{i})
        l = r                              #  ここで、^はXOR、L_{i},R_{i},k_{i}はそれぞれ
        r = tmp                            #  iラウンド目のL,R,subkey kを表している。fはf-function。
        
    y = IPinv(concatenate32to64(r,l)) # 最後に2つの32bitsから64bitsに戻し、IPの逆関数であるIPinvを適用。
    return y

def des_dec(y,key):
    assert(len(y) == 64)
    assert(len(key) == 64)
    subkeys = dec_key_schedule(key) # 復号化用Key Scheduleからsubkeyを取得。 
    y = IP(y)                       # 以下のコードはenc関数とまったく同じ。
    (l,r) = split64to32(y)     # (Feistel Networkだから)
    for i in range(16):
        tmp = xor_str(f(r,subkeys[i]),l)
        l = r
        r = tmp
        
    x = IPinv(concatenate32to64(r,l))
    return x

def enc(plaintext,key,IV):
    y = ascii_encode(plaintext) # 平文をエンコード。
    # CBCモードを使用して暗号化。
    cipher = enc_cbc(y,key,IV)
    return cipher

def dec(ciphertext,key,IV):
    x = dec_cbc(ciphertext,key,IV) # 暗号文を復号化。
    plaintext = ascii_decode(x)    # その結果をデコード。
    return plaintext

def ascii_encode(plaintext):
    y = ""
    # 文字列を二進法文字列に変換。
    for c in plaintext:
        y += "{:08b}".format(ord(c))

    # HACK: yの長さが64の倍数となるように先頭に"0"をパディング。
    pad_len = 64 - len(y)%64
    y = "0"*pad_len + y
    
    return y

def ascii_decode(ciphertext):
    d = ""
    for i in range(len(ciphertext)//8):
        # ciphertextを８文字(8bit)ずつに分割して、ASCIIに戻す。
        n = int(ciphertext[8*i:8*(i+1)],2)
        if(n == 0): continue # 先頭にあるパディング部分は無視する。
        d += chr(n)          #  (8つの0単位でパディングしていることに注意) 

    return d
