import math
import random
import prime_generation

fermat_primes = [3, 5, 17, 257, 65537] #primes that can be expressed in the form 2^2^n + 1. these are the only known fermat primes. 
#65537 = 0x10001

def create_modulus(bits:int, variability_range = 32): #bits: int divisible by 2
    #generates 2 primes (with possible offset) and the resulting modulus p*q
    sys_rand = random.SystemRandom()
    if variability_range > 0:
        offset = sys_rand.randrange(-variability_range, variability_range)
    else:
        offset = 0
    p = prime_generation.generate_prime(bits//2-offset)
    q =  prime_generation.generate_prime(bits//2+offset)
    return (p, q, p*q)

#euler's totient function: counts the number of whole numbers under N relatively prime to N
def phi(prime_set):
    return (prime_set[0]-1) * (prime_set[1] - 1)

#generates a public key chosen from 1 to phi: has to be relatively prime to both N and phi to preserve security
#most efficient (for decryption) is something with low value + low hamming weight. fermat primes satisfy all properties.
def public_key(phi):
    for prime in fermat_primes[::-1]:
        if prime < phi:
            return prime

#private key is the modular multiplicative inverse of e mod phi. you need to know phi to caluclate private key efficiently. 
#in other words, d * e mod(phi) = 1, where d is private key and e is public key
def private_key(public_key, phi):

    #the euclidian algorithm, but extended. recursively finds the gcf of (a, b) by reducing problem to gcf of (a%b, a) as remainder always retains common factor.
    def extended_euclidean(a, b, coefficients=[(1,0), (0,1)]): #extended part keeps track of the values of x and y for the linear equation ax + by = gcf(a,b), allowing us to find modular mult. inverse of gcf. 
            if a == 0: #base case
                return [b, coefficients[1]] #returns gcf and the coefficients of initial a and b that result in ax + by = gcf(a,b)
            else:
                quotient, remainder = divmod(b, a) #divmod is efficnet way of calculating quotient + remainder using modulus
                return extended_euclidean(remainder, a, coefficients=[(coefficients[1][0]-quotient*coefficients[0][0], coefficients[1][1]-quotient*coefficients[0][1]), coefficients[0]])
                #reduction to smaller problem, but with coefficients for the remainder expressed using the coefficients for a and b
                #https://www.youtube.com/watch?v=IwRtISxAHY4
    
    coefficients = extended_euclidean(public_key, phi)[1] #gives us the coefficients needed for ax + by to equal 1 (since a, b relatively prime)

    if coefficients[0] > 0:
        print("aaaa")
        return coefficients[0] #since everything is taken mod b (phi), we can eliminate the value of by, leaving us with an x that is the mult. inv. of a under mod phi. 
    else:
        return coefficients[0] + phi

def asymmetric_key_pair(bits, prime_variability_range = 32):
    prime_pair = create_modulus(bits, variability_range = prime_variability_range)
    p = phi(prime_pair)
    e = public_key(p)
    d = private_key(e, p)
    return ((e, prime_pair[2]),d)


#thanks to Eddie Woo: The RSA Encryption Algorithm
#and Art of the Problem: Public Key Cryptography: RSA Encryption Algorithm
#and Computerphile: Prime Numbers & RSA Encryption Algorithm
#and Proof of Concept: The extended Euclidean algorithm in one simple idea
