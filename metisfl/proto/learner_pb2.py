# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: metisfl/proto/learner.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from metisfl.proto import metis_pb2 as metisfl_dot_proto_dot_metis__pb2
from metisfl.proto import model_pb2 as metisfl_dot_proto_dot_model__pb2
from metisfl.proto import service_common_pb2 as metisfl_dot_proto_dot_service__common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1bmetisfl/proto/learner.proto\x12\x07metisfl\x1a\x19metisfl/proto/metis.proto\x1a\x19metisfl/proto/model.proto\x1a\"metisfl/proto/service_common.proto\"\xfc\x01\n\x14\x45valuateModelRequest\x12\x1d\n\x05model\x18\x01 \x01(\x0b\x32\x0e.metisfl.Model\x12\x12\n\nbatch_size\x18\x02 \x01(\r\x12I\n\x12\x65valuation_dataset\x18\x03 \x03(\x0e\x32-.metisfl.EvaluateModelRequest.dataset_to_eval\x12+\n\x07metrics\x18\x04 \x01(\x0b\x32\x1a.metisfl.EvaluationMetrics\"9\n\x0f\x64\x61taset_to_eval\x12\x0c\n\x08TRAINING\x10\x00\x12\x08\n\x04TEST\x10\x01\x12\x0e\n\nVALIDATION\x10\x02\"G\n\x15\x45valuateModelResponse\x12.\n\x0b\x65valuations\x18\x01 \x01(\x0b\x32\x19.metisfl.ModelEvaluations\"\x9a\x01\n\x0eRunTaskRequest\x12\x30\n\x0f\x66\x65\x64\x65rated_model\x18\x01 \x01(\x0b\x32\x17.metisfl.FederatedModel\x12#\n\x04task\x18\x02 \x01(\x0b\x32\x15.metisfl.LearningTask\x12\x31\n\x0fhyperparameters\x18\x03 \x01(\x0b\x32\x18.metisfl.Hyperparameters\",\n\x0fRunTaskResponse\x12\x19\n\x03\x61\x63k\x18\x01 \x01(\x0b\x32\x0c.metisfl.Ack\"\x11\n\x0fGetModelRequest\"G\n\x0cLearnerModel\x12\x18\n\x10global_iteration\x18\x01 \x01(\r\x12\x1d\n\x05model\x18\x02 \x01(\x0b\x32\x0e.metisfl.Model\"@\n\x10GetModelResponse\x12,\n\rlearner_model\x18\x01 \x01(\x0b\x32\x15.metisfl.LearnerModel2\x98\x03\n\x0eLearnerService\x12P\n\rEvaluateModel\x12\x1d.metisfl.EvaluateModelRequest\x1a\x1e.metisfl.EvaluateModelResponse\"\x00\x12\x41\n\x08GetModel\x12\x18.metisfl.GetModelRequest\x1a\x19.metisfl.GetModelResponse\"\x00\x12n\n\x17GetServicesHealthStatus\x12\'.metisfl.GetServicesHealthStatusRequest\x1a(.metisfl.GetServicesHealthStatusResponse\"\x00\x12>\n\x07RunTask\x12\x17.metisfl.RunTaskRequest\x1a\x18.metisfl.RunTaskResponse\"\x00\x12\x41\n\x08ShutDown\x12\x18.metisfl.ShutDownRequest\x1a\x19.metisfl.ShutDownResponse\"\x00\x62\x06proto3')



_EVALUATEMODELREQUEST = DESCRIPTOR.message_types_by_name['EvaluateModelRequest']
_EVALUATEMODELRESPONSE = DESCRIPTOR.message_types_by_name['EvaluateModelResponse']
_RUNTASKREQUEST = DESCRIPTOR.message_types_by_name['RunTaskRequest']
_RUNTASKRESPONSE = DESCRIPTOR.message_types_by_name['RunTaskResponse']
_GETMODELREQUEST = DESCRIPTOR.message_types_by_name['GetModelRequest']
_LEARNERMODEL = DESCRIPTOR.message_types_by_name['LearnerModel']
_GETMODELRESPONSE = DESCRIPTOR.message_types_by_name['GetModelResponse']
_EVALUATEMODELREQUEST_DATASET_TO_EVAL = _EVALUATEMODELREQUEST.enum_types_by_name['dataset_to_eval']
EvaluateModelRequest = _reflection.GeneratedProtocolMessageType('EvaluateModelRequest', (_message.Message,), {
  'DESCRIPTOR' : _EVALUATEMODELREQUEST,
  '__module__' : 'metisfl.proto.learner_pb2'
  # @@protoc_insertion_point(class_scope:metisfl.EvaluateModelRequest)
  })
_sym_db.RegisterMessage(EvaluateModelRequest)

EvaluateModelResponse = _reflection.GeneratedProtocolMessageType('EvaluateModelResponse', (_message.Message,), {
  'DESCRIPTOR' : _EVALUATEMODELRESPONSE,
  '__module__' : 'metisfl.proto.learner_pb2'
  # @@protoc_insertion_point(class_scope:metisfl.EvaluateModelResponse)
  })
_sym_db.RegisterMessage(EvaluateModelResponse)

RunTaskRequest = _reflection.GeneratedProtocolMessageType('RunTaskRequest', (_message.Message,), {
  'DESCRIPTOR' : _RUNTASKREQUEST,
  '__module__' : 'metisfl.proto.learner_pb2'
  # @@protoc_insertion_point(class_scope:metisfl.RunTaskRequest)
  })
_sym_db.RegisterMessage(RunTaskRequest)

RunTaskResponse = _reflection.GeneratedProtocolMessageType('RunTaskResponse', (_message.Message,), {
  'DESCRIPTOR' : _RUNTASKRESPONSE,
  '__module__' : 'metisfl.proto.learner_pb2'
  # @@protoc_insertion_point(class_scope:metisfl.RunTaskResponse)
  })
_sym_db.RegisterMessage(RunTaskResponse)

GetModelRequest = _reflection.GeneratedProtocolMessageType('GetModelRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETMODELREQUEST,
  '__module__' : 'metisfl.proto.learner_pb2'
  # @@protoc_insertion_point(class_scope:metisfl.GetModelRequest)
  })
_sym_db.RegisterMessage(GetModelRequest)

LearnerModel = _reflection.GeneratedProtocolMessageType('LearnerModel', (_message.Message,), {
  'DESCRIPTOR' : _LEARNERMODEL,
  '__module__' : 'metisfl.proto.learner_pb2'
  # @@protoc_insertion_point(class_scope:metisfl.LearnerModel)
  })
_sym_db.RegisterMessage(LearnerModel)

GetModelResponse = _reflection.GeneratedProtocolMessageType('GetModelResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETMODELRESPONSE,
  '__module__' : 'metisfl.proto.learner_pb2'
  # @@protoc_insertion_point(class_scope:metisfl.GetModelResponse)
  })
_sym_db.RegisterMessage(GetModelResponse)

_LEARNERSERVICE = DESCRIPTOR.services_by_name['LearnerService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EVALUATEMODELREQUEST._serialized_start=131
  _EVALUATEMODELREQUEST._serialized_end=383
  _EVALUATEMODELREQUEST_DATASET_TO_EVAL._serialized_start=326
  _EVALUATEMODELREQUEST_DATASET_TO_EVAL._serialized_end=383
  _EVALUATEMODELRESPONSE._serialized_start=385
  _EVALUATEMODELRESPONSE._serialized_end=456
  _RUNTASKREQUEST._serialized_start=459
  _RUNTASKREQUEST._serialized_end=613
  _RUNTASKRESPONSE._serialized_start=615
  _RUNTASKRESPONSE._serialized_end=659
  _GETMODELREQUEST._serialized_start=661
  _GETMODELREQUEST._serialized_end=678
  _LEARNERMODEL._serialized_start=680
  _LEARNERMODEL._serialized_end=751
  _GETMODELRESPONSE._serialized_start=753
  _GETMODELRESPONSE._serialized_end=817
  _LEARNERSERVICE._serialized_start=820
  _LEARNERSERVICE._serialized_end=1228
# @@protoc_insertion_point(module_scope)
