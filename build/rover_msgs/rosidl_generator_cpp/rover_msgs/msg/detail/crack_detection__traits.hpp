// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from rover_msgs:msg/CrackDetection.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rover_msgs/msg/crack_detection.hpp"


#ifndef ROVER_MSGS__MSG__DETAIL__CRACK_DETECTION__TRAITS_HPP_
#define ROVER_MSGS__MSG__DETAIL__CRACK_DETECTION__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "rover_msgs/msg/detail/crack_detection__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'timestamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace rover_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const CrackDetection & msg,
  std::ostream & out)
{
  out << "{";
  // member: timestamp
  {
    out << "timestamp: ";
    to_flow_style_yaml(msg.timestamp, out);
    out << ", ";
  }

  // member: crack_detected
  {
    out << "crack_detected: ";
    rosidl_generator_traits::value_to_yaml(msg.crack_detected, out);
    out << ", ";
  }

  // member: confidence
  {
    out << "confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.confidence, out);
    out << ", ";
  }

  // member: bbox_x_min
  {
    out << "bbox_x_min: ";
    rosidl_generator_traits::value_to_yaml(msg.bbox_x_min, out);
    out << ", ";
  }

  // member: bbox_y_min
  {
    out << "bbox_y_min: ";
    rosidl_generator_traits::value_to_yaml(msg.bbox_y_min, out);
    out << ", ";
  }

  // member: bbox_x_max
  {
    out << "bbox_x_max: ";
    rosidl_generator_traits::value_to_yaml(msg.bbox_x_max, out);
    out << ", ";
  }

  // member: bbox_y_max
  {
    out << "bbox_y_max: ";
    rosidl_generator_traits::value_to_yaml(msg.bbox_y_max, out);
    out << ", ";
  }

  // member: center_x
  {
    out << "center_x: ";
    rosidl_generator_traits::value_to_yaml(msg.center_x, out);
    out << ", ";
  }

  // member: center_y
  {
    out << "center_y: ";
    rosidl_generator_traits::value_to_yaml(msg.center_y, out);
    out << ", ";
  }

  // member: estimated_pixel_length
  {
    out << "estimated_pixel_length: ";
    rosidl_generator_traits::value_to_yaml(msg.estimated_pixel_length, out);
    out << ", ";
  }

  // member: estimated_pixel_width
  {
    out << "estimated_pixel_width: ";
    rosidl_generator_traits::value_to_yaml(msg.estimated_pixel_width, out);
    out << ", ";
  }

  // member: severity_label
  {
    out << "severity_label: ";
    rosidl_generator_traits::value_to_yaml(msg.severity_label, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const CrackDetection & msg,
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

  // member: crack_detected
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "crack_detected: ";
    rosidl_generator_traits::value_to_yaml(msg.crack_detected, out);
    out << "\n";
  }

  // member: confidence
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.confidence, out);
    out << "\n";
  }

  // member: bbox_x_min
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "bbox_x_min: ";
    rosidl_generator_traits::value_to_yaml(msg.bbox_x_min, out);
    out << "\n";
  }

  // member: bbox_y_min
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "bbox_y_min: ";
    rosidl_generator_traits::value_to_yaml(msg.bbox_y_min, out);
    out << "\n";
  }

  // member: bbox_x_max
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "bbox_x_max: ";
    rosidl_generator_traits::value_to_yaml(msg.bbox_x_max, out);
    out << "\n";
  }

  // member: bbox_y_max
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "bbox_y_max: ";
    rosidl_generator_traits::value_to_yaml(msg.bbox_y_max, out);
    out << "\n";
  }

  // member: center_x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "center_x: ";
    rosidl_generator_traits::value_to_yaml(msg.center_x, out);
    out << "\n";
  }

  // member: center_y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "center_y: ";
    rosidl_generator_traits::value_to_yaml(msg.center_y, out);
    out << "\n";
  }

  // member: estimated_pixel_length
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "estimated_pixel_length: ";
    rosidl_generator_traits::value_to_yaml(msg.estimated_pixel_length, out);
    out << "\n";
  }

  // member: estimated_pixel_width
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "estimated_pixel_width: ";
    rosidl_generator_traits::value_to_yaml(msg.estimated_pixel_width, out);
    out << "\n";
  }

  // member: severity_label
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "severity_label: ";
    rosidl_generator_traits::value_to_yaml(msg.severity_label, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const CrackDetection & msg, bool use_flow_style = false)
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
  const rover_msgs::msg::CrackDetection & msg,
  std::ostream & out, size_t indentation = 0)
{
  rover_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use rover_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const rover_msgs::msg::CrackDetection & msg)
{
  return rover_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<rover_msgs::msg::CrackDetection>()
{
  return "rover_msgs::msg::CrackDetection";
}

template<>
inline const char * name<rover_msgs::msg::CrackDetection>()
{
  return "rover_msgs/msg/CrackDetection";
}

template<>
struct has_fixed_size<rover_msgs::msg::CrackDetection>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<rover_msgs::msg::CrackDetection>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<rover_msgs::msg::CrackDetection>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ROVER_MSGS__MSG__DETAIL__CRACK_DETECTION__TRAITS_HPP_
