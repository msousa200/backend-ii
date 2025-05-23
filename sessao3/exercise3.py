import logging
import threading
import time

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(message)s'
)

counter = 0
lock = threading.Lock() 

def increment_counter(iterations, name):
    global counter
    for i in range(iterations):
        with lock:  
            current = counter
            time.sleep(0.01)
            counter = current + 1
            logging.info(f"{name} atualizou contador para: {counter}")

threads = []
for i in range(3):
    thread = threading.Thread(
        target=increment_counter, 
        args=(100, f"Thread-{i+1}"), 
        name=f"Thread-{i+1}"  
    )
    threads.append(thread)

logging.info("Iniciando threads...")
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

logging.info(f"Contador final: {counter}")  
logging.info(f"Valor esperado: {3 * 100}")  
