import grpc
from concurrent import futures
import wallet_pb2
import wallet_pb2_grpc
import sys
from google.protobuf.empty_pb2 import Empty

class WalletServicer(wallet_pb2_grpc.WalletServicer):
    def __init__(self):
        self.wallets = {}
        self.orders = {}
        self.next_order_id = 1
        self.server = None  # Referência ao servidor gRPC

    def GetBalance(self, request, context):
        wallet_id = request.id
        if wallet_id in self.wallets:
            balance = self.wallets[wallet_id]
            return wallet_pb2.Balance(value=balance)
        return wallet_pb2.Balance(value=-1)

    def CreateOrder(self, request, context):
        wallet_id = request.id
        amount = request.amount
        if wallet_id not in self.wallets or self.wallets[wallet_id] < amount:
            return wallet_pb2.PaymentOrderResponse(status=-2, order_id=-1)
        
        self.wallets[wallet_id] -= amount
        order_id = self.next_order_id
        self.orders[order_id] = amount
        self.next_order_id += 1
        return wallet_pb2.PaymentOrderResponse(status=0, order_id=order_id)

    def Transfer(self, request, context):
        order_id = request.order_id
        confirmation_value = request.confirmation_value
        destination_id = request.destination_id

        if order_id not in self.orders or self.orders[order_id] != confirmation_value:
            return wallet_pb2.TransferResponse(status=-2)
        if destination_id not in self.wallets:
            return wallet_pb2.TransferResponse(status=-3)
        
        self.wallets[destination_id] += self.orders[order_id]
        del self.orders[order_id]
        return wallet_pb2.TransferResponse(status=0)

    def Shutdown(self, request, context):
        pending_orders = len(self.orders)
        wallets = [wallet_pb2.WalletData(id=k, value=v) for k, v in self.wallets.items()]
        print("Comando 'F' recebido. Encerrando o servidor...")
        if self.server:  # Verifique se a referência do servidor foi atribuída
            self.server.stop(0)  # Para o servidor imediatamente
        return wallet_pb2.ShutdownResponse(pending_orders=pending_orders, wallets=wallets)

def serve(port, wallet_servicer):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    wallet_servicer.server = server  # Passa a referência do servidor para o WalletServicer
    wallet_pb2_grpc.add_WalletServicer_to_server(wallet_servicer, server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Servidor de carteiras iniciado na porta {port}")
    server.wait_for_termination()

if __name__ == '__main__':
    port = sys.argv[1]
    input_source = sys.argv[2] if len(sys.argv) > 2 else None  # Argumento opcional para o arquivo de entrada
    wallet_servicer = WalletServicer()

    # Leitura de carteiras e saldos
    if input_source:  # Se um arquivo for fornecido
        with open(input_source, 'r') as file:
            for line in file:
                wallet_id, balance = line.strip().split()
                wallet_servicer.wallets[wallet_id] = int(balance)
                print(f"Carteira {wallet_id} com saldo {balance} adicionada.")
    else:  # Caso contrário, lê da entrada padrão (stdin)
        print("Digite as carteiras e saldos (ex: Raphael 20). Pressione Ctrl+D quando terminar:")
        try:
            for line in sys.stdin:
                wallet_id, balance = line.strip().split()
                wallet_servicer.wallets[wallet_id] = int(balance)
                print(f"Carteira {wallet_id} com saldo {balance} adicionada.")
        except EOFError:
            print("Leitura de carteiras encerrada.")

    # Inicia o servidor
    serve(port, wallet_servicer)

