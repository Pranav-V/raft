import argparse
import concurrent.futures
import grpc
import raft_pb2_grpc
import subprocess


class KeyValueStore(raft_pb2_grpc.KeyValueStoreServicer):
    KVS_PORT_BASE = 9000

    def __init__(self, kvs_id: int, num_kvs_servers: int):
        self.kvs_id = kvs_id
        self.num_kvs_servers = num_kvs_servers
        self.server_port = self.__get_kvs_port(kvs_id)

    def GetState(self, request, context):
        pass

    def Get(self, request, context):
        pass

    def Put(self, request, context):
        pass

    def Replace(self, request, context):
        pass

    def log_msg(self, msg: str):
        print(f"[KVS {kvs_id}]: {msg}")

    def __get_kvs_port(self, kvs_id: int) -> int:
        return KeyValueStore.KVS_PORT_BASE + kvs_id


def parse_kvs_args() -> dict:
    # retrieve kvs data from frontend server
    parser = argparse.ArgumentParser()
    parser.add_argument("kvs_id")
    parser.add_argument("process_name")
    parser.add_argument("num_kvs_servers")

    return vars(parser.parse_args())


if __name__ == "__main__":
    args = parse_kvs_args()
    kvs_id, num_kvs_servers = int(args["kvs_id"]), int(args["num_kvs_servers"])

    kvs_servicer = KeyValueStore(kvs_id, num_kvs_servers)
    kvs_server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=5))
    raft_pb2_grpc.add_KeyValueStoreServicer_to_server(kvs_servicer, kvs_server)
    kvs_server.add_insecure_port(f"[::]:{kvs_servicer.server_port}")

    kvs_server.start()
    kvs_servicer.log_msg("started")
    kvs_server.wait_for_termination()
