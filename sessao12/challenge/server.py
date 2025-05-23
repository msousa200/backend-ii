"""
gRPC Server implementando um serviço de streaming que envia uma sequência de números.

Este arquivo define um servidor gRPC que implementa o serviço `StreamService` definido 
no arquivo Proto. O serviço fornece o método `StreamNumbers` que transmite números
em um intervalo especificado pelo cliente.
"""

from concurrent import futures
import logging
import time
import grpc


import streaming_pb2
import streaming_pb2_grpc

class StreamService(streaming_pb2_grpc.StreamServiceServicer):
    """Implementação do serviço StreamService definido no arquivo proto"""
    
    def StreamNumbers(self, request, context):
        """
        Implementa o método RPC StreamNumbers.
        Este método demonstra o servidor enviando múltiplos valores para um único pedido do cliente.
        
        Args:
            request: Um objeto StreamRequest contendo os valores de início e fim.
            context: Contexto RPC contendo informações sobre a chamada.
            
        Yields:
            Objetos StreamReply contendo cada número no intervalo e uma mensagem.
        """
        start = request.start
        end = request.end
        
        print(f"Recebido pedido para transmitir números de {start} a {end}")
        

        if start > end:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"O valor inicial ({start}) não pode ser maior que o valor final ({end})")
            return

        if end - start > 1000:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"O intervalo é muito grande. Máximo permitido: 1000 números")
            return
        

        for num in range(start, end + 1):
            
            square = num * num

            message = f"O quadrado de {num} é {square}"

            yield streaming_pb2.StreamReply(number=num, message=message)
            

            time.sleep(0.2)
        
        print(f"Concluída a transmissão de {end - start + 1} números")

def serve():
    """Inicia o servidor gRPC e aguarda a terminação."""

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    

    streaming_pb2_grpc.add_StreamServiceServicer_to_server(StreamService(), server)
    

    server.add_insecure_port('[::]:50052')
    

    print("Servidor iniciado, ouvindo na porta 50052...")
    server.start()
    
    try:

        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Servidor encerrado pelo usuário.")

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    serve()
