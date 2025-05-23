import multiprocessing
import random
from functools import partial

def sum_of_squares(sublist):
    """Compute the sum of squares for a sublist"""
    return sum(x**2 for x in sublist)

def parallel_sum_squares(numbers, num_processes=4):
    """Divide the list and compute sum of squares in parallel"""
    chunk_size = len(numbers) // num_processes
    chunks = [numbers[i:i + chunk_size] 
              for i in range(0, len(numbers), chunk_size)]
    
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(sum_of_squares, chunks)
    
    return sum(results)  

if __name__ == "__main__":
    numbers = [random.randint(1, 100) for _ in range(1_000_000)]
    
    print("Computing sum of squares...")
    total = parallel_sum_squares(numbers)
    print(f"Total sum of squares: {total:,}")