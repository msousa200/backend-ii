import logging
import threading
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(message)s'
)

def thread1():
    for number in range(0, 11, 2):
        logging.info(f"Número par: {number}")
        time.sleep(0.5)

def thread2():
    for number in range(1, 10, 2):
        logging.info(f"Número ímpar: {number}")
        time.sleep(0.7)

t1 = threading.Thread(target=thread1, name="ThreadPares")
t2 = threading.Thread(target=thread2, name="ThreadÍmpares")

logging.info("Iniciando threads...")
t1.start()
t2.start()
t1.join()
t2.join()
logging.info("Threads finalizadas!")

