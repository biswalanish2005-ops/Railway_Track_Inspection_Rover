// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from rover_msgs:msg/InspectionResult.idl
// generated code does not contain a copyright notice

#include "rover_msgs/msg/detail/inspection_result__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_rover_msgs
const rosidl_type_hash_t *
rover_msgs__msg__InspectionResult__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x83, 0xc2, 0xb9, 0x8d, 0x4f, 0x71, 0x59, 0xa5,
      0xa8, 0xb5, 0x7a, 0x19, 0x0b, 0x6e, 0x7c, 0xb5,
      0x3b, 0x22, 0x1e, 0x58, 0xa4, 0xbb, 0x44, 0xb8,
      0xe3, 0x78, 0x3b, 0xa8, 0x08, 0xa8, 0x41, 0x79,
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

static char rover_msgs__msg__InspectionResult__TYPE_NAME[] = "rover_msgs/msg/InspectionResult";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";

// Define type names, field names, and default values
static char rover_msgs__msg__InspectionResult__FIELD_NAME__timestamp[] = "timestamp";
static char rover_msgs__msg__InspectionResult__FIELD_NAME__inspection_id[] = "inspection_id";
static char rover_msgs__msg__InspectionResult__FIELD_NAME__crack_detected[] = "crack_detected";
static char rover_msgs__msg__InspectionResult__FIELD_NAME__confidence[] = "confidence";
static char rover_msgs__msg__InspectionResult__FIELD_NAME__crack_length_mm[] = "crack_length_mm";
static char rover_msgs__msg__InspectionResult__FIELD_NAME__crack_max_width_mm[] = "crack_max_width_mm";
static char rover_msgs__msg__InspectionResult__FIELD_NAME__crack_avg_width_mm[] = "crack_avg_width_mm";
static char rover_msgs__msg__InspectionResult__FIELD_NAME__apparent_depth_mm[] = "apparent_depth_mm";
static char rover_msgs__msg__InspectionResult__FIELD_NAME__severity_rating[] = "severity_rating";
static char rover_msgs__msg__InspectionResult__FIELD_NAME__image_saved_path[] = "image_saved_path";
static char rover_msgs__msg__InspectionResult__FIELD_NAME__rover_state[] = "rover_state";

static rosidl_runtime_c__type_description__Field rover_msgs__msg__InspectionResult__FIELDS[] = {
  {
    {rover_msgs__msg__InspectionResult__FIELD_NAME__timestamp, 9, 9},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__InspectionResult__FIELD_NAME__inspection_id, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__InspectionResult__FIELD_NAME__crack_detected, 14, 14},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__InspectionResult__FIELD_NAME__confidence, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__InspectionResult__FIELD_NAME__crack_length_mm, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__InspectionResult__FIELD_NAME__crack_max_width_mm, 18, 18},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__InspectionResult__FIELD_NAME__crack_avg_width_mm, 18, 18},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__InspectionResult__FIELD_NAME__apparent_depth_mm, 17, 17},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__InspectionResult__FIELD_NAME__severity_rating, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__InspectionResult__FIELD_NAME__image_saved_path, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__InspectionResult__FIELD_NAME__rover_state, 11, 11},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription rover_msgs__msg__InspectionResult__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
rover_msgs__msg__InspectionResult__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {rover_msgs__msg__InspectionResult__TYPE_NAME, 31, 31},
      {rover_msgs__msg__InspectionResult__FIELDS, 11, 11},
    },
    {rover_msgs__msg__InspectionResult__REFERENCED_TYPE_DESCRIPTIONS, 1, 1},
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
  "string inspection_id\n"
  "bool crack_detected\n"
  "float32 confidence\n"
  "float32 crack_length_mm\n"
  "float32 crack_max_width_mm\n"
  "float32 crack_avg_width_mm\n"
  "float32 apparent_depth_mm\n"
  "string severity_rating\n"
  "string image_saved_path\n"
  "string rover_state";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
rover_msgs__msg__InspectionResult__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {rover_msgs__msg__InspectionResult__TYPE_NAME, 31, 31},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 264, 264},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
rover_msgs__msg__InspectionResult__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[2];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 2, 2};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *rover_msgs__msg__InspectionResult__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
