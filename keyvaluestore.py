import argparse
import concurrent.futures
import grpc
import os
import raft_pb2
import raft_pb2_grpc
import random
import subprocess
import threading
import time
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

        @classmethod
        def rpc_to_call(cls, stub, request_type):
            if request_type is cls.APPEND_ENTRIES:
                return stub.AppendEntries
            elif request_type is cls.GET:
                return stub.Get
            elif request_type is cls.GET_STATE:
                return stub.GetState
            elif request_type is cls.PUT:
                return stub.Put
            elif request_type is cls.REPLACE:
                return stub.Replace
            elif request_type is cls.REQUEST_VOTE:
                return stub.RequestVote

    def __init__(self, server_id: int, num_servers: int):
        self.raft_server = RaftServer(self, server_id, num_servers)
        self.server_port = self.__get_server_port(server_id)

    def AppendEntries(self, request, context):
        return self.raft_server.recieve_message(
            KeyValueStore.KVSRPC.APPEND_ENTRIES, request
        )

    def Get(self, request, context):
        return self.raft_server.recieve_message(KeyValueStore.KVSRPC.GET, request)

    def GetState(self, request, context):
        return self.raft_server.recieve_message(KeyValueStore.KVSRPC.GET_STATE, request)

    def Put(self, request, context):
        return self.raft_server.recieve_message(KeyValueStore.KVSRPC.PUT, request)

    def Replace(self, request, context):
        return self.raft_server.recieve_message(KeyValueStore.KVSRPC.REPLACE, request)

    def RequestVote(self, request, context):
        return self.raft_server.recieve_message(
            KeyValueStore.KVSRPC.REQUEST_VOTE, request
        )

    def broadcast_rpc(self, request_type: KVSRPC, request_data):
        # TODO setup up source port for network tests

        for server_id in range(1, self.raft_server.num_servers + 1):
            # don't send rpc to self
            if server_id != self.raft_server.server_id:
                self.send_rpc(server_id, request_type, request_data)

    def cleanup(self):
        self.raft_server.cleanup()

    def send_rpc(
        self, server_id: int, request_type: KVSRPC, request_data
    ):
        # TODO setup up source port for network tests

        channel = grpc.insecure_channel(
            f"localhost:{self.__get_server_port(server_id)}"
        )
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
        # wait for other servers to start up
        time.sleep(1)

        self.kvs_servicer = kvs_servicer
        self.server_id = server_id
        self.num_servers = num_servers

        # server state
        # TODO persist state on stable storage
        self.current_term = 0
        self.election_timeout = random.randint(150, 300)
        self.election_votes = 0
        self.leader_id = None
        self.remaining_time = self.election_timeout
        self.server_state = RaftServer.ServerState.FOLLOWER
        self.voted_for = None

        # check for timeouts every CHECK_TIME s
        threading.Timer(RaftServer.CHECK_TIME, self.__check_timeout).start()
        self.stop_check = False

        self.__log_msg("started")

    def cleanup(self):
        # prevent further timeout checks
        self.stop_check = True

    def recieve_message(self, request_type: KeyValueStore.KVSRPC, request_data):
        if request_type is KeyValueStore.KVSRPC.APPEND_ENTRIES:
            pass
        elif request_type is KeyValueStore.KVSRPC.GET:
            pass
        elif request_type is KeyValueStore.KVSRPC.GET_STATE:
            pass
        elif request_type is KeyValueStore.KVSRPC.PUT:
            pass
        elif request_type is KeyValueStore.KVSRPC.REPLACE:
            pass
        elif request_type is KeyValueStore.KVSRPC.REQUEST_VOTE:
            return self.__handle_request_vote(
                request_data.term,
                request_data.candidateId,
                request_data.lastLogIndex,
                request_data.lastLogTerm,
            )

    def __check_timeout(self):
        self.remaining_time -= RaftServer.CHECK_TIME * 1000

        # transition to candidate
        if self.remaining_time <= 0:
            self.current_term += 1
            self.election_votes = 1
            self.server_state = RaftServer.ServerState.CANDIDATE
            self.voted_for = self.server_id
            self.__refresh_time()

            # TODO update last two params with acutal log information
            request_vote_args = raft_pb2.RequestVoteArgs(
                term=self.current_term,
                candidateId=self.server_id,
                lastLogIndex=0,
                lastLogTerm=0,
            )

            self.kvs_servicer.broadcast_rpc(
                self.kvs_servicer.KVSRPC.REQUEST_VOTE, request_vote_args
            )

        # check for cleanup
        if not self.stop_check:
            threading.Timer(RaftServer.CHECK_TIME, self.__check_timeout).start()

    def __handle_request_vote(
        self, term: int, candidate_id: int, last_log_index: int, last_log_term: int
    ):
        self.__refresh_time()
        self.__log_msg("recieved request")
        return raft_pb2.RequestVoteReply()

    def __refresh_time(self):
        self.remaining_time = self.election_timeout

    def __log_msg(self, msg: str):
        print(f"[KVS {self.server_id}]: {msg}")

    def __is_majority(self, count: int) -> bool:
        return count > (self.num_servers / 2)


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
