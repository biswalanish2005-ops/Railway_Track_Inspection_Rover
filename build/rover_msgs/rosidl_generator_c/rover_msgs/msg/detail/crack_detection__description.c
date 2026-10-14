// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from rover_msgs:msg/CrackDetection.idl
// generated code does not contain a copyright notice

#include "rover_msgs/msg/detail/crack_detection__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_rover_msgs
const rosidl_type_hash_t *
rover_msgs__msg__CrackDetection__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x54, 0x55, 0xfd, 0x2e, 0x27, 0xcc, 0x1c, 0xac,
      0x05, 0x8a, 0xe7, 0x4b, 0x47, 0xe1, 0x84, 0x4c,
      0x52, 0xc7, 0xc2, 0xc6, 0x34, 0xa5, 0x82, 0x02,
      0xf3, 0x3d, 0x55, 0xc7, 0x43, 0x60, 0xb2, 0xdd,
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

static char rover_msgs__msg__CrackDetection__TYPE_NAME[] = "rover_msgs/msg/CrackDetection";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";

// Define type names, field names, and default values
static char rover_msgs__msg__CrackDetection__FIELD_NAME__timestamp[] = "timestamp";
static char rover_msgs__msg__CrackDetection__FIELD_NAME__crack_detected[] = "crack_detected";
static char rover_msgs__msg__CrackDetection__FIELD_NAME__confidence[] = "confidence";
static char rover_msgs__msg__CrackDetection__FIELD_NAME__bbox_x_min[] = "bbox_x_min";
static char rover_msgs__msg__CrackDetection__FIELD_NAME__bbox_y_min[] = "bbox_y_min";
static char rover_msgs__msg__CrackDetection__FIELD_NAME__bbox_x_max[] = "bbox_x_max";
static char rover_msgs__msg__CrackDetection__FIELD_NAME__bbox_y_max[] = "bbox_y_max";
static char rover_msgs__msg__CrackDetection__FIELD_NAME__center_x[] = "center_x";
static char rover_msgs__msg__CrackDetection__FIELD_NAME__center_y[] = "center_y";
static char rover_msgs__msg__CrackDetection__FIELD_NAME__estimated_pixel_length[] = "estimated_pixel_length";
static char rover_msgs__msg__CrackDetection__FIELD_NAME__estimated_pixel_width[] = "estimated_pixel_width";
static char rover_msgs__msg__CrackDetection__FIELD_NAME__severity_label[] = "severity_label";

static rosidl_runtime_c__type_description__Field rover_msgs__msg__CrackDetection__FIELDS[] = {
  {
    {rover_msgs__msg__CrackDetection__FIELD_NAME__timestamp, 9, 9},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__CrackDetection__FIELD_NAME__crack_detected, 14, 14},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__CrackDetection__FIELD_NAME__confidence, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__CrackDetection__FIELD_NAME__bbox_x_min, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__CrackDetection__FIELD_NAME__bbox_y_min, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__CrackDetection__FIELD_NAME__bbox_x_max, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__CrackDetection__FIELD_NAME__bbox_y_max, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__CrackDetection__FIELD_NAME__center_x, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__CrackDetection__FIELD_NAME__center_y, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__CrackDetection__FIELD_NAME__estimated_pixel_length, 22, 22},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__CrackDetection__FIELD_NAME__estimated_pixel_width, 21, 21},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {rover_msgs__msg__CrackDetection__FIELD_NAME__severity_label, 14, 14},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription rover_msgs__msg__CrackDetection__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
rover_msgs__msg__CrackDetection__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {rover_msgs__msg__CrackDetection__TYPE_NAME, 29, 29},
      {rover_msgs__msg__CrackDetection__FIELDS, 12, 12},
    },
    {rover_msgs__msg__CrackDetection__REFERENCED_TYPE_DESCRIPTIONS, 1, 1},
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
  "bool crack_detected\n"
  "float32 confidence\n"
  "float32 bbox_x_min\n"
  "float32 bbox_y_min\n"
  "float32 bbox_x_max\n"
  "float32 bbox_y_max\n"
  "float32 center_x\n"
  "float32 center_y\n"
  "float32 estimated_pixel_length\n"
  "float32 estimated_pixel_width\n"
  "string severity_label";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
rover_msgs__msg__CrackDetection__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {rover_msgs__msg__CrackDetection__TYPE_NAME, 29, 29},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 266, 266},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
rover_msgs__msg__CrackDetection__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[2];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 2, 2};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *rover_msgs__msg__CrackDetection__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
