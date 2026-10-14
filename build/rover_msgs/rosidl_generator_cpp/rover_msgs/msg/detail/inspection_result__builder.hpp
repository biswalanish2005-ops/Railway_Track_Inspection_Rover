// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from rover_msgs:msg/InspectionResult.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rover_msgs/msg/inspection_result.hpp"


#ifndef ROVER_MSGS__MSG__DETAIL__INSPECTION_RESULT__BUILDER_HPP_
#define ROVER_MSGS__MSG__DETAIL__INSPECTION_RESULT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "rover_msgs/msg/detail/inspection_result__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace rover_msgs
{

namespace msg
{

namespace builder
{

class Init_InspectionResult_rover_state
{
public:
  explicit Init_InspectionResult_rover_state(::rover_msgs::msg::InspectionResult & msg)
  : msg_(msg)
  {}
  ::rover_msgs::msg::InspectionResult rover_state(::rover_msgs::msg::InspectionResult::_rover_state_type arg)
  {
    msg_.rover_state = std::move(arg);
    return std::move(msg_);
  }

private:
  ::rover_msgs::msg::InspectionResult msg_;
};

class Init_InspectionResult_image_saved_path
{
public:
  explicit Init_InspectionResult_image_saved_path(::rover_msgs::msg::InspectionResult & msg)
  : msg_(msg)
  {}
  Init_InspectionResult_rover_state image_saved_path(::rover_msgs::msg::InspectionResult::_image_saved_path_type arg)
  {
    msg_.image_saved_path = std::move(arg);
    return Init_InspectionResult_rover_state(msg_);
  }

private:
  ::rover_msgs::msg::InspectionResult msg_;
};

class Init_InspectionResult_severity_rating
{
public:
  explicit Init_InspectionResult_severity_rating(::rover_msgs::msg::InspectionResult & msg)
  : msg_(msg)
  {}
  Init_InspectionResult_image_saved_path severity_rating(::rover_msgs::msg::InspectionResult::_severity_rating_type arg)
  {
    msg_.severity_rating = std::move(arg);
    return Init_InspectionResult_image_saved_path(msg_);
  }

private:
  ::rover_msgs::msg::InspectionResult msg_;
};

class Init_InspectionResult_apparent_depth_mm
{
public:
  explicit Init_InspectionResult_apparent_depth_mm(::rover_msgs::msg::InspectionResult & msg)
  : msg_(msg)
  {}
  Init_InspectionResult_severity_rating apparent_depth_mm(::rover_msgs::msg::InspectionResult::_apparent_depth_mm_type arg)
  {
    msg_.apparent_depth_mm = std::move(arg);
    return Init_InspectionResult_severity_rating(msg_);
  }

private:
  ::rover_msgs::msg::InspectionResult msg_;
};

class Init_InspectionResult_crack_avg_width_mm
{
public:
  explicit Init_InspectionResult_crack_avg_width_mm(::rover_msgs::msg::InspectionResult & msg)
  : msg_(msg)
  {}
  Init_InspectionResult_apparent_depth_mm crack_avg_width_mm(::rover_msgs::msg::InspectionResult::_crack_avg_width_mm_type arg)
  {
    msg_.crack_avg_width_mm = std::move(arg);
    return Init_InspectionResult_apparent_depth_mm(msg_);
  }

private:
  ::rover_msgs::msg::InspectionResult msg_;
};

class Init_InspectionResult_crack_max_width_mm
{
public:
  explicit Init_InspectionResult_crack_max_width_mm(::rover_msgs::msg::InspectionResult & msg)
  : msg_(msg)
  {}
  Init_InspectionResult_crack_avg_width_mm crack_max_width_mm(::rover_msgs::msg::InspectionResult::_crack_max_width_mm_type arg)
  {
    msg_.crack_max_width_mm = std::move(arg);
    return Init_InspectionResult_crack_avg_width_mm(msg_);
  }

private:
  ::rover_msgs::msg::InspectionResult msg_;
};

class Init_InspectionResult_crack_length_mm
{
public:
  explicit Init_InspectionResult_crack_length_mm(::rover_msgs::msg::InspectionResult & msg)
  : msg_(msg)
  {}
  Init_InspectionResult_crack_max_width_mm crack_length_mm(::rover_msgs::msg::InspectionResult::_crack_length_mm_type arg)
  {
    msg_.crack_length_mm = std::move(arg);
    return Init_InspectionResult_crack_max_width_mm(msg_);
  }

private:
  ::rover_msgs::msg::InspectionResult msg_;
};

class Init_InspectionResult_confidence
{
public:
  explicit Init_InspectionResult_confidence(::rover_msgs::msg::InspectionResult & msg)
  : msg_(msg)
  {}
  Init_InspectionResult_crack_length_mm confidence(::rover_msgs::msg::InspectionResult::_confidence_type arg)
  {
    msg_.confidence = std::move(arg);
    return Init_InspectionResult_crack_length_mm(msg_);
  }

private:
  ::rover_msgs::msg::InspectionResult msg_;
};

class Init_InspectionResult_crack_detected
{
public:
  explicit Init_InspectionResult_crack_detected(::rover_msgs::msg::InspectionResult & msg)
  : msg_(msg)
  {}
  Init_InspectionResult_confidence crack_detected(::rover_msgs::msg::InspectionResult::_crack_detected_type arg)
  {
    msg_.crack_detected = std::move(arg);
    return Init_InspectionResult_confidence(msg_);
  }

private:
  ::rover_msgs::msg::InspectionResult msg_;
};

class Init_InspectionResult_inspection_id
{
public:
  explicit Init_InspectionResult_inspection_id(::rover_msgs::msg::InspectionResult & msg)
  : msg_(msg)
  {}
  Init_InspectionResult_crack_detected inspection_id(::rover_msgs::msg::InspectionResult::_inspection_id_type arg)
  {
    msg_.inspection_id = std::move(arg);
    return Init_InspectionResult_crack_detected(msg_);
  }

private:
  ::rover_msgs::msg::InspectionResult msg_;
};

class Init_InspectionResult_timestamp
{
public:
  Init_InspectionResult_timestamp()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_InspectionResult_inspection_id timestamp(::rover_msgs::msg::InspectionResult::_timestamp_type arg)
  {
    msg_.timestamp = std::move(arg);
    return Init_InspectionResult_inspection_id(msg_);
  }

private:
  ::rover_msgs::msg::InspectionResult msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::rover_msgs::msg::InspectionResult>()
{
  return rover_msgs::msg::builder::Init_InspectionResult_timestamp();
}

}  // namespace rover_msgs

#endif  // ROVER_MSGS__MSG__DETAIL__INSPECTION_RESULT__BUILDER_HPP_
