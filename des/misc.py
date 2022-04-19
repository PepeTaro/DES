def xor_str(s1,s2):
    """
    ビットを表す文字列s1とs2に対してXORを適用しその結果である文字列を返す。
    Args:
     s1: str
     s2: str
    Return:
     str
    """
    #assert(len(s1) == len(s2))    
    n = max(len(s1),len(s2))
    return ("{:0"+str(n)+"b}").format(int(s1,2)^int(s2,2))

def rot_left(s,i):
    return s[i:] + s[0:i]

def rot_right(s,i):
    return s[-i:] + s[0:-i]
