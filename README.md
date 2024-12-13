# CS 380D Raft Implementation Project

##### Pranav Venkatesh, Ritesh Thakur, Ryan Parappuram

### Compilation

To compile this project, use the makefile commands.

- ```make start```
    - start the frontend service
- ```make raft-tests```
    - run our custom python raft testing suite
- ```make class-tests```
    - run the go testing framework provided by the class admin
- ```make build-proto```
    - build the ```raft.proto``` and store output into 3 files:
        - ```raft_pb2.py```: Contains globals used for ```grpc``` module
        - ```raft_pb2.pyi```: Contains implementations for the messages used for communication through the RPC calls
        - ```raft_pb2_grpc.py```: Contains implementations for the services used to process inter-server communication
        