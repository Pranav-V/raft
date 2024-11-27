import concurrent.futures
import grpc
import grpc_gen.raft_pb2_grpc as raft_pb2
import subprocess


class Frontend(raft_pb2.FrontEndServicer):
    SERVER_PORT = 8001

    def Get(self, request, context):
        pass

    def Put(self, request, context):
        pass

    def Replace(self, request, context):
        pass

    def StartRaft(self, request, context):
        pass


if __name__ == "__main__":
    frontend_server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=5))
    raft_pb2.add_FrontEndServicer_to_server(Frontend(), frontend_server)
    frontend_server.add_insecure_port(f"[::]:{Frontend.SERVER_PORT}")
    frontend_server.start()
    print("frontend server started...")
    frontend_server.wait_for_termination()
