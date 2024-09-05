import grpc
import store_pb2
import store_pb2_grpc
import wallet_pb2
import wallet_pb2_grpc
import sys
from google.protobuf.empty_pb2 import Empty

def run():
    wallet_id = sys.argv[1]  # Identificador da carteira do cliente
    wallet_server = sys.argv[2]  # Endereço do servidor de carteiras
    store_server = sys.argv[3]  # Endereço do servidor da loja

    # Conectando ao servidor de carteiras e ao servidor da loja
    print(f"Conectando ao servidor de carteiras em {wallet_server} e ao servidor da loja em {store_server}")
    with grpc.insecure_channel(wallet_server) as wallet_channel, grpc.insecure_channel(store_server) as store_channel:
        wallet_stub = wallet_pb2_grpc.WalletStub(wallet_channel)
        store_stub = store_pb2_grpc.StoreStub(store_channel)

        # Consultando o preço do produto na loja
        print("Consultando o preço do produto na loja...")
        price_response = store_stub.GetPrice(Empty())
        print(f"Preço do produto: {price_response.value}")

        while True:
            command = input("Digite um comando: ").strip().split()
            if not command:
                continue
            action = command[0]

            if action == 'C':
                # Criação de ordem de pagamento para compra
                print(f"Criando ordem de pagamento para a carteira {wallet_id} no valor de {price_response.value}")
                order_response = wallet_stub.CreateOrder(wallet_pb2.PaymentOrderRequest(id=wallet_id, amount=price_response.value))
                print(f"ID da ordem criada: {order_response.order_id}")
                
                if order_response.order_id != -1:
                    # Realizando a compra na loja
                    print(f"Realizando compra com a ordem {order_response.order_id}")
                    purchase_response = store_stub.Purchase(store_pb2.PurchaseRequest(order_id=order_response.order_id))
                    print(f"Status da compra: {purchase_response.status}")
            elif action == 'T':
                # Encerrando o servidor da loja
                print("Encerrando o servidor da loja")
                shutdown_response = store_stub.Shutdown(Empty())
                print(f"Saldo final do vendedor: {shutdown_response.seller_balance}")
                print(f"Status de encerramento do servidor de carteiras: {shutdown_response.wallet_shutdown_status}")
                break

if __name__ == '__main__':
    run()

