"""
Cliente gRPC para o serviço Calculator.

Este cliente se conecta ao servidor gRPC e invoca o método CalculateCube
para calcular o cubo de um número.
"""

import logging
import grpc
import sys


import calculator_pb2
import calculator_pb2_grpc

def run(number):
    """
    Executa o cliente, conectando ao servidor e chamando o serviço Calculator.
    
    Args:
        number: O número para calcular o cubo.
    """

    with grpc.insecure_channel('localhost:50051') as channel:

        stub = calculator_pb2_grpc.CalculatorStub(channel)
        

        request = calculator_pb2.CubeRequest(number=number)
        
        print(f"Solicitando o cálculo do cubo de {number}...")
        
        try:

            response = stub.CalculateCube(request)
            print(f"Resposta recebida: {number}³ = {response.result}")
        except grpc.RpcError as e:
            print(f"Erro ao chamar o serviço: {e.details()}")

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    

    if len(sys.argv) > 1:
        try:
            number = int(sys.argv[1])
            run(number)
        except ValueError:
            print(f"Erro: '{sys.argv[1]}' não é um número válido")
            print("Uso: python client.py <número>")
    else:

        number = 5
        print("Nenhum número fornecido, usando o valor padrão 5")
        run(number)
