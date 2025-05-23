import time
from contextlib import contextmanager

class Timer:
    def __init__(self, name="Code block"):
        self.name = name
        
    def __enter__(self):
        self.start_time = time.perf_counter()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.perf_counter() - self.start_time
        print(f"'{self.name}' executed in {elapsed:.4f} seconds")
        return False

@contextmanager
def timer(name="Code block"):
    start_time = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start_time
        print(f"'{name}' executed in {elapsed:.4f} seconds")

if __name__ == "__main__":
    print("Testing class-based Timer:")
    with Timer("Class timer test"):
        sum(i for i in range(1_000_000))
        time.sleep(0.5)
    
    print("\nTesting function-based timer:")
    with timer("Function timer test"):
        time.sleep(1)
        [x**2 for x in range(10_000)]