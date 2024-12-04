import concurrent.futures
import grpc
import os
import raft_pb2
import raft_pb2_grpc
import subprocess


# Suppress logging warnings
os.environ["GRPC_VERBOSITY"] = "ERROR"


class FrontEnd(raft_pb2_grpc.FrontEndServicer):
    SERVER_PORT = 8001

    def Get(self, request, context):
        pass

    def Put(self, request, context):
        pass

    def Replace(self, request, context):
        pass

    def StartRaft(self, request, context):
        num_kvs_servers = request.arg
        for kvs_id in range(num_kvs_servers + 1):
            # spins up each kvs server process
            subprocess.Popen(
                [
                    "python3",
                    "keyvaluestore.py",
                    f"{kvs_id}",
                    f"raftserver{kvs_id}",
                    f"{num_kvs_servers}",
                ]
            )

        return raft_pb2.Reply()

    def log_msg(self, msg: str):
        print(f"[FrontEnd]: {msg}")


if __name__ == "__main__":
    frontend_server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=5))
    frontend_servicer = FrontEnd()
    raft_pb2_grpc.add_FrontEndServicer_to_server(frontend_servicer, frontend_server)
    frontend_server.add_insecure_port(f"[::]:{FrontEnd.SERVER_PORT}")

    frontend_server.start()
    frontend_servicer.log_msg("started")
    frontend_server.wait_for_termination()
