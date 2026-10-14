// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from rover_msgs:msg/InspectionResult.idl
// generated code does not contain a copyright notice
#include "rover_msgs/msg/detail/inspection_result__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `timestamp`
#include "builtin_interfaces/msg/detail/time__functions.h"
// Member `inspection_id`
// Member `severity_rating`
// Member `image_saved_path`
// Member `rover_state`
#include "rosidl_runtime_c/string_functions.h"

bool
rover_msgs__msg__InspectionResult__init(rover_msgs__msg__InspectionResult * msg)
{
  if (!msg) {
    return false;
  }
  // timestamp
  if (!builtin_interfaces__msg__Time__init(&msg->timestamp)) {
    rover_msgs__msg__InspectionResult__fini(msg);
    return false;
  }
  // inspection_id
  if (!rosidl_runtime_c__String__init(&msg->inspection_id)) {
    rover_msgs__msg__InspectionResult__fini(msg);
    return false;
  }
  // crack_detected
  // confidence
  // crack_length_mm
  // crack_max_width_mm
  // crack_avg_width_mm
  // apparent_depth_mm
  // severity_rating
  if (!rosidl_runtime_c__String__init(&msg->severity_rating)) {
    rover_msgs__msg__InspectionResult__fini(msg);
    return false;
  }
  // image_saved_path
  if (!rosidl_runtime_c__String__init(&msg->image_saved_path)) {
    rover_msgs__msg__InspectionResult__fini(msg);
    return false;
  }
  // rover_state
  if (!rosidl_runtime_c__String__init(&msg->rover_state)) {
    rover_msgs__msg__InspectionResult__fini(msg);
    return false;
  }
  return true;
}

void
rover_msgs__msg__InspectionResult__fini(rover_msgs__msg__InspectionResult * msg)
{
  if (!msg) {
    return;
  }
  // timestamp
  builtin_interfaces__msg__Time__fini(&msg->timestamp);
  // inspection_id
  rosidl_runtime_c__String__fini(&msg->inspection_id);
  // crack_detected
  // confidence
  // crack_length_mm
  // crack_max_width_mm
  // crack_avg_width_mm
  // apparent_depth_mm
  // severity_rating
  rosidl_runtime_c__String__fini(&msg->severity_rating);
  // image_saved_path
  rosidl_runtime_c__String__fini(&msg->image_saved_path);
  // rover_state
  rosidl_runtime_c__String__fini(&msg->rover_state);
}

bool
rover_msgs__msg__InspectionResult__are_equal(const rover_msgs__msg__InspectionResult * lhs, const rover_msgs__msg__InspectionResult * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // timestamp
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->timestamp), &(rhs->timestamp)))
  {
    return false;
  }
  // inspection_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->inspection_id), &(rhs->inspection_id)))
  {
    return false;
  }
  // crack_detected
  if (lhs->crack_detected != rhs->crack_detected) {
    return false;
  }
  // confidence
  if (lhs->confidence != rhs->confidence) {
    return false;
  }
  // crack_length_mm
  if (lhs->crack_length_mm != rhs->crack_length_mm) {
    return false;
  }
  // crack_max_width_mm
  if (lhs->crack_max_width_mm != rhs->crack_max_width_mm) {
    return false;
  }
  // crack_avg_width_mm
  if (lhs->crack_avg_width_mm != rhs->crack_avg_width_mm) {
    return false;
  }
  // apparent_depth_mm
  if (lhs->apparent_depth_mm != rhs->apparent_depth_mm) {
    return false;
  }
  // severity_rating
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->severity_rating), &(rhs->severity_rating)))
  {
    return false;
  }
  // image_saved_path
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->image_saved_path), &(rhs->image_saved_path)))
  {
    return false;
  }
  // rover_state
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->rover_state), &(rhs->rover_state)))
  {
    return false;
  }
  return true;
}

bool
rover_msgs__msg__InspectionResult__copy(
  const rover_msgs__msg__InspectionResult * input,
  rover_msgs__msg__InspectionResult * output)
{
  if (!input || !output) {
    return false;
  }
  // timestamp
  if (!builtin_interfaces__msg__Time__copy(
      &(input->timestamp), &(output->timestamp)))
  {
    return false;
  }
  // inspection_id
  if (!rosidl_runtime_c__String__copy(
      &(input->inspection_id), &(output->inspection_id)))
  {
    return false;
  }
  // crack_detected
  output->crack_detected = input->crack_detected;
  // confidence
  output->confidence = input->confidence;
  // crack_length_mm
  output->crack_length_mm = input->crack_length_mm;
  // crack_max_width_mm
  output->crack_max_width_mm = input->crack_max_width_mm;
  // crack_avg_width_mm
  output->crack_avg_width_mm = input->crack_avg_width_mm;
  // apparent_depth_mm
  output->apparent_depth_mm = input->apparent_depth_mm;
  // severity_rating
  if (!rosidl_runtime_c__String__copy(
      &(input->severity_rating), &(output->severity_rating)))
  {
    return false;
  }
  // image_saved_path
  if (!rosidl_runtime_c__String__copy(
      &(input->image_saved_path), &(output->image_saved_path)))
  {
    return false;
  }
  // rover_state
  if (!rosidl_runtime_c__String__copy(
      &(input->rover_state), &(output->rover_state)))
  {
    return false;
  }
  return true;
}

rover_msgs__msg__InspectionResult *
rover_msgs__msg__InspectionResult__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  rover_msgs__msg__InspectionResult * msg = (rover_msgs__msg__InspectionResult *)allocator.allocate(sizeof(rover_msgs__msg__InspectionResult), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(rover_msgs__msg__InspectionResult));
  bool success = rover_msgs__msg__InspectionResult__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
rover_msgs__msg__InspectionResult__destroy(rover_msgs__msg__InspectionResult * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    rover_msgs__msg__InspectionResult__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
rover_msgs__msg__InspectionResult__Sequence__init(rover_msgs__msg__InspectionResult__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  rover_msgs__msg__InspectionResult * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(rover_msgs__msg__InspectionResult)) {
      return false;
    }
    data = (rover_msgs__msg__InspectionResult *)allocator.zero_allocate(size, sizeof(rover_msgs__msg__InspectionResult), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = rover_msgs__msg__InspectionResult__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        rover_msgs__msg__InspectionResult__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
rover_msgs__msg__InspectionResult__Sequence__fini(rover_msgs__msg__InspectionResult__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      rover_msgs__msg__InspectionResult__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

rover_msgs__msg__InspectionResult__Sequence *
rover_msgs__msg__InspectionResult__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  rover_msgs__msg__InspectionResult__Sequence * array = (rover_msgs__msg__InspectionResult__Sequence *)allocator.allocate(sizeof(rover_msgs__msg__InspectionResult__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = rover_msgs__msg__InspectionResult__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
rover_msgs__msg__InspectionResult__Sequence__destroy(rover_msgs__msg__InspectionResult__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    rover_msgs__msg__InspectionResult__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
rover_msgs__msg__InspectionResult__Sequence__are_equal(const rover_msgs__msg__InspectionResult__Sequence * lhs, const rover_msgs__msg__InspectionResult__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!rover_msgs__msg__InspectionResult__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
rover_msgs__msg__InspectionResult__Sequence__copy(
  const rover_msgs__msg__InspectionResult__Sequence * input,
  rover_msgs__msg__InspectionResult__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(rover_msgs__msg__InspectionResult)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(rover_msgs__msg__InspectionResult);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    rover_msgs__msg__InspectionResult * data =
      (rover_msgs__msg__InspectionResult *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!rover_msgs__msg__InspectionResult__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          rover_msgs__msg__InspectionResult__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!rover_msgs__msg__InspectionResult__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
