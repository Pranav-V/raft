from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class State(_message.Message):
    __slots__ = ("term", "isLeader")
    TERM_FIELD_NUMBER: _ClassVar[int]
    ISLEADER_FIELD_NUMBER: _ClassVar[int]
    term: int
    isLeader: bool
    def __init__(self, term: _Optional[int] = ..., isLeader: bool = ...) -> None: ...

class KeyValue(_message.Message):
    __slots__ = ("key", "value", "ClientId", "RequestId")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    CLIENTID_FIELD_NUMBER: _ClassVar[int]
    REQUESTID_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    ClientId: int
    RequestId: int
    def __init__(
        self,
        key: _Optional[str] = ...,
        value: _Optional[str] = ...,
        ClientId: _Optional[int] = ...,
        RequestId: _Optional[int] = ...,
    ) -> None: ...

class GetKey(_message.Message):
    __slots__ = ("key", "ClientId", "RequestId")
    KEY_FIELD_NUMBER: _ClassVar[int]
    CLIENTID_FIELD_NUMBER: _ClassVar[int]
    REQUESTID_FIELD_NUMBER: _ClassVar[int]
    key: str
    ClientId: int
    RequestId: int
    def __init__(
        self,
        key: _Optional[str] = ...,
        ClientId: _Optional[int] = ...,
        RequestId: _Optional[int] = ...,
    ) -> None: ...

class Reply(_message.Message):
    __slots__ = ("wrongLeader", "error", "value")
    WRONGLEADER_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    wrongLeader: bool
    error: str
    value: str
    def __init__(
        self,
        wrongLeader: bool = ...,
        error: _Optional[str] = ...,
        value: _Optional[str] = ...,
    ) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class IntegerArg(_message.Message):
    __slots__ = ("arg",)
    ARG_FIELD_NUMBER: _ClassVar[int]
    arg: int
    def __init__(self, arg: _Optional[int] = ...) -> None: ...
