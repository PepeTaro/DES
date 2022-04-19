from misc import *
from sbox import *

E_table = [
    32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9,10,11,12,13,
    12,13,14,15,16,17,
    16,17,18,19,20,21,
    20,21,22,23,24,25,
    24,25,26,27,28,29,
    28,29,30,31,32, 1
]

P_table = [
    16,7,20,21,29,12,28,17,
    1,15,23,26,5,18,31,10,
    2,8,24,14,32,27,3,9,
    19,13,30,6,22,11,4,25
]

def E(bits32):
    """
    bits32をE_tableを使用して置換し、その結果を返す。
    Args:
     bits32: str

    Return: 
     str
    """

    assert(len(bits32) == 32)
    result = ""
    for i in range(48):
        result += bits32[E_table[i]-1]
    return result

def P(bits32):
    """
    bits32をP_tableを使用して置換し、その結果を返す。
    Args:
     bits32: str

    Return: 
     str
    """

    assert(len(bits32) == 32)
    result = ""
    for i in range(32):
        result += bits32[P_table[i]-1]
    return result

def f(r,k):
    """
    DES内のf関数を実装した関数。
    詳細は参考書を参照。
    """
    assert(len(r) == 32)
    assert(len(k) == 48)
    e = E(r)
    e_xor_k = xor_str(e,k)
    s = Sbox(e_xor_k)
    result = P(s)
    
    return result
