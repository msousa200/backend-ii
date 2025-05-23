import math
import multiprocessing
from functools import partial

def is_prime(n):
    """Verifica se um número é primo de forma otimizada"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    w = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += w
        w = 6 - w
    return True

def primes_in_range(args):
    """Encontra primos em um intervalo específico"""
    start, end = args
    primes = []
    for num in range(start, end + 1):
        if is_prime(num):
            primes.append(num)
    return primes

def parallel_prime(max_num, num_processes=4):
    """Encontra primos em paralelo usando multiprocessing"""
    chunk_size = (max_num) // num_processes
    ranges = []
    for i in range(num_processes):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size if i != num_processes - 1 else max_num
        ranges.append((start, end))
    
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(primes_in_range, ranges)
    
    all_primes = []
    for sublist in results:
        all_primes.extend(sublist)
    return all_primes

if __name__ == "__main__":
    max_num = 1_000_000
    print(f"Calculando números primos até {max_num}...")
    
    primes = parallel_prime(max_num)
    print(f"Total de números primos encontrados: {len(primes)}")
    print(f"10 maiores primos encontrados: {sorted(primes)[-10:]}")