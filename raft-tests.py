# testing
import unittest

# networking
import concurrent.futures
import multiprocessing

# grpc + protobuf
import grpc
import raft_pb2
import raft_pb2_grpc

# overloaded services
from frontend import FrontEnd
from keyvaluestore import KeyValueStore, RaftServer

TEST_CLIENT_ID = 31415
test_request_id = 1

def get_requestid():
    old_req_id = test_request_id
    test_request_id += 1
    return old_req_id

# used for frontend since that test should be running entire time
def run_test_in_process(test_func):
    def wrapper(*args, **kwargs):
        process = multiprocessing.Process(target=test_func, args=args, kwargs=kwargs)
        process.start()
        process.join()
        if process.exitcode != 0:
            raise Exception(f"Process exited with code {process.exitcode}")
    return wrapper

class TestRaftFunctionality(unittest.TestCase):

    # frontend_servicer: FrontEnd = None
    # frontend: raft_pb2_grpc.FrontEndStub = None

    # frontend functionality

    @run_test_in_process
    def test_frontend_init_and_startraft(self):
        # init
        frontend_server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
        frontend_servicer = FrontEnd()
        raft_pb2_grpc.add_FrontEndServicer_to_server(frontend_servicer, frontend_server)
        frontend_server.add_insecure_port(f"[::]:{FrontEnd.SERVER_PORT}")

        frontend_server.start()
        frontend_servicer.log_msg("[raft-tests.py] Started Frontend")

        # startraft
        channel = grpc.insecure_channel("localhost:8001")
        frontend = raft_pb2_grpc.FrontEndStub(channel)

        ag = raft_pb2.IntegerArg(arg=10)
        frontend.StartRaft(ag)

        # terminate after last test is done
        frontend_server.wait_for_termination()

    def test_frontend_put_get(self):
        pass

        # # test get (key not present)
        # request = raft_pb2.GetKey(
        #     key = 'test_key',
        #     ClientId = TEST_CLIENT_ID,
        #     RequestId = get_requestid()
        # )
        # target = ''
        # self.frontend.Get(
        #     request = request,
        #     target = target
        # )

        # # test put
        # request = raft_pb2.KeyValue(
        #     key = 'test_key',
        #     value = 'test_val',
        #     ClientId = TEST_CLIENT_ID,
        #     RequestId = get_requestid()
        # )
        # target = ''
        # self.frontend.Put(
        #     request = request,
        #     target = target
        # )

        # # test get (key present)
        # request = raft_pb2.GetKey(
        #     key = 'test_key',
        #     ClientId = TEST_CLIENT_ID,
        #     RequestId = get_requestid()
        # )
        # target = ''
        # self.frontend.Put(
        #     request = request,
        #     target = target
        # )

    def test_frontend_replace(self):
        # Your test code for method3
        pass

if __name__ == '__main__':
    unittest.main()