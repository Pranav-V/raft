build-proto:
	python3 -m grpc_tools.protoc -I. --python_out=. \
	--pyi_out=. --grpc_python_out=. raft.proto

class-tests:
	cd ./class_tests/testing; go run testfrontend.go

format:
	black .

raft-tests:
	python3 raft-tests.py

start:
	python3 frontend.py

web:
	python3 app.py