import grpc
from concurrent import futures
import store_pb2
import store_pb2_grpc
import wallet_pb2
import wallet_pb2_grpc
import sys
from google.protobuf.empty_pb2 import Empty

class StoreServicer(store_pb2_grpc.StoreServicer):
    def __init__(self, price, wallet_stub, seller_id):
        self.price = price
        self.wallet_stub = wallet_stub
        self.seller_id = seller_id
        self.seller_balance = self.get_initial_balance()
        self.server = None  # Referência ao servidor gRPC
        print(f"Saldo inicial do vendedor ({self.seller_id}): {self.seller_balance}")

    def get_initial_balance(self):
        print(f"Consultando saldo inicial para a carteira do vendedor: {self.seller_id}")
        response = self.wallet_stub.GetBalance(wallet_pb2.WalletId(id=self.seller_id))
        print(f"Saldo inicial consultado: {response.value}")
        return response.value

    def GetPrice(self, request, context):
        print(f"Pedido de preço recebido. Preço atual: {self.price}")
        return store_pb2.Price(value=self.price)

    def Purchase(self, request, context):
        order_id = request.order_id
        print(f"Recebido pedido de compra com ID de ordem {order_id} para o valor {self.price}")
        transfer_response = self.wallet_stub.Transfer(
            wallet_pb2.TransferRequest(order_id=order_id, confirmation_value=self.price, destination_id=self.seller_id)
        )
        if transfer_response.status == 0:
            self.seller_balance += self.price
            print(f"Compra realizada com sucesso. Novo saldo do vendedor ({self.seller_id}): {self.seller_balance}")
        else:
            print(f"Falha na compra com ID de ordem {order_id}. Status: {transfer_response.status}")
        return store_pb2.PurchaseResponse(status=transfer_response.status)

    def Shutdown(self, request, context):
        print("Recebido pedido para encerrar o servidor da loja.")
        if self.server:
            print("Encerrando servidor da loja.")
            self.server.stop(0)
        return store_pb2.StoreShutdownResponse(
            seller_balance=self.seller_balance, wallet_shutdown_status=0  # Removi a chamada para o Shutdown do wallet server
        )

def serve():
    price = int(sys.argv[1])
    port = sys.argv[2]
    seller_id = sys.argv[3]
    wallet_server = sys.argv[4]

    print(f"Iniciando servidor da loja na porta {port}. Produto a {price} unidades.")
    print(f"Conectando ao servidor de carteiras em {wallet_server} para o vendedor {seller_id}.")

    with grpc.insecure_channel(wallet_server) as wallet_channel:
        wallet_stub = wallet_pb2_grpc.WalletStub(wallet_channel)

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        store_servicer = StoreServicer(price, wallet_stub, seller_id)
        store_servicer.server = server  # Passa a referência do servidor gRPC para o servicer
        store_pb2_grpc.add_StoreServicer_to_server(store_servicer, server)
        server.add_insecure_port(f'[::]:{port}')
        server.start()
        print(f'Store server started on port {port}')
        server.wait_for_termination()

if __name__ == '__main__':
    serve()

