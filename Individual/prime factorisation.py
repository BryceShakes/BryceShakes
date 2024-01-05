
import math
from timeit import default_timer as timer

# all primes upto and including x
def bryce_primes(x):
    p = math.ceil(x)
    primes = []
    for i in range(2,p+1):
        test = False
        for j in range(2,i-1):
            if i%j == 0:
                test = True
                break
        if test == False:primes.append(i)
    return(primes)

# is x a prime
def bryce_prime_test(x):
        test = True
        for j in range(2,math.floor(x**0.5)+1):
            if x%j == 0:
                test = False
                break
        return(test)

# checking
bryce_primes(10)
bryce_prime_test(7)
bryce_prime_test(8)

# ready for factorisation
def bryce_factorisation(x):
    
    factors = [1,x]
    #generate primes
    pr = bryce_primes(x**0.5)
    
    for i in pr:
        index = 0
        pr_ind = i**(index+1)
        while pr_ind <= x**0.5:
            if x%pr_ind == 0:
                 index += 1
                 factors.append(pr_ind)
                 factors.append(int(x/pr_ind))
                 pr_ind = i**(index+1)
            else:
                break
            
    factors.sort()
    return(factors)
        

array_360 = bryce_factorisation(360)
big_array = bryce_factorisation(10561913748)


start = timer()
high_composit_num_arr = bryce_factorisation(6746328388800)
# this takes ages (which makes sense it has an unbeliable amount of factorisations)
end = timer()
print(end-start)