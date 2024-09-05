import grpc
import wallet_pb2
import wallet_pb2_grpc
import sys
from google.protobuf.empty_pb2 import Empty

def run():
    wallet_id = sys.argv[1]  # Identificador da carteira
    server_address = sys.argv[2]  # Endereço do servidor de carteiras

    # Conectando ao servidor de carteiras
    print(f"Conectando ao servidor de carteiras em {server_address} para a carteira {wallet_id}")
    with grpc.insecure_channel(server_address) as channel:
        stub = wallet_pb2_grpc.WalletStub(channel)
        
        while True:
            command = input("Digite um comando: ").strip().split()
            if not command:
                continue
            action = command[0]

            if action == 'S':
                # Consulta de saldo
                print(f"Consultando saldo para a carteira {wallet_id}")
                response = stub.GetBalance(wallet_pb2.WalletId(id=wallet_id))
                print(f"Saldo da carteira {wallet_id}: {response.value}")
            elif action == 'O':
                # Criação de ordem de pagamento
                amount = int(command[1])
                print(f"Criando ordem de pagamento para {wallet_id} no valor de {amount}")
                response = stub.CreateOrder(wallet_pb2.PaymentOrderRequest(id=wallet_id, amount=amount))
                print(f"ID da ordem criada: {response.order_id}")
            elif action == 'X':
                # Transferência de valor para outra carteira
                order_id = int(command[1])
                confirmation_value = int(command[2])
                destination_id = command[3]
                print(f"Transferindo {confirmation_value} da ordem {order_id} para a carteira {destination_id}")
                response = stub.Transfer(wallet_pb2.TransferRequest(order_id=order_id, confirmation_value=confirmation_value, destination_id=destination_id))
                print(f"Status da transferência: {response.status}")
            elif action == 'F':
                # Encerramento do servidor de carteiras
                print("Encerrando o servidor de carteiras")
                response = stub.Shutdown(Empty())
                print("Carteiras ao encerrar:")
                for wallet in response.wallets:
                    print(f'{wallet.id} {wallet.value}')
                print(f"Ordens pendentes: {response.pending_orders}")
                break

if __name__ == '__main__':
    run()
