import concurrent.futures
import grpc
import os
import raft_pb2
import raft_pb2_grpc
import subprocess


# suppress logging warnings
os.environ["GRPC_VERBOSITY"] = "ERROR"


class FrontEnd(raft_pb2_grpc.FrontEndServicer):
    SERVER_PORT = 8001
    KVS_PORT_BASE = 9000
    REQUEST_TIMEOUT = 0.5

    # TODO: add error checking for startraft

    def Get(self, request, context):
        pass

    def Put(self, request, context):
        curr_server_id = 1

        while True:
            try:
                channel = grpc.insecure_channel(
                    f"localhost:{self.__get_server_port(curr_server_id)}"
                )
                reply_data = raft_pb2_grpc.KeyValueStoreStub(channel).Put(
                    request, timeout=REQUEST_TIMEOUT
                )
                if not reply_data.wrongLeader:
                    # keep pinging the leader server
                    curr_server_id -= 1
                    if reply_data.error is None:
                        return reply_data
            except:
                pass
            finally:
                curr_server_id = (curr_server_id + 1) % (self.num_servers + 1)

    def Replace(self, request, context):
        pass

    def StartRaft(self, request, context):
        self.num_servers = request.arg
        for server_id in range(1, self.num_servers + 1):
            # spins up each kvs server process
            subprocess.Popen(
                [
                    "python3",
                    "keyvaluestore.py",
                    f"{server_id}",
                    f"raftserver{server_id}",
                    f"{self.num_servers}",
                ]
            )

        return raft_pb2.Reply()

    def log_msg(self, msg: str):
        print(f"[FrontEnd]: {msg}")

    def __get_server_port(self, server_id: int) -> int:
        return FrontEnd.KVS_PORT_BASE + server_id


if __name__ == "__main__":
    frontend_server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=5))
    frontend_servicer = FrontEnd()
    raft_pb2_grpc.add_FrontEndServicer_to_server(frontend_servicer, frontend_server)
    frontend_server.add_insecure_port(f"[::]:{FrontEnd.SERVER_PORT}")

    frontend_server.start()
    frontend_servicer.log_msg("started")
    frontend_server.wait_for_termination()
