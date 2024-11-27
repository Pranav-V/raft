build-proto:
	python3 -m grpc_tools.protoc -I. --python_out=. \
	--pyi_out=. --grpc_python_out=. raft.proto

format:
	black .

start:
	python3 frontend.py

web:
	python3 app.py