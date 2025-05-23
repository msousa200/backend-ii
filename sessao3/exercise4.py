import logging
import threading
import time
import random
import queue

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(message)s'
)

buffer = queue.Queue(maxsize=10)

def threadprodutor():
    """Thread produtor gera números aleatórios e coloca na Queue"""
    for i in range(1, 26):
        item = random.randint(0, 100)
        buffer.put(item)  
        logging.info(f"Produzido: {item}")
        time.sleep(random.uniform(0.1, 0.5))
    
    buffer.put(None)  
    logging.info("Produtor terminou")

def threadconsumidor():
    """Thread consumidor processa os números da Queue"""
    while True:
        item = buffer.get()
        if item is None:
            logging.info("Consumidor terminou")  
            buffer.task_done() 
        resultado = item * 2
        logging.info(f"Consumido: {item}, Resultado: {resultado}")
        buffer.task_done()
        time.sleep(random.uniform(0.1, 0.5))

thread_produtor = threading.Thread(target=threadprodutor, name="ThreadProdutor")
thread_consumidor = threading.Thread(target=threadconsumidor, name="ThreadConsumidor")

logging.info("Iniciando threads...")
thread_produtor.start()
thread_consumidor.start()

thread_produtor.join()
thread_consumidor.join()
logging.info("Threads finalizadas!")

