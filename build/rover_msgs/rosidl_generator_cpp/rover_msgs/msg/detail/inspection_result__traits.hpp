// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from rover_msgs:msg/InspectionResult.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rover_msgs/msg/inspection_result.hpp"


#ifndef ROVER_MSGS__MSG__DETAIL__INSPECTION_RESULT__TRAITS_HPP_
#define ROVER_MSGS__MSG__DETAIL__INSPECTION_RESULT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "rover_msgs/msg/detail/inspection_result__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'timestamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace rover_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const InspectionResult & msg,
  std::ostream & out)
{
  out << "{";
  // member: timestamp
  {
    out << "timestamp: ";
    to_flow_style_yaml(msg.timestamp, out);
    out << ", ";
  }

  // member: inspection_id
  {
    out << "inspection_id: ";
    rosidl_generator_traits::value_to_yaml(msg.inspection_id, out);
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

  // member: crack_length_mm
  {
    out << "crack_length_mm: ";
    rosidl_generator_traits::value_to_yaml(msg.crack_length_mm, out);
    out << ", ";
  }

  // member: crack_max_width_mm
  {
    out << "crack_max_width_mm: ";
    rosidl_generator_traits::value_to_yaml(msg.crack_max_width_mm, out);
    out << ", ";
  }

  // member: crack_avg_width_mm
  {
    out << "crack_avg_width_mm: ";
    rosidl_generator_traits::value_to_yaml(msg.crack_avg_width_mm, out);
    out << ", ";
  }

  // member: apparent_depth_mm
  {
    out << "apparent_depth_mm: ";
    rosidl_generator_traits::value_to_yaml(msg.apparent_depth_mm, out);
    out << ", ";
  }

  // member: severity_rating
  {
    out << "severity_rating: ";
    rosidl_generator_traits::value_to_yaml(msg.severity_rating, out);
    out << ", ";
  }

  // member: image_saved_path
  {
    out << "image_saved_path: ";
    rosidl_generator_traits::value_to_yaml(msg.image_saved_path, out);
    out << ", ";
  }

  // member: rover_state
  {
    out << "rover_state: ";
    rosidl_generator_traits::value_to_yaml(msg.rover_state, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const InspectionResult & msg,
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

  // member: inspection_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "inspection_id: ";
    rosidl_generator_traits::value_to_yaml(msg.inspection_id, out);
    out << "\n";
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

  // member: crack_length_mm
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "crack_length_mm: ";
    rosidl_generator_traits::value_to_yaml(msg.crack_length_mm, out);
    out << "\n";
  }

  // member: crack_max_width_mm
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "crack_max_width_mm: ";
    rosidl_generator_traits::value_to_yaml(msg.crack_max_width_mm, out);
    out << "\n";
  }

  // member: crack_avg_width_mm
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "crack_avg_width_mm: ";
    rosidl_generator_traits::value_to_yaml(msg.crack_avg_width_mm, out);
    out << "\n";
  }

  // member: apparent_depth_mm
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "apparent_depth_mm: ";
    rosidl_generator_traits::value_to_yaml(msg.apparent_depth_mm, out);
    out << "\n";
  }

  // member: severity_rating
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "severity_rating: ";
    rosidl_generator_traits::value_to_yaml(msg.severity_rating, out);
    out << "\n";
  }

  // member: image_saved_path
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "image_saved_path: ";
    rosidl_generator_traits::value_to_yaml(msg.image_saved_path, out);
    out << "\n";
  }

  // member: rover_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "rover_state: ";
    rosidl_generator_traits::value_to_yaml(msg.rover_state, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const InspectionResult & msg, bool use_flow_style = false)
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
  const rover_msgs::msg::InspectionResult & msg,
  std::ostream & out, size_t indentation = 0)
{
  rover_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use rover_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const rover_msgs::msg::InspectionResult & msg)
{
  return rover_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<rover_msgs::msg::InspectionResult>()
{
  return "rover_msgs::msg::InspectionResult";
}

template<>
inline const char * name<rover_msgs::msg::InspectionResult>()
{
  return "rover_msgs/msg/InspectionResult";
}

template<>
struct has_fixed_size<rover_msgs::msg::InspectionResult>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<rover_msgs::msg::InspectionResult>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<rover_msgs::msg::InspectionResult>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ROVER_MSGS__MSG__DETAIL__INSPECTION_RESULT__TRAITS_HPP_
