# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import raft_pb2 as raft__pb2

GRPC_GENERATED_VERSION = "1.68.0"
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower

    _version_not_supported = first_version_is_lower(
        GRPC_VERSION, GRPC_GENERATED_VERSION
    )
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f"The grpc package installed is at version {GRPC_VERSION},"
        + f" but the generated code in raft_pb2_grpc.py depends on"
        + f" grpcio>={GRPC_GENERATED_VERSION}."
        + f" Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}"
        + f" or downgrade your generated code using grpcio-tools<={GRPC_VERSION}."
    )


class KeyValueStoreStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetState = channel.unary_unary(
            "/KeyValueStore/GetState",
            request_serializer=raft__pb2.Empty.SerializeToString,
            response_deserializer=raft__pb2.State.FromString,
            _registered_method=True,
        )
        self.Get = channel.unary_unary(
            "/KeyValueStore/Get",
            request_serializer=raft__pb2.GetKey.SerializeToString,
            response_deserializer=raft__pb2.Reply.FromString,
            _registered_method=True,
        )
        self.Put = channel.unary_unary(
            "/KeyValueStore/Put",
            request_serializer=raft__pb2.KeyValue.SerializeToString,
            response_deserializer=raft__pb2.Reply.FromString,
            _registered_method=True,
        )
        self.Replace = channel.unary_unary(
            "/KeyValueStore/Replace",
            request_serializer=raft__pb2.KeyValue.SerializeToString,
            response_deserializer=raft__pb2.Reply.FromString,
            _registered_method=True,
        )


class KeyValueStoreServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetState(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def Get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def Put(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def Replace(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_KeyValueStoreServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "GetState": grpc.unary_unary_rpc_method_handler(
            servicer.GetState,
            request_deserializer=raft__pb2.Empty.FromString,
            response_serializer=raft__pb2.State.SerializeToString,
        ),
        "Get": grpc.unary_unary_rpc_method_handler(
            servicer.Get,
            request_deserializer=raft__pb2.GetKey.FromString,
            response_serializer=raft__pb2.Reply.SerializeToString,
        ),
        "Put": grpc.unary_unary_rpc_method_handler(
            servicer.Put,
            request_deserializer=raft__pb2.KeyValue.FromString,
            response_serializer=raft__pb2.Reply.SerializeToString,
        ),
        "Replace": grpc.unary_unary_rpc_method_handler(
            servicer.Replace,
            request_deserializer=raft__pb2.KeyValue.FromString,
            response_serializer=raft__pb2.Reply.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "KeyValueStore", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers("KeyValueStore", rpc_method_handlers)


# This class is part of an EXPERIMENTAL API.
class KeyValueStore(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetState(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/KeyValueStore/GetState",
            raft__pb2.Empty.SerializeToString,
            raft__pb2.State.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True,
        )

    @staticmethod
    def Get(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/KeyValueStore/Get",
            raft__pb2.GetKey.SerializeToString,
            raft__pb2.Reply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True,
        )

    @staticmethod
    def Put(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/KeyValueStore/Put",
            raft__pb2.KeyValue.SerializeToString,
            raft__pb2.Reply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True,
        )

    @staticmethod
    def Replace(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/KeyValueStore/Replace",
            raft__pb2.KeyValue.SerializeToString,
            raft__pb2.Reply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True,
        )


class FrontEndStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Get = channel.unary_unary(
            "/FrontEnd/Get",
            request_serializer=raft__pb2.GetKey.SerializeToString,
            response_deserializer=raft__pb2.Reply.FromString,
            _registered_method=True,
        )
        self.Put = channel.unary_unary(
            "/FrontEnd/Put",
            request_serializer=raft__pb2.KeyValue.SerializeToString,
            response_deserializer=raft__pb2.Reply.FromString,
            _registered_method=True,
        )
        self.Replace = channel.unary_unary(
            "/FrontEnd/Replace",
            request_serializer=raft__pb2.KeyValue.SerializeToString,
            response_deserializer=raft__pb2.Reply.FromString,
            _registered_method=True,
        )
        self.StartRaft = channel.unary_unary(
            "/FrontEnd/StartRaft",
            request_serializer=raft__pb2.IntegerArg.SerializeToString,
            response_deserializer=raft__pb2.Reply.FromString,
            _registered_method=True,
        )


class FrontEndServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def Put(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def Replace(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def StartRaft(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_FrontEndServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "Get": grpc.unary_unary_rpc_method_handler(
            servicer.Get,
            request_deserializer=raft__pb2.GetKey.FromString,
            response_serializer=raft__pb2.Reply.SerializeToString,
        ),
        "Put": grpc.unary_unary_rpc_method_handler(
            servicer.Put,
            request_deserializer=raft__pb2.KeyValue.FromString,
            response_serializer=raft__pb2.Reply.SerializeToString,
        ),
        "Replace": grpc.unary_unary_rpc_method_handler(
            servicer.Replace,
            request_deserializer=raft__pb2.KeyValue.FromString,
            response_serializer=raft__pb2.Reply.SerializeToString,
        ),
        "StartRaft": grpc.unary_unary_rpc_method_handler(
            servicer.StartRaft,
            request_deserializer=raft__pb2.IntegerArg.FromString,
            response_serializer=raft__pb2.Reply.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "FrontEnd", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers("FrontEnd", rpc_method_handlers)


# This class is part of an EXPERIMENTAL API.
class FrontEnd(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Get(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/FrontEnd/Get",
            raft__pb2.GetKey.SerializeToString,
            raft__pb2.Reply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True,
        )

    @staticmethod
    def Put(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/FrontEnd/Put",
            raft__pb2.KeyValue.SerializeToString,
            raft__pb2.Reply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True,
        )

    @staticmethod
    def Replace(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/FrontEnd/Replace",
            raft__pb2.KeyValue.SerializeToString,
            raft__pb2.Reply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True,
        )

    @staticmethod
    def StartRaft(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/FrontEnd/StartRaft",
            raft__pb2.IntegerArg.SerializeToString,
            raft__pb2.Reply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True,
        )