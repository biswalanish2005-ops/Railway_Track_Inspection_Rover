// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from rover_msgs:srv/EmergencyStop.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "rover_msgs/srv/detail/emergency_stop__rosidl_typesupport_introspection_c.h"
#include "rover_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "rover_msgs/srv/detail/emergency_stop__functions.h"
#include "rover_msgs/srv/detail/emergency_stop__struct.h"


// Include directives for member types
// Member `reason`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void rover_msgs__srv__EmergencyStop_Request__rosidl_typesupport_introspection_c__EmergencyStop_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  rover_msgs__srv__EmergencyStop_Request__init(message_memory);
}

void rover_msgs__srv__EmergencyStop_Request__rosidl_typesupport_introspection_c__EmergencyStop_Request_fini_function(void * message_memory)
{
  rover_msgs__srv__EmergencyStop_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember rover_msgs__srv__EmergencyStop_Request__rosidl_typesupport_introspection_c__EmergencyStop_Request_message_member_array[2] = {
  {
    "set_estop",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(rover_msgs__srv__EmergencyStop_Request, set_estop),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "reason",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(rover_msgs__srv__EmergencyStop_Request, reason),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers rover_msgs__srv__EmergencyStop_Request__rosidl_typesupport_introspection_c__EmergencyStop_Request_message_members = {
  "rover_msgs__srv",  // message namespace
  "EmergencyStop_Request",  // message name
  2,  // number of fields
  sizeof(rover_msgs__srv__EmergencyStop_Request),
  false,  // has_any_key_member_
  rover_msgs__srv__EmergencyStop_Request__rosidl_typesupport_introspection_c__EmergencyStop_Request_message_member_array,  // message members
  rover_msgs__srv__EmergencyStop_Request__rosidl_typesupport_introspection_c__EmergencyStop_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  rover_msgs__srv__EmergencyStop_Request__rosidl_typesupport_introspection_c__EmergencyStop_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t rover_msgs__srv__EmergencyStop_Request__rosidl_typesupport_introspection_c__EmergencyStop_Request_message_type_support_handle = {
  0,
  &rover_msgs__srv__EmergencyStop_Request__rosidl_typesupport_introspection_c__EmergencyStop_Request_message_members,
  get_message_typesupport_handle_function,
  &rover_msgs__srv__EmergencyStop_Request__get_type_hash,
  &rover_msgs__srv__EmergencyStop_Request__get_type_description,
  &rover_msgs__srv__EmergencyStop_Request__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_rover_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, rover_msgs, srv, EmergencyStop_Request)() {
  if (!rover_msgs__srv__EmergencyStop_Request__rosidl_typesupport_introspection_c__EmergencyStop_Request_message_type_support_handle.typesupport_identifier) {
    rover_msgs__srv__EmergencyStop_Request__rosidl_typesupport_introspection_c__EmergencyStop_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &rover_msgs__srv__EmergencyStop_Request__rosidl_typesupport_introspection_c__EmergencyStop_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "rover_msgs/srv/detail/emergency_stop__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rover_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "rover_msgs/srv/detail/emergency_stop__functions.h"
// already included above
// #include "rover_msgs/srv/detail/emergency_stop__struct.h"


// Include directives for member types
// Member `message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void rover_msgs__srv__EmergencyStop_Response__rosidl_typesupport_introspection_c__EmergencyStop_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  rover_msgs__srv__EmergencyStop_Response__init(message_memory);
}

void rover_msgs__srv__EmergencyStop_Response__rosidl_typesupport_introspection_c__EmergencyStop_Response_fini_function(void * message_memory)
{
  rover_msgs__srv__EmergencyStop_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember rover_msgs__srv__EmergencyStop_Response__rosidl_typesupport_introspection_c__EmergencyStop_Response_message_member_array[2] = {
  {
    "success",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(rover_msgs__srv__EmergencyStop_Response, success),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "message",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(rover_msgs__srv__EmergencyStop_Response, message),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers rover_msgs__srv__EmergencyStop_Response__rosidl_typesupport_introspection_c__EmergencyStop_Response_message_members = {
  "rover_msgs__srv",  // message namespace
  "EmergencyStop_Response",  // message name
  2,  // number of fields
  sizeof(rover_msgs__srv__EmergencyStop_Response),
  false,  // has_any_key_member_
  rover_msgs__srv__EmergencyStop_Response__rosidl_typesupport_introspection_c__EmergencyStop_Response_message_member_array,  // message members
  rover_msgs__srv__EmergencyStop_Response__rosidl_typesupport_introspection_c__EmergencyStop_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  rover_msgs__srv__EmergencyStop_Response__rosidl_typesupport_introspection_c__EmergencyStop_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t rover_msgs__srv__EmergencyStop_Response__rosidl_typesupport_introspection_c__EmergencyStop_Response_message_type_support_handle = {
  0,
  &rover_msgs__srv__EmergencyStop_Response__rosidl_typesupport_introspection_c__EmergencyStop_Response_message_members,
  get_message_typesupport_handle_function,
  &rover_msgs__srv__EmergencyStop_Response__get_type_hash,
  &rover_msgs__srv__EmergencyStop_Response__get_type_description,
  &rover_msgs__srv__EmergencyStop_Response__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_rover_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, rover_msgs, srv, EmergencyStop_Response)() {
  if (!rover_msgs__srv__EmergencyStop_Response__rosidl_typesupport_introspection_c__EmergencyStop_Response_message_type_support_handle.typesupport_identifier) {
    rover_msgs__srv__EmergencyStop_Response__rosidl_typesupport_introspection_c__EmergencyStop_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &rover_msgs__srv__EmergencyStop_Response__rosidl_typesupport_introspection_c__EmergencyStop_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "rover_msgs/srv/detail/emergency_stop__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rover_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "rover_msgs/srv/detail/emergency_stop__functions.h"
// already included above
// #include "rover_msgs/srv/detail/emergency_stop__struct.h"


// Include directives for member types
// Member `info`
#include "service_msgs/msg/service_event_info.h"
// Member `info`
#include "service_msgs/msg/detail/service_event_info__rosidl_typesupport_introspection_c.h"
// Member `request`
// Member `response`
#include "rover_msgs/srv/emergency_stop.h"
// Member `request`
// Member `response`
// already included above
// #include "rover_msgs/srv/detail/emergency_stop__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__EmergencyStop_Event_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  rover_msgs__srv__EmergencyStop_Event__init(message_memory);
}

void rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__EmergencyStop_Event_fini_function(void * message_memory)
{
  rover_msgs__srv__EmergencyStop_Event__fini(message_memory);
}

size_t rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__size_function__EmergencyStop_Event__request(
  const void * untyped_member)
{
  const rover_msgs__srv__EmergencyStop_Request__Sequence * member =
    (const rover_msgs__srv__EmergencyStop_Request__Sequence *)(untyped_member);
  return member->size;
}

const void * rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__get_const_function__EmergencyStop_Event__request(
  const void * untyped_member, size_t index)
{
  const rover_msgs__srv__EmergencyStop_Request__Sequence * member =
    (const rover_msgs__srv__EmergencyStop_Request__Sequence *)(untyped_member);
  return &member->data[index];
}

void * rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__get_function__EmergencyStop_Event__request(
  void * untyped_member, size_t index)
{
  rover_msgs__srv__EmergencyStop_Request__Sequence * member =
    (rover_msgs__srv__EmergencyStop_Request__Sequence *)(untyped_member);
  return &member->data[index];
}

void rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__fetch_function__EmergencyStop_Event__request(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const rover_msgs__srv__EmergencyStop_Request * item =
    ((const rover_msgs__srv__EmergencyStop_Request *)
    rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__get_const_function__EmergencyStop_Event__request(untyped_member, index));
  rover_msgs__srv__EmergencyStop_Request * value =
    (rover_msgs__srv__EmergencyStop_Request *)(untyped_value);
  *value = *item;
}

void rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__assign_function__EmergencyStop_Event__request(
  void * untyped_member, size_t index, const void * untyped_value)
{
  rover_msgs__srv__EmergencyStop_Request * item =
    ((rover_msgs__srv__EmergencyStop_Request *)
    rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__get_function__EmergencyStop_Event__request(untyped_member, index));
  const rover_msgs__srv__EmergencyStop_Request * value =
    (const rover_msgs__srv__EmergencyStop_Request *)(untyped_value);
  *item = *value;
}

bool rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__resize_function__EmergencyStop_Event__request(
  void * untyped_member, size_t size)
{
  rover_msgs__srv__EmergencyStop_Request__Sequence * member =
    (rover_msgs__srv__EmergencyStop_Request__Sequence *)(untyped_member);
  rover_msgs__srv__EmergencyStop_Request__Sequence__fini(member);
  return rover_msgs__srv__EmergencyStop_Request__Sequence__init(member, size);
}

size_t rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__size_function__EmergencyStop_Event__response(
  const void * untyped_member)
{
  const rover_msgs__srv__EmergencyStop_Response__Sequence * member =
    (const rover_msgs__srv__EmergencyStop_Response__Sequence *)(untyped_member);
  return member->size;
}

const void * rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__get_const_function__EmergencyStop_Event__response(
  const void * untyped_member, size_t index)
{
  const rover_msgs__srv__EmergencyStop_Response__Sequence * member =
    (const rover_msgs__srv__EmergencyStop_Response__Sequence *)(untyped_member);
  return &member->data[index];
}

void * rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__get_function__EmergencyStop_Event__response(
  void * untyped_member, size_t index)
{
  rover_msgs__srv__EmergencyStop_Response__Sequence * member =
    (rover_msgs__srv__EmergencyStop_Response__Sequence *)(untyped_member);
  return &member->data[index];
}

void rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__fetch_function__EmergencyStop_Event__response(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const rover_msgs__srv__EmergencyStop_Response * item =
    ((const rover_msgs__srv__EmergencyStop_Response *)
    rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__get_const_function__EmergencyStop_Event__response(untyped_member, index));
  rover_msgs__srv__EmergencyStop_Response * value =
    (rover_msgs__srv__EmergencyStop_Response *)(untyped_value);
  *value = *item;
}

void rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__assign_function__EmergencyStop_Event__response(
  void * untyped_member, size_t index, const void * untyped_value)
{
  rover_msgs__srv__EmergencyStop_Response * item =
    ((rover_msgs__srv__EmergencyStop_Response *)
    rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__get_function__EmergencyStop_Event__response(untyped_member, index));
  const rover_msgs__srv__EmergencyStop_Response * value =
    (const rover_msgs__srv__EmergencyStop_Response *)(untyped_value);
  *item = *value;
}

bool rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__resize_function__EmergencyStop_Event__response(
  void * untyped_member, size_t size)
{
  rover_msgs__srv__EmergencyStop_Response__Sequence * member =
    (rover_msgs__srv__EmergencyStop_Response__Sequence *)(untyped_member);
  rover_msgs__srv__EmergencyStop_Response__Sequence__fini(member);
  return rover_msgs__srv__EmergencyStop_Response__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__EmergencyStop_Event_message_member_array[3] = {
  {
    "info",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(rover_msgs__srv__EmergencyStop_Event, info),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "request",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    1,  // array size
    true,  // is upper bound
    offsetof(rover_msgs__srv__EmergencyStop_Event, request),  // bytes offset in struct
    NULL,  // default value
    rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__size_function__EmergencyStop_Event__request,  // size() function pointer
    rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__get_const_function__EmergencyStop_Event__request,  // get_const(index) function pointer
    rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__get_function__EmergencyStop_Event__request,  // get(index) function pointer
    rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__fetch_function__EmergencyStop_Event__request,  // fetch(index, &value) function pointer
    rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__assign_function__EmergencyStop_Event__request,  // assign(index, value) function pointer
    rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__resize_function__EmergencyStop_Event__request  // resize(index) function pointer
  },
  {
    "response",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    1,  // array size
    true,  // is upper bound
    offsetof(rover_msgs__srv__EmergencyStop_Event, response),  // bytes offset in struct
    NULL,  // default value
    rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__size_function__EmergencyStop_Event__response,  // size() function pointer
    rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__get_const_function__EmergencyStop_Event__response,  // get_const(index) function pointer
    rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__get_function__EmergencyStop_Event__response,  // get(index) function pointer
    rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__fetch_function__EmergencyStop_Event__response,  // fetch(index, &value) function pointer
    rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__assign_function__EmergencyStop_Event__response,  // assign(index, value) function pointer
    rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__resize_function__EmergencyStop_Event__response  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__EmergencyStop_Event_message_members = {
  "rover_msgs__srv",  // message namespace
  "EmergencyStop_Event",  // message name
  3,  // number of fields
  sizeof(rover_msgs__srv__EmergencyStop_Event),
  false,  // has_any_key_member_
  rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__EmergencyStop_Event_message_member_array,  // message members
  rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__EmergencyStop_Event_init_function,  // function to initialize message memory (memory has to be allocated)
  rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__EmergencyStop_Event_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__EmergencyStop_Event_message_type_support_handle = {
  0,
  &rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__EmergencyStop_Event_message_members,
  get_message_typesupport_handle_function,
  &rover_msgs__srv__EmergencyStop_Event__get_type_hash,
  &rover_msgs__srv__EmergencyStop_Event__get_type_description,
  &rover_msgs__srv__EmergencyStop_Event__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_rover_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, rover_msgs, srv, EmergencyStop_Event)() {
  rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__EmergencyStop_Event_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, service_msgs, msg, ServiceEventInfo)();
  rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__EmergencyStop_Event_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, rover_msgs, srv, EmergencyStop_Request)();
  rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__EmergencyStop_Event_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, rover_msgs, srv, EmergencyStop_Response)();
  if (!rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__EmergencyStop_Event_message_type_support_handle.typesupport_identifier) {
    rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__EmergencyStop_Event_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__EmergencyStop_Event_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "rover_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rover_msgs/srv/detail/emergency_stop__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers rover_msgs__srv__detail__emergency_stop__rosidl_typesupport_introspection_c__EmergencyStop_service_members = {
  "rover_msgs__srv",  // service namespace
  "EmergencyStop",  // service name
  // the following fields are initialized below on first access
  NULL,  // request message
  // rover_msgs__srv__detail__emergency_stop__rosidl_typesupport_introspection_c__EmergencyStop_Request_message_type_support_handle,
  NULL,  // response message
  // rover_msgs__srv__detail__emergency_stop__rosidl_typesupport_introspection_c__EmergencyStop_Response_message_type_support_handle
  NULL  // event_message
  // rover_msgs__srv__detail__emergency_stop__rosidl_typesupport_introspection_c__EmergencyStop_Response_message_type_support_handle
};


static rosidl_service_type_support_t rover_msgs__srv__detail__emergency_stop__rosidl_typesupport_introspection_c__EmergencyStop_service_type_support_handle = {
  0,
  &rover_msgs__srv__detail__emergency_stop__rosidl_typesupport_introspection_c__EmergencyStop_service_members,
  get_service_typesupport_handle_function,
  &rover_msgs__srv__EmergencyStop_Request__rosidl_typesupport_introspection_c__EmergencyStop_Request_message_type_support_handle,
  &rover_msgs__srv__EmergencyStop_Response__rosidl_typesupport_introspection_c__EmergencyStop_Response_message_type_support_handle,
  &rover_msgs__srv__EmergencyStop_Event__rosidl_typesupport_introspection_c__EmergencyStop_Event_message_type_support_handle,
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    rover_msgs,
    srv,
    EmergencyStop
  ),
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    rover_msgs,
    srv,
    EmergencyStop
  ),
  &rover_msgs__srv__EmergencyStop__get_type_hash,
  &rover_msgs__srv__EmergencyStop__get_type_description,
  &rover_msgs__srv__EmergencyStop__get_type_description_sources,
};

// Forward declaration of message type support functions for service members
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, rover_msgs, srv, EmergencyStop_Request)(void);

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, rover_msgs, srv, EmergencyStop_Response)(void);

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, rover_msgs, srv, EmergencyStop_Event)(void);

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_rover_msgs
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, rover_msgs, srv, EmergencyStop)(void) {
  if (!rover_msgs__srv__detail__emergency_stop__rosidl_typesupport_introspection_c__EmergencyStop_service_type_support_handle.typesupport_identifier) {
    rover_msgs__srv__detail__emergency_stop__rosidl_typesupport_introspection_c__EmergencyStop_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)rover_msgs__srv__detail__emergency_stop__rosidl_typesupport_introspection_c__EmergencyStop_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, rover_msgs, srv, EmergencyStop_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, rover_msgs, srv, EmergencyStop_Response)()->data;
  }
  if (!service_members->event_members_) {
    service_members->event_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, rover_msgs, srv, EmergencyStop_Event)()->data;
  }

  return &rover_msgs__srv__detail__emergency_stop__rosidl_typesupport_introspection_c__EmergencyStop_service_type_support_handle;
}
