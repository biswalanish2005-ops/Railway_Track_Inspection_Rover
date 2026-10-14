// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from rover_msgs:msg/CrackDetection.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rover_msgs/msg/crack_detection.hpp"


#ifndef ROVER_MSGS__MSG__DETAIL__CRACK_DETECTION__STRUCT_HPP_
#define ROVER_MSGS__MSG__DETAIL__CRACK_DETECTION__STRUCT_HPP_

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
# define DEPRECATED__rover_msgs__msg__CrackDetection __attribute__((deprecated))
#else
# define DEPRECATED__rover_msgs__msg__CrackDetection __declspec(deprecated)
#endif

namespace rover_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct CrackDetection_
{
  using Type = CrackDetection_<ContainerAllocator>;

  explicit CrackDetection_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : timestamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->crack_detected = false;
      this->confidence = 0.0f;
      this->bbox_x_min = 0.0f;
      this->bbox_y_min = 0.0f;
      this->bbox_x_max = 0.0f;
      this->bbox_y_max = 0.0f;
      this->center_x = 0.0f;
      this->center_y = 0.0f;
      this->estimated_pixel_length = 0.0f;
      this->estimated_pixel_width = 0.0f;
      this->severity_label = "";
    }
  }

  explicit CrackDetection_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : timestamp(_alloc, _init),
    severity_label(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->crack_detected = false;
      this->confidence = 0.0f;
      this->bbox_x_min = 0.0f;
      this->bbox_y_min = 0.0f;
      this->bbox_x_max = 0.0f;
      this->bbox_y_max = 0.0f;
      this->center_x = 0.0f;
      this->center_y = 0.0f;
      this->estimated_pixel_length = 0.0f;
      this->estimated_pixel_width = 0.0f;
      this->severity_label = "";
    }
  }

  // field types and members
  using _timestamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _timestamp_type timestamp;
  using _crack_detected_type =
    bool;
  _crack_detected_type crack_detected;
  using _confidence_type =
    float;
  _confidence_type confidence;
  using _bbox_x_min_type =
    float;
  _bbox_x_min_type bbox_x_min;
  using _bbox_y_min_type =
    float;
  _bbox_y_min_type bbox_y_min;
  using _bbox_x_max_type =
    float;
  _bbox_x_max_type bbox_x_max;
  using _bbox_y_max_type =
    float;
  _bbox_y_max_type bbox_y_max;
  using _center_x_type =
    float;
  _center_x_type center_x;
  using _center_y_type =
    float;
  _center_y_type center_y;
  using _estimated_pixel_length_type =
    float;
  _estimated_pixel_length_type estimated_pixel_length;
  using _estimated_pixel_width_type =
    float;
  _estimated_pixel_width_type estimated_pixel_width;
  using _severity_label_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _severity_label_type severity_label;

  // setters for named parameter idiom
  Type & set__timestamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->timestamp = _arg;
    return *this;
  }
  Type & set__crack_detected(
    const bool & _arg)
  {
    this->crack_detected = _arg;
    return *this;
  }
  Type & set__confidence(
    const float & _arg)
  {
    this->confidence = _arg;
    return *this;
  }
  Type & set__bbox_x_min(
    const float & _arg)
  {
    this->bbox_x_min = _arg;
    return *this;
  }
  Type & set__bbox_y_min(
    const float & _arg)
  {
    this->bbox_y_min = _arg;
    return *this;
  }
  Type & set__bbox_x_max(
    const float & _arg)
  {
    this->bbox_x_max = _arg;
    return *this;
  }
  Type & set__bbox_y_max(
    const float & _arg)
  {
    this->bbox_y_max = _arg;
    return *this;
  }
  Type & set__center_x(
    const float & _arg)
  {
    this->center_x = _arg;
    return *this;
  }
  Type & set__center_y(
    const float & _arg)
  {
    this->center_y = _arg;
    return *this;
  }
  Type & set__estimated_pixel_length(
    const float & _arg)
  {
    this->estimated_pixel_length = _arg;
    return *this;
  }
  Type & set__estimated_pixel_width(
    const float & _arg)
  {
    this->estimated_pixel_width = _arg;
    return *this;
  }
  Type & set__severity_label(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->severity_label = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    rover_msgs::msg::CrackDetection_<ContainerAllocator> *;
  using ConstRawPtr =
    const rover_msgs::msg::CrackDetection_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<rover_msgs::msg::CrackDetection_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<rover_msgs::msg::CrackDetection_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      rover_msgs::msg::CrackDetection_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<rover_msgs::msg::CrackDetection_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      rover_msgs::msg::CrackDetection_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<rover_msgs::msg::CrackDetection_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<rover_msgs::msg::CrackDetection_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<rover_msgs::msg::CrackDetection_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__rover_msgs__msg__CrackDetection
    std::shared_ptr<rover_msgs::msg::CrackDetection_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__rover_msgs__msg__CrackDetection
    std::shared_ptr<rover_msgs::msg::CrackDetection_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CrackDetection_ & other) const
  {
    if (this->timestamp != other.timestamp) {
      return false;
    }
    if (this->crack_detected != other.crack_detected) {
      return false;
    }
    if (this->confidence != other.confidence) {
      return false;
    }
    if (this->bbox_x_min != other.bbox_x_min) {
      return false;
    }
    if (this->bbox_y_min != other.bbox_y_min) {
      return false;
    }
    if (this->bbox_x_max != other.bbox_x_max) {
      return false;
    }
    if (this->bbox_y_max != other.bbox_y_max) {
      return false;
    }
    if (this->center_x != other.center_x) {
      return false;
    }
    if (this->center_y != other.center_y) {
      return false;
    }
    if (this->estimated_pixel_length != other.estimated_pixel_length) {
      return false;
    }
    if (this->estimated_pixel_width != other.estimated_pixel_width) {
      return false;
    }
    if (this->severity_label != other.severity_label) {
      return false;
    }
    return true;
  }
  bool operator!=(const CrackDetection_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CrackDetection_

// alias to use template instance with default allocator
using CrackDetection =
  rover_msgs::msg::CrackDetection_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace rover_msgs

#endif  // ROVER_MSGS__MSG__DETAIL__CRACK_DETECTION__STRUCT_HPP_
