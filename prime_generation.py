import math
import random
import time

first_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541]

#1. How common are primes? From PNT: probability of odd number p to be prime is 2/ln(p)
#2. How hard is it to test primality? Much more cost effective to choose probabilistic prediction

#random number generation
def RNG(bits):
    sys_rand = random.SystemRandom()
    return sys_rand.randrange(2**(bits-1) + 1, 2**bits)

#returns a random number not divisible by first primes
def possible_prime(bits):
    poss = RNG(bits)
    for prime in first_primes:
        if poss % prime == 0:
            return possible_prime(bits)
    return poss

#slow but definitive
def ptest_deterministic(n:int):
    #wilson's theorem: if math.factorial((n-1)) % n == p-1: return True 
    for i in range(2, round(math.sqrt(n))):
        if n % i == 0:
            return False
    return True


#faster but not 100% - can detect composite with cerainty, prime with high probability (75% per iteration)
#Rabin Miller primality test
def ptest_probabilistic(n:int, security:int=10):
    #miller-rabin test
    if n%2 == 0 or n == 1:
        return False

    factor = n-1
    power_2 = 0
    while factor % 2 == 0:
        factor >>= 1
        power_2 += 1
    factor = int(factor)

    sys_rand = random.SystemRandom() #cryptographically random object
    testers = [sys_rand.randrange(2, n) for test in range(security)]
    
    def composite_conditional(test):
        #tests the two conditions to see if the iteration is predicted to be composite
        if pow(test, factor, n) == 1:
            return False

        for i in range(power_2):
            if pow(test, 2**i * factor, n) == n-1:
                return False
        
        return True

    for test in testers:
        if composite_conditional(test):
            return False
    return True


def generate_prime(bits:int, security:int = 10):
    prime = possible_prime(bits)
    while not ptest_probabilistic(prime, security):
        prime = possible_prime(bits)
    return prime

'''
time1 = time.time()
print(generate_prime(1024))
print(time.time()-time1)
'''