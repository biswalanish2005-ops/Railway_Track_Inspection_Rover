// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from rover_msgs:srv/EmergencyStop.idl
// generated code does not contain a copyright notice
#include "rover_msgs/srv/detail/emergency_stop__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `reason`
#include "rosidl_runtime_c/string_functions.h"

bool
rover_msgs__srv__EmergencyStop_Request__init(rover_msgs__srv__EmergencyStop_Request * msg)
{
  if (!msg) {
    return false;
  }
  // set_estop
  // reason
  if (!rosidl_runtime_c__String__init(&msg->reason)) {
    rover_msgs__srv__EmergencyStop_Request__fini(msg);
    return false;
  }
  return true;
}

void
rover_msgs__srv__EmergencyStop_Request__fini(rover_msgs__srv__EmergencyStop_Request * msg)
{
  if (!msg) {
    return;
  }
  // set_estop
  // reason
  rosidl_runtime_c__String__fini(&msg->reason);
}

bool
rover_msgs__srv__EmergencyStop_Request__are_equal(const rover_msgs__srv__EmergencyStop_Request * lhs, const rover_msgs__srv__EmergencyStop_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // set_estop
  if (lhs->set_estop != rhs->set_estop) {
    return false;
  }
  // reason
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->reason), &(rhs->reason)))
  {
    return false;
  }
  return true;
}

bool
rover_msgs__srv__EmergencyStop_Request__copy(
  const rover_msgs__srv__EmergencyStop_Request * input,
  rover_msgs__srv__EmergencyStop_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // set_estop
  output->set_estop = input->set_estop;
  // reason
  if (!rosidl_runtime_c__String__copy(
      &(input->reason), &(output->reason)))
  {
    return false;
  }
  return true;
}

rover_msgs__srv__EmergencyStop_Request *
rover_msgs__srv__EmergencyStop_Request__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  rover_msgs__srv__EmergencyStop_Request * msg = (rover_msgs__srv__EmergencyStop_Request *)allocator.allocate(sizeof(rover_msgs__srv__EmergencyStop_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(rover_msgs__srv__EmergencyStop_Request));
  bool success = rover_msgs__srv__EmergencyStop_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
rover_msgs__srv__EmergencyStop_Request__destroy(rover_msgs__srv__EmergencyStop_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    rover_msgs__srv__EmergencyStop_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
rover_msgs__srv__EmergencyStop_Request__Sequence__init(rover_msgs__srv__EmergencyStop_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  rover_msgs__srv__EmergencyStop_Request * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(rover_msgs__srv__EmergencyStop_Request)) {
      return false;
    }
    data = (rover_msgs__srv__EmergencyStop_Request *)allocator.zero_allocate(size, sizeof(rover_msgs__srv__EmergencyStop_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = rover_msgs__srv__EmergencyStop_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        rover_msgs__srv__EmergencyStop_Request__fini(&data[i - 1]);
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
rover_msgs__srv__EmergencyStop_Request__Sequence__fini(rover_msgs__srv__EmergencyStop_Request__Sequence * array)
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
      rover_msgs__srv__EmergencyStop_Request__fini(&array->data[i]);
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

rover_msgs__srv__EmergencyStop_Request__Sequence *
rover_msgs__srv__EmergencyStop_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  rover_msgs__srv__EmergencyStop_Request__Sequence * array = (rover_msgs__srv__EmergencyStop_Request__Sequence *)allocator.allocate(sizeof(rover_msgs__srv__EmergencyStop_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = rover_msgs__srv__EmergencyStop_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
rover_msgs__srv__EmergencyStop_Request__Sequence__destroy(rover_msgs__srv__EmergencyStop_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    rover_msgs__srv__EmergencyStop_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
rover_msgs__srv__EmergencyStop_Request__Sequence__are_equal(const rover_msgs__srv__EmergencyStop_Request__Sequence * lhs, const rover_msgs__srv__EmergencyStop_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!rover_msgs__srv__EmergencyStop_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
rover_msgs__srv__EmergencyStop_Request__Sequence__copy(
  const rover_msgs__srv__EmergencyStop_Request__Sequence * input,
  rover_msgs__srv__EmergencyStop_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(rover_msgs__srv__EmergencyStop_Request)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(rover_msgs__srv__EmergencyStop_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    rover_msgs__srv__EmergencyStop_Request * data =
      (rover_msgs__srv__EmergencyStop_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!rover_msgs__srv__EmergencyStop_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          rover_msgs__srv__EmergencyStop_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!rover_msgs__srv__EmergencyStop_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
rover_msgs__srv__EmergencyStop_Response__init(rover_msgs__srv__EmergencyStop_Response * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    rover_msgs__srv__EmergencyStop_Response__fini(msg);
    return false;
  }
  return true;
}

void
rover_msgs__srv__EmergencyStop_Response__fini(rover_msgs__srv__EmergencyStop_Response * msg)
{
  if (!msg) {
    return;
  }
  // success
  // message
  rosidl_runtime_c__String__fini(&msg->message);
}

bool
rover_msgs__srv__EmergencyStop_Response__are_equal(const rover_msgs__srv__EmergencyStop_Response * lhs, const rover_msgs__srv__EmergencyStop_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->message), &(rhs->message)))
  {
    return false;
  }
  return true;
}

bool
rover_msgs__srv__EmergencyStop_Response__copy(
  const rover_msgs__srv__EmergencyStop_Response * input,
  rover_msgs__srv__EmergencyStop_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  // message
  if (!rosidl_runtime_c__String__copy(
      &(input->message), &(output->message)))
  {
    return false;
  }
  return true;
}

rover_msgs__srv__EmergencyStop_Response *
rover_msgs__srv__EmergencyStop_Response__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  rover_msgs__srv__EmergencyStop_Response * msg = (rover_msgs__srv__EmergencyStop_Response *)allocator.allocate(sizeof(rover_msgs__srv__EmergencyStop_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(rover_msgs__srv__EmergencyStop_Response));
  bool success = rover_msgs__srv__EmergencyStop_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
rover_msgs__srv__EmergencyStop_Response__destroy(rover_msgs__srv__EmergencyStop_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    rover_msgs__srv__EmergencyStop_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
rover_msgs__srv__EmergencyStop_Response__Sequence__init(rover_msgs__srv__EmergencyStop_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  rover_msgs__srv__EmergencyStop_Response * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(rover_msgs__srv__EmergencyStop_Response)) {
      return false;
    }
    data = (rover_msgs__srv__EmergencyStop_Response *)allocator.zero_allocate(size, sizeof(rover_msgs__srv__EmergencyStop_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = rover_msgs__srv__EmergencyStop_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        rover_msgs__srv__EmergencyStop_Response__fini(&data[i - 1]);
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
rover_msgs__srv__EmergencyStop_Response__Sequence__fini(rover_msgs__srv__EmergencyStop_Response__Sequence * array)
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
      rover_msgs__srv__EmergencyStop_Response__fini(&array->data[i]);
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

rover_msgs__srv__EmergencyStop_Response__Sequence *
rover_msgs__srv__EmergencyStop_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  rover_msgs__srv__EmergencyStop_Response__Sequence * array = (rover_msgs__srv__EmergencyStop_Response__Sequence *)allocator.allocate(sizeof(rover_msgs__srv__EmergencyStop_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = rover_msgs__srv__EmergencyStop_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
rover_msgs__srv__EmergencyStop_Response__Sequence__destroy(rover_msgs__srv__EmergencyStop_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    rover_msgs__srv__EmergencyStop_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
rover_msgs__srv__EmergencyStop_Response__Sequence__are_equal(const rover_msgs__srv__EmergencyStop_Response__Sequence * lhs, const rover_msgs__srv__EmergencyStop_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!rover_msgs__srv__EmergencyStop_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
rover_msgs__srv__EmergencyStop_Response__Sequence__copy(
  const rover_msgs__srv__EmergencyStop_Response__Sequence * input,
  rover_msgs__srv__EmergencyStop_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(rover_msgs__srv__EmergencyStop_Response)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(rover_msgs__srv__EmergencyStop_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    rover_msgs__srv__EmergencyStop_Response * data =
      (rover_msgs__srv__EmergencyStop_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!rover_msgs__srv__EmergencyStop_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          rover_msgs__srv__EmergencyStop_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!rover_msgs__srv__EmergencyStop_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `info`
#include "service_msgs/msg/detail/service_event_info__functions.h"
// Member `request`
// Member `response`
// already included above
// #include "rover_msgs/srv/detail/emergency_stop__functions.h"

bool
rover_msgs__srv__EmergencyStop_Event__init(rover_msgs__srv__EmergencyStop_Event * msg)
{
  if (!msg) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__init(&msg->info)) {
    rover_msgs__srv__EmergencyStop_Event__fini(msg);
    return false;
  }
  // request
  if (!rover_msgs__srv__EmergencyStop_Request__Sequence__init(&msg->request, 0)) {
    rover_msgs__srv__EmergencyStop_Event__fini(msg);
    return false;
  }
  // response
  if (!rover_msgs__srv__EmergencyStop_Response__Sequence__init(&msg->response, 0)) {
    rover_msgs__srv__EmergencyStop_Event__fini(msg);
    return false;
  }
  return true;
}

void
rover_msgs__srv__EmergencyStop_Event__fini(rover_msgs__srv__EmergencyStop_Event * msg)
{
  if (!msg) {
    return;
  }
  // info
  service_msgs__msg__ServiceEventInfo__fini(&msg->info);
  // request
  rover_msgs__srv__EmergencyStop_Request__Sequence__fini(&msg->request);
  // response
  rover_msgs__srv__EmergencyStop_Response__Sequence__fini(&msg->response);
}

bool
rover_msgs__srv__EmergencyStop_Event__are_equal(const rover_msgs__srv__EmergencyStop_Event * lhs, const rover_msgs__srv__EmergencyStop_Event * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__are_equal(
      &(lhs->info), &(rhs->info)))
  {
    return false;
  }
  // request
  if (!rover_msgs__srv__EmergencyStop_Request__Sequence__are_equal(
      &(lhs->request), &(rhs->request)))
  {
    return false;
  }
  // response
  if (!rover_msgs__srv__EmergencyStop_Response__Sequence__are_equal(
      &(lhs->response), &(rhs->response)))
  {
    return false;
  }
  return true;
}

bool
rover_msgs__srv__EmergencyStop_Event__copy(
  const rover_msgs__srv__EmergencyStop_Event * input,
  rover_msgs__srv__EmergencyStop_Event * output)
{
  if (!input || !output) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__copy(
      &(input->info), &(output->info)))
  {
    return false;
  }
  // request
  if (!rover_msgs__srv__EmergencyStop_Request__Sequence__copy(
      &(input->request), &(output->request)))
  {
    return false;
  }
  // response
  if (!rover_msgs__srv__EmergencyStop_Response__Sequence__copy(
      &(input->response), &(output->response)))
  {
    return false;
  }
  return true;
}

rover_msgs__srv__EmergencyStop_Event *
rover_msgs__srv__EmergencyStop_Event__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  rover_msgs__srv__EmergencyStop_Event * msg = (rover_msgs__srv__EmergencyStop_Event *)allocator.allocate(sizeof(rover_msgs__srv__EmergencyStop_Event), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(rover_msgs__srv__EmergencyStop_Event));
  bool success = rover_msgs__srv__EmergencyStop_Event__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
rover_msgs__srv__EmergencyStop_Event__destroy(rover_msgs__srv__EmergencyStop_Event * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    rover_msgs__srv__EmergencyStop_Event__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
rover_msgs__srv__EmergencyStop_Event__Sequence__init(rover_msgs__srv__EmergencyStop_Event__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  rover_msgs__srv__EmergencyStop_Event * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(rover_msgs__srv__EmergencyStop_Event)) {
      return false;
    }
    data = (rover_msgs__srv__EmergencyStop_Event *)allocator.zero_allocate(size, sizeof(rover_msgs__srv__EmergencyStop_Event), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = rover_msgs__srv__EmergencyStop_Event__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        rover_msgs__srv__EmergencyStop_Event__fini(&data[i - 1]);
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
rover_msgs__srv__EmergencyStop_Event__Sequence__fini(rover_msgs__srv__EmergencyStop_Event__Sequence * array)
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
      rover_msgs__srv__EmergencyStop_Event__fini(&array->data[i]);
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

rover_msgs__srv__EmergencyStop_Event__Sequence *
rover_msgs__srv__EmergencyStop_Event__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  rover_msgs__srv__EmergencyStop_Event__Sequence * array = (rover_msgs__srv__EmergencyStop_Event__Sequence *)allocator.allocate(sizeof(rover_msgs__srv__EmergencyStop_Event__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = rover_msgs__srv__EmergencyStop_Event__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
rover_msgs__srv__EmergencyStop_Event__Sequence__destroy(rover_msgs__srv__EmergencyStop_Event__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    rover_msgs__srv__EmergencyStop_Event__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
rover_msgs__srv__EmergencyStop_Event__Sequence__are_equal(const rover_msgs__srv__EmergencyStop_Event__Sequence * lhs, const rover_msgs__srv__EmergencyStop_Event__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!rover_msgs__srv__EmergencyStop_Event__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
rover_msgs__srv__EmergencyStop_Event__Sequence__copy(
  const rover_msgs__srv__EmergencyStop_Event__Sequence * input,
  rover_msgs__srv__EmergencyStop_Event__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(rover_msgs__srv__EmergencyStop_Event)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(rover_msgs__srv__EmergencyStop_Event);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    rover_msgs__srv__EmergencyStop_Event * data =
      (rover_msgs__srv__EmergencyStop_Event *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!rover_msgs__srv__EmergencyStop_Event__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          rover_msgs__srv__EmergencyStop_Event__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!rover_msgs__srv__EmergencyStop_Event__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
