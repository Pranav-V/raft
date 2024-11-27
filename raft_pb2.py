# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: raft.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC, 5, 28, 1, "", "raft.proto"
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\nraft.proto"\'\n\x05State\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x10\n\x08isLeader\x18\x02 \x01(\x08"K\n\x08KeyValue\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\x12\x10\n\x08\x43lientId\x18\x03 \x01(\x03\x12\x11\n\tRequestId\x18\x04 \x01(\x03":\n\x06GetKey\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x10\n\x08\x43lientId\x18\x02 \x01(\x03\x12\x11\n\tRequestId\x18\x03 \x01(\x03":\n\x05Reply\x12\x13\n\x0bwrongLeader\x18\x01 \x01(\x08\x12\r\n\x05\x65rror\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\t"\x07\n\x05\x45mpty"\x19\n\nIntegerArg\x12\x0b\n\x03\x61rg\x18\x01 \x01(\x05\x32\x83\x01\n\rKeyValueStore\x12\x1c\n\x08GetState\x12\x06.Empty\x1a\x06.State"\x00\x12\x18\n\x03Get\x12\x07.GetKey\x1a\x06.Reply"\x00\x12\x1a\n\x03Put\x12\t.KeyValue\x1a\x06.Reply"\x00\x12\x1e\n\x07Replace\x12\t.KeyValue\x1a\x06.Reply"\x00\x32\x84\x01\n\x08\x46rontEnd\x12\x18\n\x03Get\x12\x07.GetKey\x1a\x06.Reply"\x00\x12\x1a\n\x03Put\x12\t.KeyValue\x1a\x06.Reply"\x00\x12\x1e\n\x07Replace\x12\t.KeyValue\x1a\x06.Reply"\x00\x12"\n\tStartRaft\x12\x0b.IntegerArg\x1a\x06.Reply"\x00\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "raft_pb2", _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals["_STATE"]._serialized_start = 14
    _globals["_STATE"]._serialized_end = 53
    _globals["_KEYVALUE"]._serialized_start = 55
    _globals["_KEYVALUE"]._serialized_end = 130
    _globals["_GETKEY"]._serialized_start = 132
    _globals["_GETKEY"]._serialized_end = 190
    _globals["_REPLY"]._serialized_start = 192
    _globals["_REPLY"]._serialized_end = 250
    _globals["_EMPTY"]._serialized_start = 252
    _globals["_EMPTY"]._serialized_end = 259
    _globals["_INTEGERARG"]._serialized_start = 261
    _globals["_INTEGERARG"]._serialized_end = 286
    _globals["_KEYVALUESTORE"]._serialized_start = 289
    _globals["_KEYVALUESTORE"]._serialized_end = 420
    _globals["_FRONTEND"]._serialized_start = 423
    _globals["_FRONTEND"]._serialized_end = 555
# @@protoc_insertion_point(module_scope)