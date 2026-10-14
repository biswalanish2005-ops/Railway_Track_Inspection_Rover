// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from rover_msgs:msg/RoverState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rover_msgs/msg/rover_state.h"


#ifndef ROVER_MSGS__MSG__DETAIL__ROVER_STATE__STRUCT_H_
#define ROVER_MSGS__MSG__DETAIL__ROVER_STATE__STRUCT_H_

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
// Member 'current_state'
// Member 'status_message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/RoverState in the package rover_msgs.
typedef struct rover_msgs__msg__RoverState
{
  builtin_interfaces__msg__Time timestamp;
  rosidl_runtime_c__String current_state;
  float current_linear_speed;
  float current_angular_speed;
  bool emergency_stop_active;
  bool motor_enabled;
  bool watchdog_active;
  rosidl_runtime_c__String status_message;
} rover_msgs__msg__RoverState;

// Struct for a sequence of rover_msgs__msg__RoverState.
typedef struct rover_msgs__msg__RoverState__Sequence
{
  rover_msgs__msg__RoverState * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} rover_msgs__msg__RoverState__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROVER_MSGS__MSG__DETAIL__ROVER_STATE__STRUCT_H_
