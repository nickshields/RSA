#Required libraries for generating primes.
import random
import fractions

#The Rabin Miller Prime test is what I used to help verify that the large
#Prime numbers were in fact prime (It estimates it to a great deal of certainty).
#I used the internet as a resource to obtain this method. Help was attained from the following sources:
#https://inventwithpython.com/rabinMiller.py
#https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
#Also used was stack exchange to obtain methods to solve modular arithmetic using code.
def rabinMiller(num):
    # Returns True if num is a prime number.

    s = num - 1
    t = 0
    while s % 2 == 0:
        # keep halving s while it is even (and use t
        # to count how many times we halve s)
        s = s // 2
        t += 1

    for trials in range(5): # try to falsify num's primality 5 times
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1: # this test does not apply if v is 1.
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True


def isPrime(num):
    # Return True if num is a prime number. This function does a quicker
    # prime number check before calling rabinMiller().

    if (num < 2):
        return False # 0, 1, and negative numbers are not prime

    lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

    if num in lowPrimes:
        return True

    # See if any of the low prime numbers can divide num
    for prime in lowPrimes:
        if (num % prime == 0):
            return False

    # If all else fails, call rabinMiller() to determine if num is a prime.
    return rabinMiller(num)


def generateLargePrime(keysize=1024):
    # Returns a random 1024 bit number (Which is approx:300 digits.)
    while True:
        num = random.randrange(2**(keysize-1), 2**(keysize))
        if isPrime(num):
            return num

def extended_gcd(a, b):
    #Returns pair (x, y) such that xa + yb = gcd(a, b)
    x, lastx, y, lasty = 0, 1, 1, 0
    while b != 0:
        q, r = divmod(a, b)
        a, b = b, r
        x, lastx = lastx - q * x, x
        y, lasty = lasty - q * y, y
    return lastx, lasty

    #Calculate de = 1(mod phi)
    # It calculates dex +phiy = 1 
def decryptionKey(e, n):
    """Find the multiplicative inverse of e mod n."""
    x, y = extended_gcd(e, n)
    if x < 0:
        return n + x
    return x

def generate_key():
    p = generateLargePrime()
    q = generateLargePrime()
    n = p * q
    o = (p - 1) * (q - 1)
    e=70001 #Predefined here, but it could also be generated(more difficult)
    d = decryptionKey(e, o)
    return (n, e, d)

#This function calculates C=M^e(Modn) and D=C^d(Modn)
def calculate(x, m, n):
    a = 1
    while m > 0:
        if m % 2 == 1:
            a = (a * x) % n
        x = (x * x) % n
        m //= 2
    return a

def rsa_encrypt(message, n, e):
    return calculate(message, e, n)

def rsa_decrypt(ciphertext, n, d):
    return calculate(ciphertext, d, n)


#To Generate A Set of Keys, use:
n, e, d = generate_key()
#Now that you have your keys, we can take a numerical message and encrypt it:
message = 5435435
ciphertext = rsa_encrypt(message, n, e)
print "Cipher \n"+ str(ciphertext)

#To decrypt the message:
decrypted_message = rsa_decrypt(ciphertext, n, d)
print str(decrypted_message)
