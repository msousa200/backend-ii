import threading
import time

def print_letters():
    letters = ['A', 'B', 'C', 'D', 'E']
    for letter in letters:
        print(f"Letra: {letter}")
        time.sleep(1)  

def print_numbers():
    for number in range(1, 6):
        print(f"Número: {number}")
        time.sleep(1.5)  

if __name__ == "__main__":
    thread_letters = threading.Thread(target=print_letters)
    thread_numbers = threading.Thread(target=print_numbers)

    print("Iniciando threads...\n")

    thread_letters.start()
    thread_numbers.start()

    thread_letters.join()
    thread_numbers.join()

    print("\nThreads finalizados!")