import argparse
import concurrent.futures
import grpc
import os
import raft_pb2_grpc
import random
import subprocess
import threading


# suppress logging warnings
os.environ["GRPC_VERBOSITY"] = "ERROR"


class KeyValueStore(raft_pb2_grpc.KeyValueStoreServicer):
    KVS_PORT_BASE = 9000

    def __init__(self, server_id: int, num_servers: int):
        self.raft_server = RaftServer(self, server_id, num_servers)
        self.server_port = self.__get_kvs_port(server_id)

    def GetState(self, request, context):
        pass

    def Get(self, request, context):
        pass

    def Put(self, request, context):
        pass

    def Replace(self, request, context):
        pass

    def cleanup(self):
        self.raft_server.cleanup()

    def __get_kvs_port(self, kvs_id: int) -> int:
        return KeyValueStore.KVS_PORT_BASE + kvs_id


class RaftServer:

    CHECK_TIME = 0.075

    def __init__(self, kvs_servicer: KeyValueStore, server_id: int, num_servers: int):
        self.kvs_servicer = kvs_servicer
        self.server_id = server_id
        self.num_servers = num_servers

        self.election_timeout = random.randint(150, 300)
        self.remaining_time = self.election_timeout

        # check for timeouts every CHECK_TIME s
        threading.Timer(RaftServer.CHECK_TIME, self.__check_timeout, args=(False,)).start()
        self.stop_check = False

        self.__log_msg("started")

    def cleanup(self):
        # prevent further timeout checks
        self.stop_check = True

    def __check_timeout(self, decrement: bool):
        if decrement:
            self.remaining_time -= (CHECK_TIME * 1000)

            # transition to candidate
            if self.remaining_time <= 0:
                pass

        # check for cleanup
        if not self.stop_check:
            threading.Timer(RaftServer.CHECK_TIME, self.__check_timeout, args=(True,)).start()

    def __log_msg(self, msg: str):
        print(f"[KVS {self.server_id}]: {msg}")


def parse_kvs_args() -> dict:
    # retrieve kvs data from frontend server
    parser = argparse.ArgumentParser()
    parser.add_argument("server_id")
    parser.add_argument("process_name")
    parser.add_argument("num_servers")

    return vars(parser.parse_args())


if __name__ == "__main__":
    args = parse_kvs_args()
    server_id, num_servers = int(args["server_id"]), int(args["num_servers"])

    kvs_servicer = KeyValueStore(server_id, num_servers)
    kvs_server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=5))
    raft_pb2_grpc.add_KeyValueStoreServicer_to_server(kvs_servicer, kvs_server)
    kvs_server.add_insecure_port(f"[::]:{kvs_servicer.server_port}")

    try:
        kvs_server.start()
        kvs_server.wait_for_termination()
    except KeyboardInterrupt:
        pass
    finally:
        kvs_servicer.cleanup()
