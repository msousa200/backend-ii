"""
gRPC Server implementando um serviço de calculadora que calcula o cubo de um número.

Este arquivo define um servidor gRPC que implementa o serviço `Calculator` definido 
no arquivo Proto. O serviço fornece o método `CalculateCube` que calcula o cubo
de um número fornecido pelo cliente.
"""

from concurrent import futures
import logging
import grpc
import time


import calculator_pb2
import calculator_pb2_grpc

class Calculator(calculator_pb2_grpc.CalculatorServicer):
    """Implementação do serviço Calculator definido no arquivo proto"""
    
    def CalculateCube(self, request, context):
        """
        Implementa o método RPC CalculateCube.
        
        Args:
            request: Um objeto CubeRequest contendo o número a ser elevado ao cubo.
            context: Contexto RPC contendo informações sobre a chamada.
            
        Returns:
            Um objeto CubeReply contendo o resultado da operação.
        """
        number = request.number
        cube = number * number * number
        
        print(f"Recebido pedido para calcular o cubo de {number}")
        print(f"Resultado: {cube}")
        
        return calculator_pb2.CubeReply(result=cube)

def serve():
    """Inicia o servidor gRPC e aguarda a terminação."""

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    

    calculator_pb2_grpc.add_CalculatorServicer_to_server(Calculator(), server)
    

    server.add_insecure_port('[::]:50051')
    
    print("Servidor iniciado, ouvindo na porta 50051...")
    server.start()
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Servidor encerrado pelo usuário.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()
