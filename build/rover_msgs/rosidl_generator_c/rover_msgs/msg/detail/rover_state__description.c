// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from rover_msgs:msg/RoverState.idl
// generated code does not contain a copyright notice

#include "rover_msgs/msg/detail/rover_state__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_rover_msgs
const rosidl_type_hash_t *
rover_msgs__msg__RoverState__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x8c, 0xc3, 0xa4, 0x4b, 0x4d, 0x24, 0xfe, 0x0f,
      0x5e, 0x87, 0x78, 0xa6, 0x6c, 0xba, 0xce, 0x49,
      0xf0, 0xb8, 0xf7, 0x77, 0x7f, 0x56, 0xe8, 0x87,
      0xb1, 0xd3, 0x48, 0x64, 0x02, 0xda, 0xf8, 0x2d,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "builtin_interfaces/msg/detail/time__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t builtin_interfaces__msg__Time__EXPECTED_HASH = {1, {
    0xb1, 0x06, 0x23, 0x5e, 0x25, 0xa4, 0xc5, 0xed,
    0x35, 0x09, 0x8a, 0xa0, 0xa6, 0x1a, 0x3e, 0xe9,
    0xc9, 0xb1, 0x8d, 0x19, 0x7f, 0x39, 0x8b, 0x0e,
    0x42, 0x06, 0xce, 0xa9, 0xac, 0xf9, 0xc1, 0x97,
  }};
#endif

static char rover_msgs__msg__RoverState__TYPE_NAME[] = "rover_msgs/msg/RoverState";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";

// Define type names, field names, and default values
static char rover_msgs__msg__RoverState__FIELD_NAME__timestamp[] = "timestamp";
static char rover_msgs__msg__RoverState__FIELD_NAME__current_state[] = "current_state";
static char rover_msgs__msg__RoverState__FIELD_NAME__current_linear_speed[] = "current_linear_speed";
static char rover_msgs__msg__RoverState__FIELD_NAME__current_angular_speed[] = "current_angular_speed";
static char rover_msgs__msg__RoverState__FIELD_NAME__emergency_stop_active[] = "emergency_stop_active";
static char rover_msgs__msg__RoverState__FIELD_NAME__motor_enabled[] = "motor_enabled";
static char rover_msgs__msg__RoverState__FIELD_NAME__watchdog_active[] = "watchdog_active";
static char rover_msgs__msg__RoverState__FIELD_NAME__status_message[] = "status_message";

static rosidl_runtime_c__type_description__Field rover_msgs__msg__RoverState__FIELDS[] = {
  {
    {rover_msgs__msg__RoverState__FIELD_NAME__timestamp, 9, 9},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__RoverState__FIELD_NAME__current_state, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__RoverState__FIELD_NAME__current_linear_speed, 20, 20},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__RoverState__FIELD_NAME__current_angular_speed, 21, 21},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__RoverState__FIELD_NAME__emergency_stop_active, 21, 21},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__RoverState__FIELD_NAME__motor_enabled, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__RoverState__FIELD_NAME__watchdog_active, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__RoverState__FIELD_NAME__status_message, 14, 14},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription rover_msgs__msg__RoverState__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
rover_msgs__msg__RoverState__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {rover_msgs__msg__RoverState__TYPE_NAME, 25, 25},
      {rover_msgs__msg__RoverState__FIELDS, 8, 8},
    },
    {rover_msgs__msg__RoverState__REFERENCED_TYPE_DESCRIPTIONS, 1, 1},
  };
  if (!constructed) {
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "builtin_interfaces/Time timestamp\n"
  "string current_state\n"
  "float32 current_linear_speed\n"
  "float32 current_angular_speed\n"
  "bool emergency_stop_active\n"
  "bool motor_enabled\n"
  "bool watchdog_active\n"
  "string status_message";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
rover_msgs__msg__RoverState__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {rover_msgs__msg__RoverState__TYPE_NAME, 25, 25},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 203, 203},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
rover_msgs__msg__RoverState__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[2];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 2, 2};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *rover_msgs__msg__RoverState__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
