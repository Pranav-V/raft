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
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'raft.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nraft.proto\x12\x06raftkv\"\'\n\x05State\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x10\n\x08isLeader\x18\x02 \x01(\x08\"K\n\x08KeyValue\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\x12\x10\n\x08\x43lientId\x18\x03 \x01(\x03\x12\x11\n\tRequestId\x18\x04 \x01(\x03\":\n\x06GetKey\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x10\n\x08\x43lientId\x18\x02 \x01(\x03\x12\x11\n\tRequestId\x18\x03 \x01(\x03\":\n\x05Reply\x12\x13\n\x0bwrongLeader\x18\x01 \x01(\x08\x12\r\n\x05\x65rror\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\t\"\x07\n\x05\x45mpty\"\x19\n\nIntegerArg\x12\x0b\n\x03\x61rg\x18\x01 \x01(\x05\"\x8e\x01\n\x08LogEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\x12\x10\n\x08\x43lientId\x18\x03 \x01(\x03\x12\x11\n\tRequestId\x18\x04 \x01(\x03\x12\r\n\x05index\x18\x05 \x01(\x05\x12\x0c\n\x04term\x18\x06 \x01(\x05\x12$\n\x07request\x18\x07 \x01(\x0e\x32\x13.raftkv.RequestType\"\x82\x01\n\x11\x41ppendEntriesArgs\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x10\n\x08leaderId\x18\x02 \x01(\x05\x12\x14\n\x0cprevLogIndex\x18\x03 \x01(\x05\x12!\n\x07\x65ntries\x18\x04 \x03(\x0b\x32\x10.raftkv.LogEntry\x12\x14\n\x0cleaderCommit\x18\x05 \x01(\x05\"I\n\x12\x41ppendEntriesReply\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x0f\n\x07success\x18\x02 \x01(\x08\x12\x14\n\x0cnextTryIndex\x18\x03 \x01(\x05\"_\n\x0fRequestVoteArgs\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x13\n\x0b\x63\x61ndidateId\x18\x02 \x01(\x05\x12\x14\n\x0clastLogIndex\x18\x03 \x01(\x05\x12\x13\n\x0blastLogTerm\x18\x04 \x01(\x05\"5\n\x10RequestVoteReply\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x13\n\x0bvoteGranted\x18\x02 \x01(\x08*,\n\x0bRequestType\x12\x07\n\x03get\x10\x00\x12\x07\n\x03put\x10\x01\x12\x0b\n\x07replace\x10\x02\x32\xc9\x02\n\rKeyValueStore\x12H\n\rAppendEntries\x12\x19.raftkv.AppendEntriesArgs\x1a\x1a.raftkv.AppendEntriesReply\"\x00\x12*\n\x08GetState\x12\r.raftkv.Empty\x1a\r.raftkv.State\"\x00\x12&\n\x03Get\x12\x0e.raftkv.GetKey\x1a\r.raftkv.Reply\"\x00\x12(\n\x03Put\x12\x10.raftkv.KeyValue\x1a\r.raftkv.Reply\"\x00\x12,\n\x07Replace\x12\x10.raftkv.KeyValue\x1a\r.raftkv.Reply\"\x00\x12\x42\n\x0bRequestVote\x12\x17.raftkv.RequestVoteArgs\x1a\x18.raftkv.RequestVoteReply\"\x00\x32\xbc\x01\n\x08\x46rontEnd\x12&\n\x03Get\x12\x0e.raftkv.GetKey\x1a\r.raftkv.Reply\"\x00\x12(\n\x03Put\x12\x10.raftkv.KeyValue\x1a\r.raftkv.Reply\"\x00\x12,\n\x07Replace\x12\x10.raftkv.KeyValue\x1a\r.raftkv.Reply\"\x00\x12\x30\n\tStartRaft\x12\x12.raftkv.IntegerArg\x1a\r.raftkv.Reply\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'raft_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_REQUESTTYPE']._serialized_start=801
  _globals['_REQUESTTYPE']._serialized_end=845
  _globals['_STATE']._serialized_start=22
  _globals['_STATE']._serialized_end=61
  _globals['_KEYVALUE']._serialized_start=63
  _globals['_KEYVALUE']._serialized_end=138
  _globals['_GETKEY']._serialized_start=140
  _globals['_GETKEY']._serialized_end=198
  _globals['_REPLY']._serialized_start=200
  _globals['_REPLY']._serialized_end=258
  _globals['_EMPTY']._serialized_start=260
  _globals['_EMPTY']._serialized_end=267
  _globals['_INTEGERARG']._serialized_start=269
  _globals['_INTEGERARG']._serialized_end=294
  _globals['_LOGENTRY']._serialized_start=297
  _globals['_LOGENTRY']._serialized_end=439
  _globals['_APPENDENTRIESARGS']._serialized_start=442
  _globals['_APPENDENTRIESARGS']._serialized_end=572
  _globals['_APPENDENTRIESREPLY']._serialized_start=574
  _globals['_APPENDENTRIESREPLY']._serialized_end=647
  _globals['_REQUESTVOTEARGS']._serialized_start=649
  _globals['_REQUESTVOTEARGS']._serialized_end=744
  _globals['_REQUESTVOTEREPLY']._serialized_start=746
  _globals['_REQUESTVOTEREPLY']._serialized_end=799
  _globals['_KEYVALUESTORE']._serialized_start=848
  _globals['_KEYVALUESTORE']._serialized_end=1177
  _globals['_FRONTEND']._serialized_start=1180
  _globals['_FRONTEND']._serialized_end=1368
# @@protoc_insertion_point(module_scope)
