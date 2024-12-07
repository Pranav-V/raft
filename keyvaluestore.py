import argparse
import concurrent.futures
import grpc
import os
import raft_pb2
import raft_pb2_grpc
import random
import subprocess
import threading
from enum import Enum


# suppress logging warnings
os.environ["GRPC_VERBOSITY"] = "ERROR"


class KeyValueStore(raft_pb2_grpc.KeyValueStoreServicer):
    KVS_PORT_BASE = 9000

    class KVSRPC(Enum):
        APPEND_ENTRIES = 1
        GET = 2
        GET_STATE = 3
        PUT = 4
        REPLACE = 5
        REQUEST_VOTE = 6

        @static
        def rpc_to_call(stub, request_type):
            match request_type:
                case APPEND_ENTRIES:
                    return stub.AppendEntries
                case GET:
                    return stub.Get
                case GET_STATE:
                    return stub.GetState
                case PUT:
                    return stub.Put
                case REPLACE:
                    return stub.Replace
                case REQUEST_VOTE:
                    return stub.RequestVote

    def __init__(self, server_id: int, num_servers: int):
        self.raft_server = RaftServer(self, server_id, num_servers)
        self.server_port = self.__get_kvs_port(server_id)

    def AppendEntries(self, request, context):
        pass

    def Get(self, request, context):
        pass

    def GetState(self, request, context):
        pass

    def Put(self, request, context):
        pass

    def Replace(self, request, context):
        pass

    def RequestVote(self, request, context):
        pass

    def broadcast_rpc(self, request_type: KeyValueStore.KVSRPC, request_data):
        # TODO setup up source port for network tests

        for server_id in range(1, self.num_servers + 1):
            # don't send rpc to self
            if server_id != self.raft_server.server_id:
                self.send_rpc(server_id, request_type, request_data)

    def cleanup(self):
        self.raft_server.cleanup()

    def send_rpc(self, server_id: int, request_type: KeyValueStore.KVSRPC, request_data):
        # TODO setup up source port for network tests

        channel = grpc.insecure_channel(f"localhost:{self.__get_server_port(server_id)}")
        stub = raft_pb2_grpc.KeyValueStoreStub(channel)
        KeyValueStore.KVSRPC.rpc_to_call(stub, request_type)(request_data)

    def __get_server_port(self, server_id: int) -> int:
        return KeyValueStore.KVS_PORT_BASE + server_id


class RaftServer:

    CHECK_TIME = 0.075

    class ServerState(Enum):
        FOLLOWER = 1
        CANDIDATE = 2
        LEADER = 3

    def __init__(self, kvs_servicer: KeyValueStore, server_id: int, num_servers: int):
        self.kvs_servicer = kvs_servicer
        self.server_id = server_id
        self.num_servers = num_servers

        # server state
        self.election_timeout = random.randint(150, 300)
        self.election_votes = 0
        self.leader_id = None
        self.remaining_time = self.election_timeout
        self.server_state = RaftServer.ServerState.FOLLOWER

        # check for timeouts every CHECK_TIME s
        threading.Timer(RaftServer.CHECK_TIME, self.__check_timeout).start()
        self.stop_check = False

        self.__log_msg("started")

    def cleanup(self):
        # prevent further timeout checks
        self.stop_check = True

    def __check_timeout(self):
        self.remaining_time -= CHECK_TIME * 1000

        # transition to candidate
        if self.remaining_time <= 0:
            self.server_state = RaftServer.ServerState.CANDIDATE

        # check for cleanup
        if not self.stop_check:
            threading.Timer(RaftServer.CHECK_TIME, self.__check_timeout).start()

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
