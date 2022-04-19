class Block:
    def __init__(self,size,val=0):        
        assert(0 <= val < 2**size) #The range of the vals of size bits
        self._size = size # The size of the block(bits)
        self._val  = val  # The value of the block(size bits)

    def __str__(self):
        s = "{:0" + "{0}".format(self._size) + "b}"
        return s.format(self._val)
    
    def __eq__(self,other):
        assert(type(self) == type(other))
        assert(self._size == other._size)
        for i in range(1,self._size + 1):
            if(self[i] != other[i]): return False
        return True

    def __add__(self,other):
        # This operator does the XOR operation. 
        assert(type(self) == type(other))
        assert(self._size == other._size)
        result = Block(self._size)
        for i in range(1,self._size + 1):
            result[i] = self[i] ^ other[i]
            
        return result
    
    def __getitem__(self,key):
        # Note that the index starts with 1 and ends with self._size
        # i.e. key in [1,self._size]        
        assert(1 <= key <= self._size)
        return (self._val >> (self._size - key)) & 1

    def __setitem__(self,key,val):
        # Note that the index starts with 1 and ends with self._size
        # i.e. key in [1,self._size]
        assert(1 <= key <= self._size)
        assert(val == 0 or val == 1)
        if(val == 0):
            self._val &= ~(1 << (self._size - key))
        else:
            self._val |= (1 << (self._size - key))

    def size(self):
        return self._size
    def val(self):
        return self._val
    
    def rot_left(self,shift):
        overflow = self._val & ((2**shift - 1) << (self._size - shift))
        self._val <<= shift
        self._val &= 2**(self._size) - 1
        self._val |= overflow >> self._size - shift

    def rot_right(self,shift):
        overflow = self._val & (2**shift - 1)
        self._val >>= shift
        self._val |= overflow << self._size - shift
        
def split_from64to32(block):
    assert(block.size() == 64)
    left = Block(32)
    right = Block(32)
    for i in range(1,32 + 1):
        left[i] = block[i]
    for i in range(1,32 + 1):
        right[i] = block[32 + i]
    return (left,right)

def concatenate_from32to64(l,r):
    assert(l.size() == 32)
    assert(r.size() == 32)
    result = Block(64)
    for i in range(1,32 + 1):
        result[i] = l[i]
        result[32 + i] = r[i]
        
    return result

import random
def main():
    b = Block(5,31);
    b[1] = 0
    b[5] = 0
    print(b[1],b[2],b[3],b[4],b[5])
    for i in range(5):
        print("Before left rot: ",b)
        b.rot_left(2)
        print("After left rot: ",b,"\n")
        
    for i in range(5):
        print("Before right rot: ",b)
        b.rot_right(2)
        print("After right rot: ",b,"\n")

    x = random.randrange(0,2**64)
    b = Block(64,x)
    print(b)
    (l,r) = split_from64to32(b)
    result = concatenate_from32to64(l,r)
    
    print("Left: ",l)
    print("Right: ",r)
    print("Concat: ",result,result == b)

    print("Xor clear: ",result + result)
    print("l ^ r: ",l + r)

    
if __name__ == '__main__':
    main()
