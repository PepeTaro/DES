import number_theory

def _swap(p,q):
    return (q,p)

def generate_keys1024():
    return generate_keys(1024)

def generate_keys2048():
    return generate_keys(2048)

def generate_keys3072():
    return generate_keys(3072)

def generate_keys4096():
    return generate_keys(4096)

def generate_keys(bit_length):
    """
    RSAの公開鍵と秘密鍵のペアを返す。
    引数bit_length(bitの長さであることに注意)は、modulusのビット長を指定している。
    """
    e = 65537 # public exponent(固定)

    (p,q) = generate_prime_pair(bit_length,e)# 素数のペアを生成        
    n = p*q # modulusを計算
    phi_n = (p-1)*(q-1) # nのオイラー関数を計算
    d = get_private_exponent(e,phi_n)# private exponentを計算
        
    return [(n,e),(d,p,q)] #[公開鍵,秘密鍵]を返す

def get_private_exponent(e,phi_n):
    """
    private exponentを計算してその結果を返す。
    private exponentとは d*e = 1 (mod phi_n) を満たす整数d。
    """
    
    euclidean_solution = number_theory.euclidean(e,phi_n)
    if(euclidean_solution[0] != 1):#private exponentの条件を満たさない場合
        print("[!]Error(generate_keys):eとphi_nが互いに素でない")
        exit(-1)

    d = euclidean_solution[1] # private exponentを取り出す
    assert(1 < d < phi_n) #private exponentの条件を確認

    return d

def generate_prime_pair(bit_length,e):
    """
    p*qのビット長がbit_lengthとほぼ等しくなるような,素数のペア(p,q)を生成し返す。
    (注意) 素数生成にはMiller-Rabin素数判定法を使用しているため,必ず素数を返すとは限らない
           (ただし,合成数を返す確率は(デフォルト動作において)限りなく0に近い確率)
    """

    assert(bit_length >= 10) #10ビット長以上でないと素数がうまく生成されない(例えば bit_length == 6だと,常にp==qとなる)
    
    while(True):                
        p = number_theory.generate_n_bits_prime(bit_length//2)
        q = number_theory.generate_n_bits_prime(bit_length - bit_length//2)
        
        if (p == q): continue   
        elif(p < q):# p > q　となるように調整
            (p,q) = _swap(p,q)
            break
    
    return (p,q)

def encrypt(plaintext,n,e):
    """
    整数であるplaintextを公開鍵(n,e)を使って暗号化して、その値を返す。
    """    
    assert(0 <= plaintext < n)
    ciphertext = number_theory.exp_mod(plaintext,e,n)#暗号化
    return ciphertext

def decrypt(ciphertext,n,d):
    """
    整数であるciphertextを公開鍵nと秘密鍵dを使って復号化して、その値を返す。
    """    
    assert(0 <= ciphertext < n)
    plaintext = number_theory.exp_mod(ciphertext,d,n)#復号化
    return plaintext
