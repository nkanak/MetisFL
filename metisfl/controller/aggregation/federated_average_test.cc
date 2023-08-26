
#include "metisfl/controller/aggregation/federated_average.h"

#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include "metisfl/controller/common/macros.h"
#include "metisfl/controller/common/proto_matchers.h"
#include "metisfl/controller/common/proto_tensor_serde.h"
#include "metisfl/proto/model.pb.h"

namespace metisfl::controller {
namespace {

using metisfl::proto::ParseTextOrDie;
using ::testing::proto::EqualsProto;

const char kModel1_with_tensor_values_1to10_as_UINT16[] = R"pb(
  tensor {
    length: 10
    encrypted: false
    dimensions: 10
    type { type: UINT16 byte_order: LITTLE_ENDIAN_ORDER fortran_order: False }
    value: "\001\000\002\000\003\000\004\000\005\000\006\000\007\000\010\000\t\000\n\000"
  }
)pb";

const char kModel1_with_tensor_values_1to10_as_INT32[] = R"pb(
  tensor {
    length: 10
    dimensions: 10
    encrypted: false
    type { type: INT32 byte_order: LITTLE_ENDIAN_ORDER fortran_order: False }
    value: "\001\000\000\000\002\000\000\000\003\000\000\000\004\000\000\000\005\000\000\000\006\000\000\000\007\000\000\000\010\000\000\000\t\000\000\000\n\000\000\000"
  }
)pb";

const char kModel1_with_tensor_values_1to10_as_FLOAT32[] = R"pb(
  tensor {
    length: 10
    encrypted: false
    dimensions: 10
    type { type: FLOAT32 byte_order: LITTLE_ENDIAN_ORDER fortran_order: False }
    value: "\000\000\200?\000\000\000@\000\000@@\000\000\200@\000\000\240@\000\000\300@\000\000\340@\000\000\000A\000\000\020A\000\000 A"
  }
)pb";

const char kModel1_with_tensor_values_1to10_as_FLOAT64[] = R"pb(
  tensor {
    length: 10
    encrypted: false
    dimensions: 10
    type { type: FLOAT64 byte_order: LITTLE_ENDIAN_ORDER fortran_order: False }
    value: "\000\000\000\000\000\000\360?\000\000\000\000\000\000\000@\000\000\000\000\000\000\010@\000\000\000\000\000\000\020@\000\000\000\000\000\000\024@\000\000\000\000\000\000\030@\000\000\000\000\000\000\034@\000\000\000\000\000\000 @\000\000\000\000\000\000\"@\000\000\000\000\000\000$@"
  }
)pb";

class FederatedAverageTest : public ::testing::Test {};

TEST_F(FederatedAverageTest, CorrectAverageUINT16) {
  auto model1 =
      ParseTextOrDie<Model>(kModel1_with_tensor_values_1to10_as_UINT16);
  auto model2 =
      ParseTextOrDie<Model>(kModel1_with_tensor_values_1to10_as_UINT16);
  auto expected =
      ParseTextOrDie<Model>(kModel1_with_tensor_values_1to10_as_UINT16);

  // CAUTION! Since the expected values are of type uint16 there is no
  // precision. Therefore, everything is rounded down to the closest / smallest
  // integer:
  //    uint16(0.5 * 1) + uint16(0.5 * 1) = uint16(0.5) + uint16(0.5) = 0
  //    uint16(0.5 * 9) + uint16(0.5 * 9) = uint16(4.5) + uint16(4.5) = 8
  std::vector<unsigned short> expected_values{0, 2, 2, 4, 4, 6, 6, 8, 8, 10};
  auto serialized_tensor = metisfl::proto::SerializeTensor(expected_values);
  std::string serialized_tensor_str(serialized_tensor.begin(),
                                    serialized_tensor.end());
  *expected.mutable_tensors(0)->mutable_value() = serialized_tensor_str;

  std::vector seq1({std::make_pair<const Model *, double>(&model1, 0.5)});
  std::vector seq2({std::make_pair<const Model *, double>(&model2, 0.5)});
  std::vector to_aggregate({seq1, seq2});

  FederatedAverage avg = FederatedAverage<unsigned short>();
  Model averaged = avg.Aggregate(to_aggregate);

  auto aggregated_value_serialized = averaged.model().tensors().at(0).value();
  auto num_values = averaged.model().tensors().at(0).length();
  metisfl::proto::PrintSerializedTensor<unsigned short>(
      aggregated_value_serialized, num_values);

  EXPECT_THAT(averaged.model(), EqualsProto(expected));
}

TEST_F(FederatedAverageTest, CorrectAverageINT32) {
  auto model1 =
      ParseTextOrDie<Model>(kModel1_with_tensor_values_1to10_as_INT32);
  auto model2 =
      ParseTextOrDie<Model>(kModel1_with_tensor_values_1to10_as_INT32);

  auto expected =
      ParseTextOrDie<Model>(kModel1_with_tensor_values_1to10_as_INT32);
  // CAUTION! Since the expected values are of type int32 there is no precision.
  // Therefore, similar to uint16, everything is rounded down to the closest
  // integer:
  //    uint32(0.5 * 1) + uint32(0.5 * 1) = uint32(0.5) + uint32(0.5) = 0
  //    uint32(0.5 * 9) + uint32(0.5 * 9) = uint32(4.5) + uint32(4.5) = 8
  std::vector<signed int> expected_values{0, 2, 2, 4, 4, 6, 6, 8, 8, 10};
  auto serialized_tensor = metisfl::proto::SerializeTensor(expected_values);
  std::string serialized_tensor_str(serialized_tensor.begin(),
                                    serialized_tensor.end());
  *expected.mutable_tensors(0)->mutable_value() = serialized_tensor_str;

  std::vector seq1({std::make_pair<const Model *, double>(&model1, 0.5)});
  std::vector seq2({std::make_pair<const Model *, double>(&model2, 0.5)});
  std::vector to_aggregate({seq1, seq2});

  FederatedAverage avg = FederatedAverage<unsigned int>();
  Model averaged = avg.Aggregate(to_aggregate);

  auto aggregated_value_serialized = averaged.model().tensors().at(0).value();
  auto num_values = averaged.model().tensors().at(0).length();
  metisfl::proto::PrintSerializedTensor<signed int>(aggregated_value_serialized,
                                                    num_values);

  // The aggregated value should be equal with the half of models sum.
  // Therefore, the global model must be equal to either model1 or model2.
  EXPECT_THAT(averaged.model(), EqualsProto(expected));
}

TEST_F(FederatedAverageTest, CorrectAverageFLOAT32) {
  auto model1 =
      ParseTextOrDie<Model>(kModel1_with_tensor_values_1to10_as_FLOAT32);
  auto model2 =
      ParseTextOrDie<Model>(kModel1_with_tensor_values_1to10_as_FLOAT32);

  std::vector seq1({std::make_pair<const Model *, double>(&model1, 0.5)});
  std::vector seq2({std::make_pair<const Model *, double>(&model2, 0.5)});
  std::vector to_aggregate({seq1, seq2});

  FederatedAverage avg = FederatedAverage<float>();
  Model averaged = avg.Aggregate(to_aggregate);

  auto aggregated_value_serialized = averaged.model().tensors().at(0).value();
  auto num_values = averaged.model().tensors().at(0).length();
  metisfl::proto::PrintSerializedTensor<float>(aggregated_value_serialized,
                                               num_values);
  EXPECT_THAT(averaged.model(), EqualsProto(model1));
}

TEST_F(FederatedAverageTest, CorrectAverageFLOAT64) {
  auto model1 =
      ParseTextOrDie<Model>(kModel1_with_tensor_values_1to10_as_FLOAT64);
  auto model2 =
      ParseTextOrDie<Model>(kModel1_with_tensor_values_1to10_as_FLOAT64);

  std::vector seq1({std::make_pair<const Model *, double>(&model1, 0.5)});
  std::vector seq2({std::make_pair<const Model *, double>(&model2, 0.5)});
  std::vector to_aggregate({seq1, seq2});

  FederatedAverage avg = FederatedAverage<double>();
  Model averaged = avg.Aggregate(to_aggregate);
  auto aggregated_value_serialized = averaged.model().tensors().at(0).value();
  auto num_values = averaged.model().tensors().at(0).length();
  metisfl::proto::PrintSerializedTensor<double>(aggregated_value_serialized,
                                                num_values);

  // The aggregated value should be equal with the half of models sum.
  // Therefore, the global model must be equal to either model1 or model2.
  EXPECT_THAT(averaged, EqualsProto(model1));
}

}  // namespace
}  // namespace metisfl::controller