// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from rover_msgs:msg/CrackDetection.idl
// generated code does not contain a copyright notice
#include "rover_msgs/msg/detail/crack_detection__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `timestamp`
#include "builtin_interfaces/msg/detail/time__functions.h"
// Member `severity_label`
#include "rosidl_runtime_c/string_functions.h"

bool
rover_msgs__msg__CrackDetection__init(rover_msgs__msg__CrackDetection * msg)
{
  if (!msg) {
    return false;
  }
  // timestamp
  if (!builtin_interfaces__msg__Time__init(&msg->timestamp)) {
    rover_msgs__msg__CrackDetection__fini(msg);
    return false;
  }
  // crack_detected
  // confidence
  // bbox_x_min
  // bbox_y_min
  // bbox_x_max
  // bbox_y_max
  // center_x
  // center_y
  // estimated_pixel_length
  // estimated_pixel_width
  // severity_label
  if (!rosidl_runtime_c__String__init(&msg->severity_label)) {
    rover_msgs__msg__CrackDetection__fini(msg);
    return false;
  }
  return true;
}

void
rover_msgs__msg__CrackDetection__fini(rover_msgs__msg__CrackDetection * msg)
{
  if (!msg) {
    return;
  }
  // timestamp
  builtin_interfaces__msg__Time__fini(&msg->timestamp);
  // crack_detected
  // confidence
  // bbox_x_min
  // bbox_y_min
  // bbox_x_max
  // bbox_y_max
  // center_x
  // center_y
  // estimated_pixel_length
  // estimated_pixel_width
  // severity_label
  rosidl_runtime_c__String__fini(&msg->severity_label);
}

bool
rover_msgs__msg__CrackDetection__are_equal(const rover_msgs__msg__CrackDetection * lhs, const rover_msgs__msg__CrackDetection * rhs)
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
  // crack_detected
  if (lhs->crack_detected != rhs->crack_detected) {
    return false;
  }
  // confidence
  if (lhs->confidence != rhs->confidence) {
    return false;
  }
  // bbox_x_min
  if (lhs->bbox_x_min != rhs->bbox_x_min) {
    return false;
  }
  // bbox_y_min
  if (lhs->bbox_y_min != rhs->bbox_y_min) {
    return false;
  }
  // bbox_x_max
  if (lhs->bbox_x_max != rhs->bbox_x_max) {
    return false;
  }
  // bbox_y_max
  if (lhs->bbox_y_max != rhs->bbox_y_max) {
    return false;
  }
  // center_x
  if (lhs->center_x != rhs->center_x) {
    return false;
  }
  // center_y
  if (lhs->center_y != rhs->center_y) {
    return false;
  }
  // estimated_pixel_length
  if (lhs->estimated_pixel_length != rhs->estimated_pixel_length) {
    return false;
  }
  // estimated_pixel_width
  if (lhs->estimated_pixel_width != rhs->estimated_pixel_width) {
    return false;
  }
  // severity_label
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->severity_label), &(rhs->severity_label)))
  {
    return false;
  }
  return true;
}

bool
rover_msgs__msg__CrackDetection__copy(
  const rover_msgs__msg__CrackDetection * input,
  rover_msgs__msg__CrackDetection * output)
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
  // crack_detected
  output->crack_detected = input->crack_detected;
  // confidence
  output->confidence = input->confidence;
  // bbox_x_min
  output->bbox_x_min = input->bbox_x_min;
  // bbox_y_min
  output->bbox_y_min = input->bbox_y_min;
  // bbox_x_max
  output->bbox_x_max = input->bbox_x_max;
  // bbox_y_max
  output->bbox_y_max = input->bbox_y_max;
  // center_x
  output->center_x = input->center_x;
  // center_y
  output->center_y = input->center_y;
  // estimated_pixel_length
  output->estimated_pixel_length = input->estimated_pixel_length;
  // estimated_pixel_width
  output->estimated_pixel_width = input->estimated_pixel_width;
  // severity_label
  if (!rosidl_runtime_c__String__copy(
      &(input->severity_label), &(output->severity_label)))
  {
    return false;
  }
  return true;
}

rover_msgs__msg__CrackDetection *
rover_msgs__msg__CrackDetection__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  rover_msgs__msg__CrackDetection * msg = (rover_msgs__msg__CrackDetection *)allocator.allocate(sizeof(rover_msgs__msg__CrackDetection), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(rover_msgs__msg__CrackDetection));
  bool success = rover_msgs__msg__CrackDetection__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
rover_msgs__msg__CrackDetection__destroy(rover_msgs__msg__CrackDetection * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    rover_msgs__msg__CrackDetection__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
rover_msgs__msg__CrackDetection__Sequence__init(rover_msgs__msg__CrackDetection__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  rover_msgs__msg__CrackDetection * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(rover_msgs__msg__CrackDetection)) {
      return false;
    }
    data = (rover_msgs__msg__CrackDetection *)allocator.zero_allocate(size, sizeof(rover_msgs__msg__CrackDetection), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = rover_msgs__msg__CrackDetection__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        rover_msgs__msg__CrackDetection__fini(&data[i - 1]);
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
rover_msgs__msg__CrackDetection__Sequence__fini(rover_msgs__msg__CrackDetection__Sequence * array)
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
      rover_msgs__msg__CrackDetection__fini(&array->data[i]);
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

rover_msgs__msg__CrackDetection__Sequence *
rover_msgs__msg__CrackDetection__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  rover_msgs__msg__CrackDetection__Sequence * array = (rover_msgs__msg__CrackDetection__Sequence *)allocator.allocate(sizeof(rover_msgs__msg__CrackDetection__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = rover_msgs__msg__CrackDetection__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
rover_msgs__msg__CrackDetection__Sequence__destroy(rover_msgs__msg__CrackDetection__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    rover_msgs__msg__CrackDetection__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
rover_msgs__msg__CrackDetection__Sequence__are_equal(const rover_msgs__msg__CrackDetection__Sequence * lhs, const rover_msgs__msg__CrackDetection__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!rover_msgs__msg__CrackDetection__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
rover_msgs__msg__CrackDetection__Sequence__copy(
  const rover_msgs__msg__CrackDetection__Sequence * input,
  rover_msgs__msg__CrackDetection__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(rover_msgs__msg__CrackDetection)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(rover_msgs__msg__CrackDetection);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    rover_msgs__msg__CrackDetection * data =
      (rover_msgs__msg__CrackDetection *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!rover_msgs__msg__CrackDetection__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          rover_msgs__msg__CrackDetection__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!rover_msgs__msg__CrackDetection__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
