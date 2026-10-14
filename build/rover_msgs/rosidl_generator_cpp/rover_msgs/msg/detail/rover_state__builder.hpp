// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from rover_msgs:msg/RoverState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rover_msgs/msg/rover_state.hpp"


#ifndef ROVER_MSGS__MSG__DETAIL__ROVER_STATE__BUILDER_HPP_
#define ROVER_MSGS__MSG__DETAIL__ROVER_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "rover_msgs/msg/detail/rover_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace rover_msgs
{

namespace msg
{

namespace builder
{

class Init_RoverState_status_message
{
public:
  explicit Init_RoverState_status_message(::rover_msgs::msg::RoverState & msg)
  : msg_(msg)
  {}
  ::rover_msgs::msg::RoverState status_message(::rover_msgs::msg::RoverState::_status_message_type arg)
  {
    msg_.status_message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::rover_msgs::msg::RoverState msg_;
};

class Init_RoverState_watchdog_active
{
public:
  explicit Init_RoverState_watchdog_active(::rover_msgs::msg::RoverState & msg)
  : msg_(msg)
  {}
  Init_RoverState_status_message watchdog_active(::rover_msgs::msg::RoverState::_watchdog_active_type arg)
  {
    msg_.watchdog_active = std::move(arg);
    return Init_RoverState_status_message(msg_);
  }

private:
  ::rover_msgs::msg::RoverState msg_;
};

class Init_RoverState_motor_enabled
{
public:
  explicit Init_RoverState_motor_enabled(::rover_msgs::msg::RoverState & msg)
  : msg_(msg)
  {}
  Init_RoverState_watchdog_active motor_enabled(::rover_msgs::msg::RoverState::_motor_enabled_type arg)
  {
    msg_.motor_enabled = std::move(arg);
    return Init_RoverState_watchdog_active(msg_);
  }

private:
  ::rover_msgs::msg::RoverState msg_;
};

class Init_RoverState_emergency_stop_active
{
public:
  explicit Init_RoverState_emergency_stop_active(::rover_msgs::msg::RoverState & msg)
  : msg_(msg)
  {}
  Init_RoverState_motor_enabled emergency_stop_active(::rover_msgs::msg::RoverState::_emergency_stop_active_type arg)
  {
    msg_.emergency_stop_active = std::move(arg);
    return Init_RoverState_motor_enabled(msg_);
  }

private:
  ::rover_msgs::msg::RoverState msg_;
};

class Init_RoverState_current_angular_speed
{
public:
  explicit Init_RoverState_current_angular_speed(::rover_msgs::msg::RoverState & msg)
  : msg_(msg)
  {}
  Init_RoverState_emergency_stop_active current_angular_speed(::rover_msgs::msg::RoverState::_current_angular_speed_type arg)
  {
    msg_.current_angular_speed = std::move(arg);
    return Init_RoverState_emergency_stop_active(msg_);
  }

private:
  ::rover_msgs::msg::RoverState msg_;
};

class Init_RoverState_current_linear_speed
{
public:
  explicit Init_RoverState_current_linear_speed(::rover_msgs::msg::RoverState & msg)
  : msg_(msg)
  {}
  Init_RoverState_current_angular_speed current_linear_speed(::rover_msgs::msg::RoverState::_current_linear_speed_type arg)
  {
    msg_.current_linear_speed = std::move(arg);
    return Init_RoverState_current_angular_speed(msg_);
  }

private:
  ::rover_msgs::msg::RoverState msg_;
};

class Init_RoverState_current_state
{
public:
  explicit Init_RoverState_current_state(::rover_msgs::msg::RoverState & msg)
  : msg_(msg)
  {}
  Init_RoverState_current_linear_speed current_state(::rover_msgs::msg::RoverState::_current_state_type arg)
  {
    msg_.current_state = std::move(arg);
    return Init_RoverState_current_linear_speed(msg_);
  }

private:
  ::rover_msgs::msg::RoverState msg_;
};

class Init_RoverState_timestamp
{
public:
  Init_RoverState_timestamp()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RoverState_current_state timestamp(::rover_msgs::msg::RoverState::_timestamp_type arg)
  {
    msg_.timestamp = std::move(arg);
    return Init_RoverState_current_state(msg_);
  }

private:
  ::rover_msgs::msg::RoverState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::rover_msgs::msg::RoverState>()
{
  return rover_msgs::msg::builder::Init_RoverState_timestamp();
}

}  // namespace rover_msgs

#endif  // ROVER_MSGS__MSG__DETAIL__ROVER_STATE__BUILDER_HPP_
