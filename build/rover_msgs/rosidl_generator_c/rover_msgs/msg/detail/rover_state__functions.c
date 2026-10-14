// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from rover_msgs:msg/RoverState.idl
// generated code does not contain a copyright notice
#include "rover_msgs/msg/detail/rover_state__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `timestamp`
#include "builtin_interfaces/msg/detail/time__functions.h"
// Member `current_state`
// Member `status_message`
#include "rosidl_runtime_c/string_functions.h"

bool
rover_msgs__msg__RoverState__init(rover_msgs__msg__RoverState * msg)
{
  if (!msg) {
    return false;
  }
  // timestamp
  if (!builtin_interfaces__msg__Time__init(&msg->timestamp)) {
    rover_msgs__msg__RoverState__fini(msg);
    return false;
  }
  // current_state
  if (!rosidl_runtime_c__String__init(&msg->current_state)) {
    rover_msgs__msg__RoverState__fini(msg);
    return false;
  }
  // current_linear_speed
  // current_angular_speed
  // emergency_stop_active
  // motor_enabled
  // watchdog_active
  // status_message
  if (!rosidl_runtime_c__String__init(&msg->status_message)) {
    rover_msgs__msg__RoverState__fini(msg);
    return false;
  }
  return true;
}

void
rover_msgs__msg__RoverState__fini(rover_msgs__msg__RoverState * msg)
{
  if (!msg) {
    return;
  }
  // timestamp
  builtin_interfaces__msg__Time__fini(&msg->timestamp);
  // current_state
  rosidl_runtime_c__String__fini(&msg->current_state);
  // current_linear_speed
  // current_angular_speed
  // emergency_stop_active
  // motor_enabled
  // watchdog_active
  // status_message
  rosidl_runtime_c__String__fini(&msg->status_message);
}

bool
rover_msgs__msg__RoverState__are_equal(const rover_msgs__msg__RoverState * lhs, const rover_msgs__msg__RoverState * rhs)
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
  // current_state
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->current_state), &(rhs->current_state)))
  {
    return false;
  }
  // current_linear_speed
  if (lhs->current_linear_speed != rhs->current_linear_speed) {
    return false;
  }
  // current_angular_speed
  if (lhs->current_angular_speed != rhs->current_angular_speed) {
    return false;
  }
  // emergency_stop_active
  if (lhs->emergency_stop_active != rhs->emergency_stop_active) {
    return false;
  }
  // motor_enabled
  if (lhs->motor_enabled != rhs->motor_enabled) {
    return false;
  }
  // watchdog_active
  if (lhs->watchdog_active != rhs->watchdog_active) {
    return false;
  }
  // status_message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->status_message), &(rhs->status_message)))
  {
    return false;
  }
  return true;
}

bool
rover_msgs__msg__RoverState__copy(
  const rover_msgs__msg__RoverState * input,
  rover_msgs__msg__RoverState * output)
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
  // current_state
  if (!rosidl_runtime_c__String__copy(
      &(input->current_state), &(output->current_state)))
  {
    return false;
  }
  // current_linear_speed
  output->current_linear_speed = input->current_linear_speed;
  // current_angular_speed
  output->current_angular_speed = input->current_angular_speed;
  // emergency_stop_active
  output->emergency_stop_active = input->emergency_stop_active;
  // motor_enabled
  output->motor_enabled = input->motor_enabled;
  // watchdog_active
  output->watchdog_active = input->watchdog_active;
  // status_message
  if (!rosidl_runtime_c__String__copy(
      &(input->status_message), &(output->status_message)))
  {
    return false;
  }
  return true;
}

rover_msgs__msg__RoverState *
rover_msgs__msg__RoverState__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  rover_msgs__msg__RoverState * msg = (rover_msgs__msg__RoverState *)allocator.allocate(sizeof(rover_msgs__msg__RoverState), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(rover_msgs__msg__RoverState));
  bool success = rover_msgs__msg__RoverState__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
rover_msgs__msg__RoverState__destroy(rover_msgs__msg__RoverState * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    rover_msgs__msg__RoverState__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
rover_msgs__msg__RoverState__Sequence__init(rover_msgs__msg__RoverState__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  rover_msgs__msg__RoverState * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(rover_msgs__msg__RoverState)) {
      return false;
    }
    data = (rover_msgs__msg__RoverState *)allocator.zero_allocate(size, sizeof(rover_msgs__msg__RoverState), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = rover_msgs__msg__RoverState__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        rover_msgs__msg__RoverState__fini(&data[i - 1]);
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
rover_msgs__msg__RoverState__Sequence__fini(rover_msgs__msg__RoverState__Sequence * array)
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
      rover_msgs__msg__RoverState__fini(&array->data[i]);
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

rover_msgs__msg__RoverState__Sequence *
rover_msgs__msg__RoverState__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  rover_msgs__msg__RoverState__Sequence * array = (rover_msgs__msg__RoverState__Sequence *)allocator.allocate(sizeof(rover_msgs__msg__RoverState__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = rover_msgs__msg__RoverState__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
rover_msgs__msg__RoverState__Sequence__destroy(rover_msgs__msg__RoverState__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    rover_msgs__msg__RoverState__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
rover_msgs__msg__RoverState__Sequence__are_equal(const rover_msgs__msg__RoverState__Sequence * lhs, const rover_msgs__msg__RoverState__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!rover_msgs__msg__RoverState__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
rover_msgs__msg__RoverState__Sequence__copy(
  const rover_msgs__msg__RoverState__Sequence * input,
  rover_msgs__msg__RoverState__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(rover_msgs__msg__RoverState)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(rover_msgs__msg__RoverState);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    rover_msgs__msg__RoverState * data =
      (rover_msgs__msg__RoverState *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!rover_msgs__msg__RoverState__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          rover_msgs__msg__RoverState__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!rover_msgs__msg__RoverState__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
