from misc import *

PC1_table = [
    57,49,41,33,25,17,9,1,
    58,50,42,34,26,18,10,2,
    59,51,43,35,27,19,11,3,
    60,52,44,36,63,55,47,39,
    31,23,15,7,62,54,46,38,
    30,22,14,6,61,53,45,37,
    29,21,13,5,28,20,12,4
]

PC2_table = [
    14,17,11,24,1,5,3,28,
    15,6,21,10,23,19,12,4,
    26,8,16,7,27,20,13,2,
    41,52,31,37,47,55,30,40,
    51,45,33,48,44,49,39,56,
    34,53,46,42,50,36,29,32
]

def PC1(bits64):
    assert(len(bits64) == 64)
    result = ""
    for i in range(56):
        result += bits64[PC1_table[i]-1]
    return result

def PC2(bits56):
    assert(len(bits56) == 56)
    result = ""
    for i in range(48):
        result += bits56[PC2_table[i]-1]
    return result

def split56to28(bits56):
    assert(len(bits56) == 56)
    c = bits56[0:28]
    d = bits56[28:56]        
    return (c,d)

def concatenate28to56(c,d):
    assert(len(c) == 28)
    assert(len(d) == 28)
    result = c+d        
    return result

def enc_key_schedule(key):
    subkeys = []
    pc1 = PC1(key)
    (c,d) = split56to28(pc1)

    for i in range(16):
        if(i == 0 or i == 1 or i == 8 or i == 15):
            c = rot_left(c,1)
            d = rot_left(d,1)            
        else:
            c = rot_left(c,2)
            d = rot_left(d,2)

        subkey = PC2(concatenate28to56(c,d))
        subkeys.append(subkey)
        
    return subkeys

def dec_key_schedule(key):
    subkeys = []
    pc1 = PC1(key)
    (c,d) = split56to28(pc1)
    subkey = PC2(concatenate28to56(c,d))
    subkeys.append(subkey)
    
    for i in range(15):        
        if(i == 0 or i == 7 or i == 14):
            c = rot_right(c,1)
            d = rot_right(d,1)            
        else:
            c = rot_right(c,2)
            d = rot_right(d,2)

        subkey = PC2(concatenate28to56(c,d))
        subkeys.append(subkey)
        
    return subkeys
