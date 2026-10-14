// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from rover_msgs:msg/InspectionResult.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rover_msgs/msg/inspection_result.h"


#ifndef ROVER_MSGS__MSG__DETAIL__INSPECTION_RESULT__STRUCT_H_
#define ROVER_MSGS__MSG__DETAIL__INSPECTION_RESULT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'timestamp'
#include "builtin_interfaces/msg/detail/time__struct.h"
// Member 'inspection_id'
// Member 'severity_rating'
// Member 'image_saved_path'
// Member 'rover_state'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/InspectionResult in the package rover_msgs.
typedef struct rover_msgs__msg__InspectionResult
{
  builtin_interfaces__msg__Time timestamp;
  rosidl_runtime_c__String inspection_id;
  bool crack_detected;
  float confidence;
  float crack_length_mm;
  float crack_max_width_mm;
  float crack_avg_width_mm;
  float apparent_depth_mm;
  rosidl_runtime_c__String severity_rating;
  rosidl_runtime_c__String image_saved_path;
  rosidl_runtime_c__String rover_state;
} rover_msgs__msg__InspectionResult;

// Struct for a sequence of rover_msgs__msg__InspectionResult.
typedef struct rover_msgs__msg__InspectionResult__Sequence
{
  rover_msgs__msg__InspectionResult * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} rover_msgs__msg__InspectionResult__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROVER_MSGS__MSG__DETAIL__INSPECTION_RESULT__STRUCT_H_
