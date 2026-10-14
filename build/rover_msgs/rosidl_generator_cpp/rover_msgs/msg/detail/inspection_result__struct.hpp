// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from rover_msgs:msg/InspectionResult.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rover_msgs/msg/inspection_result.hpp"


#ifndef ROVER_MSGS__MSG__DETAIL__INSPECTION_RESULT__STRUCT_HPP_
#define ROVER_MSGS__MSG__DETAIL__INSPECTION_RESULT__STRUCT_HPP_

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
# define DEPRECATED__rover_msgs__msg__InspectionResult __attribute__((deprecated))
#else
# define DEPRECATED__rover_msgs__msg__InspectionResult __declspec(deprecated)
#endif

namespace rover_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct InspectionResult_
{
  using Type = InspectionResult_<ContainerAllocator>;

  explicit InspectionResult_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : timestamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->inspection_id = "";
      this->crack_detected = false;
      this->confidence = 0.0f;
      this->crack_length_mm = 0.0f;
      this->crack_max_width_mm = 0.0f;
      this->crack_avg_width_mm = 0.0f;
      this->apparent_depth_mm = 0.0f;
      this->severity_rating = "";
      this->image_saved_path = "";
      this->rover_state = "";
    }
  }

  explicit InspectionResult_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : timestamp(_alloc, _init),
    inspection_id(_alloc),
    severity_rating(_alloc),
    image_saved_path(_alloc),
    rover_state(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->inspection_id = "";
      this->crack_detected = false;
      this->confidence = 0.0f;
      this->crack_length_mm = 0.0f;
      this->crack_max_width_mm = 0.0f;
      this->crack_avg_width_mm = 0.0f;
      this->apparent_depth_mm = 0.0f;
      this->severity_rating = "";
      this->image_saved_path = "";
      this->rover_state = "";
    }
  }

  // field types and members
  using _timestamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _timestamp_type timestamp;
  using _inspection_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _inspection_id_type inspection_id;
  using _crack_detected_type =
    bool;
  _crack_detected_type crack_detected;
  using _confidence_type =
    float;
  _confidence_type confidence;
  using _crack_length_mm_type =
    float;
  _crack_length_mm_type crack_length_mm;
  using _crack_max_width_mm_type =
    float;
  _crack_max_width_mm_type crack_max_width_mm;
  using _crack_avg_width_mm_type =
    float;
  _crack_avg_width_mm_type crack_avg_width_mm;
  using _apparent_depth_mm_type =
    float;
  _apparent_depth_mm_type apparent_depth_mm;
  using _severity_rating_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _severity_rating_type severity_rating;
  using _image_saved_path_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _image_saved_path_type image_saved_path;
  using _rover_state_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _rover_state_type rover_state;

  // setters for named parameter idiom
  Type & set__timestamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->timestamp = _arg;
    return *this;
  }
  Type & set__inspection_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->inspection_id = _arg;
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
  Type & set__crack_length_mm(
    const float & _arg)
  {
    this->crack_length_mm = _arg;
    return *this;
  }
  Type & set__crack_max_width_mm(
    const float & _arg)
  {
    this->crack_max_width_mm = _arg;
    return *this;
  }
  Type & set__crack_avg_width_mm(
    const float & _arg)
  {
    this->crack_avg_width_mm = _arg;
    return *this;
  }
  Type & set__apparent_depth_mm(
    const float & _arg)
  {
    this->apparent_depth_mm = _arg;
    return *this;
  }
  Type & set__severity_rating(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->severity_rating = _arg;
    return *this;
  }
  Type & set__image_saved_path(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->image_saved_path = _arg;
    return *this;
  }
  Type & set__rover_state(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->rover_state = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    rover_msgs::msg::InspectionResult_<ContainerAllocator> *;
  using ConstRawPtr =
    const rover_msgs::msg::InspectionResult_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<rover_msgs::msg::InspectionResult_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<rover_msgs::msg::InspectionResult_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      rover_msgs::msg::InspectionResult_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<rover_msgs::msg::InspectionResult_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      rover_msgs::msg::InspectionResult_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<rover_msgs::msg::InspectionResult_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<rover_msgs::msg::InspectionResult_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<rover_msgs::msg::InspectionResult_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__rover_msgs__msg__InspectionResult
    std::shared_ptr<rover_msgs::msg::InspectionResult_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__rover_msgs__msg__InspectionResult
    std::shared_ptr<rover_msgs::msg::InspectionResult_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const InspectionResult_ & other) const
  {
    if (this->timestamp != other.timestamp) {
      return false;
    }
    if (this->inspection_id != other.inspection_id) {
      return false;
    }
    if (this->crack_detected != other.crack_detected) {
      return false;
    }
    if (this->confidence != other.confidence) {
      return false;
    }
    if (this->crack_length_mm != other.crack_length_mm) {
      return false;
    }
    if (this->crack_max_width_mm != other.crack_max_width_mm) {
      return false;
    }
    if (this->crack_avg_width_mm != other.crack_avg_width_mm) {
      return false;
    }
    if (this->apparent_depth_mm != other.apparent_depth_mm) {
      return false;
    }
    if (this->severity_rating != other.severity_rating) {
      return false;
    }
    if (this->image_saved_path != other.image_saved_path) {
      return false;
    }
    if (this->rover_state != other.rover_state) {
      return false;
    }
    return true;
  }
  bool operator!=(const InspectionResult_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct InspectionResult_

// alias to use template instance with default allocator
using InspectionResult =
  rover_msgs::msg::InspectionResult_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace rover_msgs

#endif  // ROVER_MSGS__MSG__DETAIL__INSPECTION_RESULT__STRUCT_HPP_
