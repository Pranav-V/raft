import grpc
import raft_pb2
import raft_pb2_grpc
import time

channel = grpc.insecure_channel("localhost:8001")
stub = raft_pb2_grpc.FrontEndStub(channel)

ag = raft_pb2.IntegerArg(arg=2)
stub.StartRaft(ag)
time.sleep(3)
ag = raft_pb2.KeyValue(key="hello", value="there", ClientId=1, RequestId=2)
stub.Put(ag)
