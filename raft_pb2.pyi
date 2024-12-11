from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class RequestType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    get: _ClassVar[RequestType]
    put: _ClassVar[RequestType]
    replace: _ClassVar[RequestType]

get: RequestType
put: RequestType
replace: RequestType

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

class LogEntry(_message.Message):
    __slots__ = ("key", "value", "ClientId", "RequestId", "index", "term", "request")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    CLIENTID_FIELD_NUMBER: _ClassVar[int]
    REQUESTID_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    TERM_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    ClientId: int
    RequestId: int
    index: int
    term: int
    request: RequestType
    def __init__(
        self,
        key: _Optional[str] = ...,
        value: _Optional[str] = ...,
        ClientId: _Optional[int] = ...,
        RequestId: _Optional[int] = ...,
        index: _Optional[int] = ...,
        term: _Optional[int] = ...,
        request: _Optional[_Union[RequestType, str]] = ...,
    ) -> None: ...

class AppendEntriesArgs(_message.Message):
    __slots__ = (
        "term",
        "leaderId",
        "prevLogIndex",
        "prevLogTerm",
        "entries",
        "leaderCommit",
    )
    TERM_FIELD_NUMBER: _ClassVar[int]
    LEADERID_FIELD_NUMBER: _ClassVar[int]
    PREVLOGINDEX_FIELD_NUMBER: _ClassVar[int]
    PREVLOGTERM_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    LEADERCOMMIT_FIELD_NUMBER: _ClassVar[int]
    term: int
    leaderId: int
    prevLogIndex: int
    prevLogTerm: int
    entries: _containers.RepeatedCompositeFieldContainer[LogEntry]
    leaderCommit: int
    def __init__(
        self,
        term: _Optional[int] = ...,
        leaderId: _Optional[int] = ...,
        prevLogIndex: _Optional[int] = ...,
        prevLogTerm: _Optional[int] = ...,
        entries: _Optional[_Iterable[_Union[LogEntry, _Mapping]]] = ...,
        leaderCommit: _Optional[int] = ...,
    ) -> None: ...

class AppendEntriesReply(_message.Message):
    __slots__ = ("term", "success", "nextTryIndex")
    TERM_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    NEXTTRYINDEX_FIELD_NUMBER: _ClassVar[int]
    term: int
    success: bool
    nextTryIndex: int
    def __init__(
        self,
        term: _Optional[int] = ...,
        success: bool = ...,
        nextTryIndex: _Optional[int] = ...,
    ) -> None: ...

class RequestVoteArgs(_message.Message):
    __slots__ = ("term", "candidateId", "lastLogIndex", "lastLogTerm")
    TERM_FIELD_NUMBER: _ClassVar[int]
    CANDIDATEID_FIELD_NUMBER: _ClassVar[int]
    LASTLOGINDEX_FIELD_NUMBER: _ClassVar[int]
    LASTLOGTERM_FIELD_NUMBER: _ClassVar[int]
    term: int
    candidateId: int
    lastLogIndex: int
    lastLogTerm: int
    def __init__(
        self,
        term: _Optional[int] = ...,
        candidateId: _Optional[int] = ...,
        lastLogIndex: _Optional[int] = ...,
        lastLogTerm: _Optional[int] = ...,
    ) -> None: ...

class RequestVoteReply(_message.Message):
    __slots__ = ("term", "voteGranted")
    TERM_FIELD_NUMBER: _ClassVar[int]
    VOTEGRANTED_FIELD_NUMBER: _ClassVar[int]
    term: int
    voteGranted: bool
    def __init__(self, term: _Optional[int] = ..., voteGranted: bool = ...) -> None: ...
