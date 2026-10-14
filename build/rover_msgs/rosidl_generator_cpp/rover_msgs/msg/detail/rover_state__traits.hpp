// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from rover_msgs:msg/RoverState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rover_msgs/msg/rover_state.hpp"


#ifndef ROVER_MSGS__MSG__DETAIL__ROVER_STATE__TRAITS_HPP_
#define ROVER_MSGS__MSG__DETAIL__ROVER_STATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "rover_msgs/msg/detail/rover_state__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'timestamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace rover_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const RoverState & msg,
  std::ostream & out)
{
  out << "{";
  // member: timestamp
  {
    out << "timestamp: ";
    to_flow_style_yaml(msg.timestamp, out);
    out << ", ";
  }

  // member: current_state
  {
    out << "current_state: ";
    rosidl_generator_traits::value_to_yaml(msg.current_state, out);
    out << ", ";
  }

  // member: current_linear_speed
  {
    out << "current_linear_speed: ";
    rosidl_generator_traits::value_to_yaml(msg.current_linear_speed, out);
    out << ", ";
  }

  // member: current_angular_speed
  {
    out << "current_angular_speed: ";
    rosidl_generator_traits::value_to_yaml(msg.current_angular_speed, out);
    out << ", ";
  }

  // member: emergency_stop_active
  {
    out << "emergency_stop_active: ";
    rosidl_generator_traits::value_to_yaml(msg.emergency_stop_active, out);
    out << ", ";
  }

  // member: motor_enabled
  {
    out << "motor_enabled: ";
    rosidl_generator_traits::value_to_yaml(msg.motor_enabled, out);
    out << ", ";
  }

  // member: watchdog_active
  {
    out << "watchdog_active: ";
    rosidl_generator_traits::value_to_yaml(msg.watchdog_active, out);
    out << ", ";
  }

  // member: status_message
  {
    out << "status_message: ";
    rosidl_generator_traits::value_to_yaml(msg.status_message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const RoverState & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: timestamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "timestamp:\n";
    to_block_style_yaml(msg.timestamp, out, indentation + 2);
  }

  // member: current_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "current_state: ";
    rosidl_generator_traits::value_to_yaml(msg.current_state, out);
    out << "\n";
  }

  // member: current_linear_speed
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "current_linear_speed: ";
    rosidl_generator_traits::value_to_yaml(msg.current_linear_speed, out);
    out << "\n";
  }

  // member: current_angular_speed
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "current_angular_speed: ";
    rosidl_generator_traits::value_to_yaml(msg.current_angular_speed, out);
    out << "\n";
  }

  // member: emergency_stop_active
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "emergency_stop_active: ";
    rosidl_generator_traits::value_to_yaml(msg.emergency_stop_active, out);
    out << "\n";
  }

  // member: motor_enabled
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "motor_enabled: ";
    rosidl_generator_traits::value_to_yaml(msg.motor_enabled, out);
    out << "\n";
  }

  // member: watchdog_active
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "watchdog_active: ";
    rosidl_generator_traits::value_to_yaml(msg.watchdog_active, out);
    out << "\n";
  }

  // member: status_message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status_message: ";
    rosidl_generator_traits::value_to_yaml(msg.status_message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const RoverState & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace rover_msgs

namespace rosidl_generator_traits
{

[[deprecated("use rover_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const rover_msgs::msg::RoverState & msg,
  std::ostream & out, size_t indentation = 0)
{
  rover_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use rover_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const rover_msgs::msg::RoverState & msg)
{
  return rover_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<rover_msgs::msg::RoverState>()
{
  return "rover_msgs::msg::RoverState";
}

template<>
inline const char * name<rover_msgs::msg::RoverState>()
{
  return "rover_msgs/msg/RoverState";
}

template<>
struct has_fixed_size<rover_msgs::msg::RoverState>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<rover_msgs::msg::RoverState>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<rover_msgs::msg::RoverState>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ROVER_MSGS__MSG__DETAIL__ROVER_STATE__TRAITS_HPP_
