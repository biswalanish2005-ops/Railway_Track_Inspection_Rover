// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from rover_msgs:msg/CrackDetection.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rover_msgs/msg/crack_detection.h"


#ifndef ROVER_MSGS__MSG__DETAIL__CRACK_DETECTION__STRUCT_H_
#define ROVER_MSGS__MSG__DETAIL__CRACK_DETECTION__STRUCT_H_

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
// Member 'severity_label'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/CrackDetection in the package rover_msgs.
typedef struct rover_msgs__msg__CrackDetection
{
  builtin_interfaces__msg__Time timestamp;
  bool crack_detected;
  float confidence;
  float bbox_x_min;
  float bbox_y_min;
  float bbox_x_max;
  float bbox_y_max;
  float center_x;
  float center_y;
  float estimated_pixel_length;
  float estimated_pixel_width;
  rosidl_runtime_c__String severity_label;
} rover_msgs__msg__CrackDetection;

// Struct for a sequence of rover_msgs__msg__CrackDetection.
typedef struct rover_msgs__msg__CrackDetection__Sequence
{
  rover_msgs__msg__CrackDetection * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} rover_msgs__msg__CrackDetection__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROVER_MSGS__MSG__DETAIL__CRACK_DETECTION__STRUCT_H_
