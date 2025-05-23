import multiprocessing
import time

def factorial(n):
    """Função recursiva para calcular fatorial"""
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

def compute_factorial(number, result_queue):
    """Função executada por cada processo"""
    start_time = time.time()
    result = factorial(number)
    end_time = time.time()
    result_queue.put((number, result, end_time - start_time))

if __name__ == "__main__":
    numbers = [5, 10, 15, 20]  
    processes = []
    result_queue = multiprocessing.Queue()  

    for num in numbers:
        p = multiprocessing.Process(
            target=compute_factorial,
            args=(num, result_queue)
        )
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print("\nResultados:")
    while not result_queue.empty():
        num, result, elapsed = result_queue.get()
        print(f"{num}! = {result} (tempo: {elapsed:.4f}s)")
        