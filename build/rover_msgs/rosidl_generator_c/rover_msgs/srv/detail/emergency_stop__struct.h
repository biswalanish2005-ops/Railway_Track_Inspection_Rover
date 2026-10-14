// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from rover_msgs:srv/EmergencyStop.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rover_msgs/srv/emergency_stop.h"


#ifndef ROVER_MSGS__SRV__DETAIL__EMERGENCY_STOP__STRUCT_H_
#define ROVER_MSGS__SRV__DETAIL__EMERGENCY_STOP__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'reason'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/EmergencyStop in the package rover_msgs.
typedef struct rover_msgs__srv__EmergencyStop_Request
{
  bool set_estop;
  rosidl_runtime_c__String reason;
} rover_msgs__srv__EmergencyStop_Request;

// Struct for a sequence of rover_msgs__srv__EmergencyStop_Request.
typedef struct rover_msgs__srv__EmergencyStop_Request__Sequence
{
  rover_msgs__srv__EmergencyStop_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} rover_msgs__srv__EmergencyStop_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/EmergencyStop in the package rover_msgs.
typedef struct rover_msgs__srv__EmergencyStop_Response
{
  bool success;
  rosidl_runtime_c__String message;
} rover_msgs__srv__EmergencyStop_Response;

// Struct for a sequence of rover_msgs__srv__EmergencyStop_Response.
typedef struct rover_msgs__srv__EmergencyStop_Response__Sequence
{
  rover_msgs__srv__EmergencyStop_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} rover_msgs__srv__EmergencyStop_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  rover_msgs__srv__EmergencyStop_Event__request__MAX_SIZE = 1
};
// response
enum
{
  rover_msgs__srv__EmergencyStop_Event__response__MAX_SIZE = 1
};

/// Struct defined in srv/EmergencyStop in the package rover_msgs.
typedef struct rover_msgs__srv__EmergencyStop_Event
{
  service_msgs__msg__ServiceEventInfo info;
  rover_msgs__srv__EmergencyStop_Request__Sequence request;
  rover_msgs__srv__EmergencyStop_Response__Sequence response;
} rover_msgs__srv__EmergencyStop_Event;

// Struct for a sequence of rover_msgs__srv__EmergencyStop_Event.
typedef struct rover_msgs__srv__EmergencyStop_Event__Sequence
{
  rover_msgs__srv__EmergencyStop_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} rover_msgs__srv__EmergencyStop_Event__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROVER_MSGS__SRV__DETAIL__EMERGENCY_STOP__STRUCT_H_
