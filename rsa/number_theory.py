from math import sqrt 
import random

def is_integer(number):
    if(isinstance(number,int)):
        return True
    else:
        return False

def is_positive_integer(number):
    if(isinstance(number,int) and number > 0):
        return True
    else:
        return False

def is_non_negative_integer(number):
    if(isinstance(number,int) and number >= 0):
        return True
    else:
        return False

def is_divisible(dividend,divisor):
    """
    dividedがdevisorにより割り切れるかどうかをチェック。
    割り切れるならTrue,そうでないならFalseを返す。
    """
    assert(is_integer(dividend))
    assert(is_integer(divisor))
    
    if(dividend%divisor == 0):
        return True
    else:
        return False

def is_prime(test_number):
    """
    test_numberが素数か否かを判定。
    test_numberが素数ならTrue,合成数ならFalseを返す。

    Args
    --------
    test_number:正整数。
    """
    
    assert(is_positive_integer(test_number))
    
    if(test_number == 1):#自明な場合
        return False
    
    for divisor in range(2,int(sqrt(test_number))+1):# nが合成数なら,sqrt(n)以下で割り切れる。
        if(is_divisible(test_number,divisor)):
            return False
    return True

def factorize(n):
    """
    nを素因数分解しその結果を返す。

    Args
    --------
    n:素因数分解される,2以上の正整数

    Returns
    --------
    :dict
    nの素因数分解を表す辞書を返す
    Ex) factorize(12) -> {2:2,3:1}

    """
    assert(is_positive_integer(n) and n >= 2)    
    prime_factors = {} # nの素因数を格納するための辞書
    
    if(is_prime(n)): #素数なら自明
        prime_factors[n] = 1
        return prime_factors
    else:
        for prime in range(2,n):
            if(is_prime(prime)): # 2からn-1までの間の素数を判定
                while(is_divisible(n,prime)): # primeがnの素因数なら
                    if(prime in prime_factors): # すでにprimeが辞書に乗っている場合
                        prime_factors[prime] += 1
                    else: # 辞書に乗っていない場合初期化
                        prime_factors[prime] = 1
                    n //= prime
                if(n == 1): # これ以上素因数がないなら終わり
                    return prime_factors

def euler_phi(n):
    """
    nのオイラー関数を計算しその値を返す。

    Args
    --------
    n:正整数
     
    Returns
    -------
    :正整数
     nのオイラー関数の値を計算して返す。
    
    """
   
    assert(is_positive_integer(n))
    if(n == 1): # 自明な場合
        return 1
    
    prime_factors = factorize(n) # nの素因数を取得
    result = 1
    # pとkはそれぞれ、nの素因数とその素因数の個数を格納
    for p,k in prime_factors.items():
        # result *= (p^k-p^(k-1))を計算
        result *= (p-1)*(p**(k-1))
    return result

def euclidean(a,b):
    """
    ax+by=gをみたす整数(g,x,y)を求めて返す。

    Args
    ---------
    a:正整数
    b:正整数
    
    Returns
    -------
    :タプル
    (g,x,y),ここでg=gcd(a,b)(最大公約数),xとyは ax+by=gをみたす整数
    特にxは"正整数"
    """
    
    assert(is_positive_integer(a) and is_positive_integer(b)) #aとbは正整数でなくてはいけない
    
    # 以下のアルゴリズムは速くするために少し複雑
    # しかし行っていることは単にユークリッドの互除法。
    x = 1
    g = a
    v = 0
    w = b
    while(True):
        if(w == 0):
            y = (g-a*x)//b
            #xが正整数となるように調節
            if(x > 0):
                return (g,x,y)
            else:
                k = 1
                while(x+k*(b//g) <= 0):
                    k += 1
                return (g,x+k*(b//g),y-k*(a//g))
                      
        q = g//w
        t = g-q*w
        s = x-q*v
        (x,g) = (v,w)
        (v,w) = (s,t)
    
def exp_mod(a,k,m):
    """
    繰り返し自乗法によりa^k(mod m)を計算し、その値を返す。

    Args
    ----------
    a:正整数
    k:正整数
    m:正整数

    Returns
    -------
    :正整数
     a^k(mod m)の値
    """
    
    assert(is_non_negative_integer(k) and is_non_negative_integer(m))
    if(m == 0): return a**k
    elif(k == 0): return 1
    
    b = 1
    while(k>=1):
        if(k%2 == 1):
            b = (a*b)%m
        a = (a*a)%m
        k = k//2
    return b

def root_mod(k,b,m,phi_m=None):
    """
    法をmとしたbのk乗根を計算,
    つまり,x^k = b(mod m)をみたす正整数を計算。
    phi_mは、mのオイラー関数の値。この値が与えられていると高速。

    Args
    ----------
    k:正整数
    b:正整数
    m:正整数
    phi_m:正整数

    Returns
    -------
    :正整数
     x^k = b(mod m)をみたす正整数を返す。
    -------
    """

    assert(is_positive_integer(b) and is_positive_integer(k) and is_positive_integer(m))
    
    if(phi_m == None): # phi_mが与えられていないなら、前もってその値を計算をする。(NPクラス)
        phi_m = euler_phi(m)

    #以下はアルゴリズムが正しく動作するための条件(次が条件-> gcd(b,m) = 1,gcd(k,phi(m)) = 1)
    assert(euclidean(b,m)[0] == 1) # アルゴリズムの条件を満たしているかチェック
    (g,u,v) = euclidean(k,phi_m)
    assert(g == 1)  # アルゴリズムの条件を満たしているかチェック
        
    x = exp_mod(b,u,m)
    return x

def miller_rabin_test(test_number,a):
    """
    test_numberに対するMiller-Rabin判定法。
    "合成数"であるか否かを判定することに注意。
    
    Args
    ----------
    test_number:正整数
    a:正整数
     Miller-Rabin判定法のパラメーター。

    Returns
    -------
    :bool
    test_numberが合成数ならTrue,そうでないならFalseを返す
    Falseの場合は素数 "かもしれない"(確率的) ことを示唆している。
    """
    assert(test_number >= 2 and is_positive_integer(a))  # アルゴリズムの条件を満たしているかチェック
        
    if(is_divisible(test_number,2)):# 自明な場合
        return True


    k = 0
    q = test_number - 1
    while(is_divisible(q,2)):
        q //= 2
        k += 1
    val = exp_mod(a,q,test_number)
    
    if(not (is_divisible(val-1,test_number) or is_divisible(val+1,test_number))):
        for i in range(k):
            val *= val
            if(not is_divisible(val+1,test_number)):
                continue
            else:
                return False
        return True
    else:
        return False

def miller_rabin_prime_test(test_number,tries=100):
    """
    Miller-Rabin判定法を使って,確率的にtest_numberが素数か合成数か判定,素数ならTrue,そうでないならFalseを返す。
    triesが大きいほど判定信頼度は,増すが時間がかかる。

    Args
    ----------
    test_number: 2以上の正整数
    tries:正整数
     triesはMiller-Rabin判定のトライ回数、tries数が大きければ大きいほど判定信頼度は増す。

    Returns
    -------
    :bool
    test_numberがおそらく素数ならTrue,合成数ならFalse。
    """
    
    assert(test_number >= 2 and is_positive_integer(tries))
    
    if(test_number == 2):# 自明な素数
        return True
    elif(is_divisible(test_number,2)):# 2以外の偶数なら明らかにFalse
        return False

    for _ in range(tries):
        a = random.randint(1,test_number-1)  # 1からtest_number-1までの整数からランダムに一つ選択
        if(miller_rabin_test(test_number,a)):
            return False
    return True

def generate_n_digit_prime(digit,tries=100):
    """
    digit桁に近い素数を生成し返す、Miller-Rabin法を使用しているため確実に素数かどうかはわからない。

    Args
    ----------
    digit:正整数
     望む素数の桁数
    tries:正整数
     Miller-Rabin素数判定法に使用するトライ回数

    Returns
    --------
    :正整数
     digit桁に近い素数
    
    """
    
    assert(is_positive_integer(digit))
    
    if(digit == 1):
        prime = random.choice([2,3,5,7]) #HACK: 美しくない
        return prime
    else:
        prime = random.randint(10*(digit-1),10**digit-1)

    # primeが偶数なら奇数に調整(あとで2ずつ増やしていくため,つまり15,17,19,...のように増やしていき素数を見つける)
    if(is_divisible(prime,2)):
        prime += 1
    
    while(not miller_rabin_prime_test(prime,tries)):# 素数となるまで繰り返す
        prime += 2

    return prime

def generate_n_bits_prime(bits,tries=100):
    """
    bits長に近い素数を生成し返す、Miller-Rabin法を使用しているため確実に素数かどうかはわからない。

    Args
    ----------
    bits:正整数
     望む素数のビット長
    tries:正整数
     Miller-Rabin素数判定法に使用するトライ回数

    Returns
    --------
    :正整数
     bits長に近い素数
    
    """

    assert(bits >= 2) # 最小の素数は2(b10)であるため,bitsが１以下はエラー
    
    prime_candidate = random.getrandbits(bits) # 長さがbitsである乱数を生成
    prime_candidate |= 1 # 奇数に調整
    prime_candidate |= (1<<(bits-1)) | (1<<(bits-2))#prime_candidateが小さすぎる場合を防ぐ
    
    while(not miller_rabin_prime_test(prime_candidate,tries)):# 素数となるまで繰り返す
        prime_candidate += 2

    return prime_candidate
