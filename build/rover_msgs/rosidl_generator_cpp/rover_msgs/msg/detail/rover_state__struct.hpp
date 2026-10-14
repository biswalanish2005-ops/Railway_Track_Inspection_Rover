// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from rover_msgs:msg/RoverState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rover_msgs/msg/rover_state.hpp"


#ifndef ROVER_MSGS__MSG__DETAIL__ROVER_STATE__STRUCT_HPP_
#define ROVER_MSGS__MSG__DETAIL__ROVER_STATE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'timestamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__rover_msgs__msg__RoverState __attribute__((deprecated))
#else
# define DEPRECATED__rover_msgs__msg__RoverState __declspec(deprecated)
#endif

namespace rover_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct RoverState_
{
  using Type = RoverState_<ContainerAllocator>;

  explicit RoverState_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : timestamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->current_state = "";
      this->current_linear_speed = 0.0f;
      this->current_angular_speed = 0.0f;
      this->emergency_stop_active = false;
      this->motor_enabled = false;
      this->watchdog_active = false;
      this->status_message = "";
    }
  }

  explicit RoverState_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : timestamp(_alloc, _init),
    current_state(_alloc),
    status_message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->current_state = "";
      this->current_linear_speed = 0.0f;
      this->current_angular_speed = 0.0f;
      this->emergency_stop_active = false;
      this->motor_enabled = false;
      this->watchdog_active = false;
      this->status_message = "";
    }
  }

  // field types and members
  using _timestamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _timestamp_type timestamp;
  using _current_state_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _current_state_type current_state;
  using _current_linear_speed_type =
    float;
  _current_linear_speed_type current_linear_speed;
  using _current_angular_speed_type =
    float;
  _current_angular_speed_type current_angular_speed;
  using _emergency_stop_active_type =
    bool;
  _emergency_stop_active_type emergency_stop_active;
  using _motor_enabled_type =
    bool;
  _motor_enabled_type motor_enabled;
  using _watchdog_active_type =
    bool;
  _watchdog_active_type watchdog_active;
  using _status_message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _status_message_type status_message;

  // setters for named parameter idiom
  Type & set__timestamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->timestamp = _arg;
    return *this;
  }
  Type & set__current_state(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->current_state = _arg;
    return *this;
  }
  Type & set__current_linear_speed(
    const float & _arg)
  {
    this->current_linear_speed = _arg;
    return *this;
  }
  Type & set__current_angular_speed(
    const float & _arg)
  {
    this->current_angular_speed = _arg;
    return *this;
  }
  Type & set__emergency_stop_active(
    const bool & _arg)
  {
    this->emergency_stop_active = _arg;
    return *this;
  }
  Type & set__motor_enabled(
    const bool & _arg)
  {
    this->motor_enabled = _arg;
    return *this;
  }
  Type & set__watchdog_active(
    const bool & _arg)
  {
    this->watchdog_active = _arg;
    return *this;
  }
  Type & set__status_message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->status_message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    rover_msgs::msg::RoverState_<ContainerAllocator> *;
  using ConstRawPtr =
    const rover_msgs::msg::RoverState_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<rover_msgs::msg::RoverState_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<rover_msgs::msg::RoverState_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      rover_msgs::msg::RoverState_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<rover_msgs::msg::RoverState_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      rover_msgs::msg::RoverState_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<rover_msgs::msg::RoverState_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<rover_msgs::msg::RoverState_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<rover_msgs::msg::RoverState_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__rover_msgs__msg__RoverState
    std::shared_ptr<rover_msgs::msg::RoverState_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__rover_msgs__msg__RoverState
    std::shared_ptr<rover_msgs::msg::RoverState_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const RoverState_ & other) const
  {
    if (this->timestamp != other.timestamp) {
      return false;
    }
    if (this->current_state != other.current_state) {
      return false;
    }
    if (this->current_linear_speed != other.current_linear_speed) {
      return false;
    }
    if (this->current_angular_speed != other.current_angular_speed) {
      return false;
    }
    if (this->emergency_stop_active != other.emergency_stop_active) {
      return false;
    }
    if (this->motor_enabled != other.motor_enabled) {
      return false;
    }
    if (this->watchdog_active != other.watchdog_active) {
      return false;
    }
    if (this->status_message != other.status_message) {
      return false;
    }
    return true;
  }
  bool operator!=(const RoverState_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct RoverState_

// alias to use template instance with default allocator
using RoverState =
  rover_msgs::msg::RoverState_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace rover_msgs

#endif  // ROVER_MSGS__MSG__DETAIL__ROVER_STATE__STRUCT_HPP_
