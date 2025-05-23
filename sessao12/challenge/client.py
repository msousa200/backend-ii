"""
Cliente gRPC para o serviço StreamService.

Este cliente se conecta ao servidor gRPC e invoca o método StreamNumbers
para receber um fluxo de números no intervalo especificado.
"""

import logging
import grpc
import sys

import streaming_pb2
import streaming_pb2_grpc

def run(start, end):
    """
    Executa o cliente, conectando ao servidor e chamando o serviço StreamService.
    
    Args:
        start: O número inicial do intervalo.
        end: O número final do intervalo.
    """

    with grpc.insecure_channel('localhost:50052') as channel:

        stub = streaming_pb2_grpc.StreamServiceStub(channel)
        

        request = streaming_pb2.StreamRequest(start=start, end=end)
        
        print(f"Solicitando transmissão de números de {start} a {end}...")
        
        try:

            responses = stub.StreamNumbers(request)
            

            for response in responses:
                print(f"Recebido: Número {response.number} - {response.message}")
                
            print("Transmissão concluída!")
            
        except grpc.RpcError as e:
            status_code = e.code()
            print(f"Erro gRPC: {status_code.name} - {e.details()}")

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    

    if len(sys.argv) > 2:
        try:
            start = int(sys.argv[1])
            end = int(sys.argv[2])
            run(start, end)
        except ValueError:
            print("Erro: Os argumentos devem ser números inteiros")
            print("Uso: python client.py <início> <fim>")
    else:

        start = 1
        end = 10
        print(f"Nenhum intervalo fornecido, usando valores padrão: {start} a {end}")
        run(start, end)
