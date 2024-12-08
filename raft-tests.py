import grpc
import raft_pb2
import raft_pb2_grpc

channel = grpc.insecure_channel("localhost:8001")
stub = raft_pb2_grpc.FrontEndStub(channel)

ag = raft_pb2.IntegerArg(arg=2)
stub.StartRaft(ag)
