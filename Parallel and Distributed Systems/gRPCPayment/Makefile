clean:
	rm -f *_pb2*.py

# Regra para gerar os stubs somente quando necessário
wallet_pb2.py: wallet.proto
	python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. wallet.proto

store_pb2.py: store.proto
	python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. store.proto

stubs: wallet_pb2.py store_pb2.py

run_serv_banco:
	python wallet_server.py $(arg1)

run_cli_banco:
	python wallet_client.py $(arg1) $(arg2)

run_serv_loja:
	python store_server.py $(arg1) $(arg2) $(arg3) $(arg4)

run_cli_loja:
	python store_client.py $(arg1) $(arg2) $(arg3)

