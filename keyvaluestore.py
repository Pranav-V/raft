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
from dataclasses import dataclass
from enum import Enum
from typing import Optional

# suppress logging warnings
os.environ["GRPC_VERBOSITY"] = "ERROR"


class KeyValueStore(raft_pb2_grpc.KeyValueStoreServicer):

    KVS_PORT_BASE = 9000
    KVS_TIMEOUT = 0.25

    class KVSRPC(Enum):
        APPEND_ENTRIES = 1
        GET = 2
        GET_STATE = 3
        PUT = 4
        REPLACE = 5
        REQUEST_VOTE = 6
        APPEND_ENTRIES_REPLY = 7
        REQUEST_VOTE_REPLY = 8

        @classmethod
        def rpc_to_call(cls, stub, request_type):
            if request_type is cls.APPEND_ENTRIES:
                return stub.AppendEntries
            elif request_type is cls.REQUEST_VOTE:
                return stub.RequestVote

            raise Exception

    def __init__(self, server_id: int, num_servers: int):
        self.raft_server = RaftServer(self, server_id, num_servers)
        self.server_port = self.__get_server_port(server_id)
        self.stop_check = False

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
        # prevent further rpc calls
        self.stop_check = True
        self.raft_server.cleanup()

    def send_rpc(self, server_id: int, request_type: KVSRPC, request_data):
        # TODO setup up source port for network tests

        if not self.stop_check:
            try:
                channel = grpc.insecure_channel(
                    f"localhost:{self.__get_server_port(server_id)}"
                )
                stub = raft_pb2_grpc.KeyValueStoreStub(channel)
                reply_data = KeyValueStore.KVSRPC.rpc_to_call(stub, request_type)(
                    request_data, timeout=KeyValueStore.KVS_TIMEOUT
                )
                self.raft_server.recieve_reply(request_type, reply_data)
            except:
                # timeout or network errors
                pass

    def __get_server_port(self, server_id: int) -> int:
        return KeyValueStore.KVS_PORT_BASE + server_id


class RaftServer:

    CHECK_TIME = 0.075

    class RaftLog:

        @dataclass
        class LogEntry:
            key: str
            value: str
            request: KeyValueStore.KVSRPC
            index: int
            term: int
            client_id: int
            request_id: int

        def __init__(self):
            self.commit_index = 0
            self.kvstore = {}
            self.log = []

        def append_log(self, new_entry: LogEntry) -> bool:
            # check for duplicate request
            for entry in self.log:
                if (
                    entry.client_id == new_entry.client_id
                    and entry.request_id == new_entry.request_id
                ):
                    return False

            self.log.append(new_entry)
            return True

        def copy_log(self, from_idx: int) -> list[raft_pb2.LogEntry]:
            copied_entries = []
            for i in range(from_idx, len(self.log)):
                entry = self.log[i]
                copied_entries.append(
                    raft_pb2.LogEntry(
                        key=entry.key,
                        value=entry.value,
                        ClientId=entry.client_id,
                        RequestId=entry.request_id,
                        index=entry.index,
                        term=entry.term,
                        request=(
                            {
                                KeyValueStore.KVSRPC.PUT: raft_pb2.RequestType.put,
                                KeyValueStore.KVSRPC.GET: raft_pb2.RequestType.get,
                                KeyValueStore.KVSRPC.REPLACE: raft_pb2.RequestType.replace,
                            }[entry.request]
                        ),
                    )
                )

            return copied_entries

        def last_entry(self) -> Optional[LogEntry]:
            return None if not self.log else self.log[-1]

        def __len__(self):
            return len(self.log)

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
        # TODO persist some state on stable storage
        self.current_term = 0
        self.election_timeout = random.randint(150, 300)
        self.election_votes = 0
        self.leader_id = None
        self.log = RaftServer.RaftLog()
        self.match_index = None
        self.next_index = None
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
            return self.__handle_append_entries(
                request_data.term,
                request_data.leaderId,
                request_data.prevLogIndex,
                request_data.prevLogTerm,
                request_data.entries,
                request_data.leaderCommit,
            )
        elif request_type is KeyValueStore.KVSRPC.GET:
            return
        elif request_type is KeyValueStore.KVSRPC.GET_STATE:
            return
        elif request_type is KeyValueStore.KVSRPC.PUT:
            return self.__handle_put(
                request_data.key,
                request_data.value,
                request_data.ClientId,
                request_data.RequestId,
            )
        elif request_type is KeyValueStore.KVSRPC.REPLACE:
            return
        elif request_type is KeyValueStore.KVSRPC.REQUEST_VOTE:
            return self.__handle_request_vote(
                request_data.term,
                request_data.candidateId,
                request_data.lastLogIndex,
                request_data.lastLogTerm,
            )

        raise Exception

    def recieve_reply(self, request_type: KeyValueStore.KVSRPC, reply_data):
        if request_type is KeyValueStore.KVSRPC.APPEND_ENTRIES:
            pass
        elif request_type is KeyValueStore.KVSRPC.REQUEST_VOTE:
            self.__handle_request_vote_reply(reply_data.term, reply_data.voteGranted)

    def __check_timeout(self):
        # no election timeout for leader
        if self.server_state is RaftServer.ServerState.LEADER:
            # heartbeat to maintain leadership
            append_entries_args = raft_pb2.AppendEntriesArgs(
                term=self.current_term, leaderId=self.server_id
            )

            self.kvs_servicer.broadcast_rpc(
                self.kvs_servicer.KVSRPC.APPEND_ENTRIES, append_entries_args
            )
        else:
            self.remaining_time -= RaftServer.CHECK_TIME * 1000

        # transition to candidate
        if self.remaining_time <= 0:
            self.current_term += 1
            self.election_votes = 1
            self.server_state = RaftServer.ServerState.CANDIDATE
            self.voted_for = self.server_id
            self.__refresh_time()

            last_entry = self.log.last_entry()
            last_log_index = last_log_term = -1
            if last_entry:
                last_log_index = last_entry.index
                last_log_term = last_entry.term

            request_vote_args = raft_pb2.RequestVoteArgs(
                term=self.current_term,
                candidateId=self.server_id,
                lastLogIndex=last_log_index,
                lastLogTerm=last_log_term,
            )

            self.kvs_servicer.broadcast_rpc(
                self.kvs_servicer.KVSRPC.REQUEST_VOTE, request_vote_args
            )

        # check for cleanup
        if not self.stop_check:
            threading.Timer(RaftServer.CHECK_TIME, self.__check_timeout).start()

    def __handle_append_entries(
        self,
        leader_term: int,
        leader_id: int,
        prev_log_index: int,
        prev_log_term: int,
        log_entries: list[raft_pb2.LogEntry],
        leader_commit_index: int,
    ):
        print(log_entries)
        if leader_term >= self.current_term:
            self.__refresh_time()

        return raft_pb2.AppendEntriesReply()

    def __handle_put(self, key: str, value: str, client_id: int, request_id: int):
        # TODO: check duplicate with client_id and request_id
        if self.server_state is not RaftServer.ServerState.LEADER:
            return raft_pb2.Reply(wrongLeader=True)

        new_entry = self.log.append_log(
            RaftServer.RaftLog.LogEntry(
                key,
                value,
                self.kvs_servicer.KVSRPC.PUT,
                len(self.log),
                self.current_term,
                client_id,
                request_id,
            )
        )

        # don't duplicate request in log
        try:
            if new_entry:
                match_to_index = len(self.log) - 1
                print(self.log.commit_index, match_to_index)
                while (
                    self.server_state is RaftServer.ServerState.LEADER
                    and self.log.commit_index <= match_to_index
                ):
                    for server_id in range(1, self.num_servers + 1):
                        if (
                            server_id != self.server_id
                            and self.match_index[server_id - 1] <= match_to_index
                        ):
                            prev_index = self.next_index[server_id - 1] - 1
                            append_entries_args = raft_pb2.AppendEntriesArgs(
                                term=self.current_term,
                                leaderId=self.server_id,
                                prevLogIndex=prev_index,
                                prevLogTerm=(
                                    0
                                    if prev_index == -1
                                    else self.log.log[prev_index].term
                                ),
                                entries=self.log.copy_log(prev_index + 1),
                                leaderCommit=self.log.commit_index,
                            )
                            self.kvs_servicer.broadcast_rpc(
                                self.kvs_servicer.KVSRPC.APPEND_ENTRIES,
                                append_entries_args,
                            )

                    # wait for replies to come through
                    time.sleep(KeyValueStore.KVS_TIMEOUT)

                    return raft_pb2.Reply(wrongLeader=False)
        except Exception as e:
            print(e)
        return raft_pb2.Reply(wrongLeader=False)

    def __handle_request_vote(
        self,
        candidate_term: int,
        candidate_id: int,
        candidate_last_log_index: int,
        candidate_last_log_term: int,
    ):
        # reject candidate (based on term)
        if candidate_term < self.current_term or (
            candidate_term == self.current_term and self.voted_for is not None
        ):
            return raft_pb2.RequestVoteReply(term=self.current_term, voteGranted=False)

        last_entry = self.log.last_entry()
        last_log_index = last_log_term = -1
        if last_entry:
            last_log_index = last_entry.index
            last_log_term = last_entry.term

        # reject candidate (based on log restriction)
        if last_log_term > candidate_last_log_term or (
            last_log_term == candidate_last_log_term
            and last_log_index > candidate_last_log_index
        ):
            return raft_pb2.RequestVoteReply(term=self.current_term, voteGranted=False)

        # vote for candidate and reset state TODO: do we still reset time each time (maybe leader is dead ig)
        self.current_term = candidate_term
        self.election_votes = 0
        self.leader_id = None
        self.match_index = None
        self.next_index = None
        self.server_state = RaftServer.ServerState.FOLLOWER
        self.voted_for = candidate_id
        self.__refresh_time()

        return raft_pb2.RequestVoteReply(term=self.current_term, voteGranted=True)

    def __handle_request_vote_reply(self, reply_term: int, vote_granted: bool):
        if self.current_term == reply_term and vote_granted:
            self.election_votes += 1

            # transition to leader
            if (
                self.__is_majority(self.election_votes)
                and self.server_state is RaftServer.ServerState.CANDIDATE
            ):
                self.leader_id = self.server_id
                self.match_index = [0] * self.num_servers
                self.next_index = [len(self.log)] * self.num_servers
                self.server_state = RaftServer.ServerState.LEADER

                self.__log_msg(f"elected leader for term {self.current_term}")

                # convey leadership change
                append_entries_args = raft_pb2.AppendEntriesArgs(
                    term=self.current_term, leaderId=self.server_id
                )

                self.kvs_servicer.broadcast_rpc(
                    self.kvs_servicer.KVSRPC.APPEND_ENTRIES, append_entries_args
                )

                time.sleep()

    def __refresh_time(self):
        self.remaining_time = self.election_timeout

    def __log_msg(self, msg: str):
        if not self.stop_check:
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
