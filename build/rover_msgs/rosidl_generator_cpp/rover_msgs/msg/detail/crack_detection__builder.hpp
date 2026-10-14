// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from rover_msgs:msg/CrackDetection.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rover_msgs/msg/crack_detection.hpp"


#ifndef ROVER_MSGS__MSG__DETAIL__CRACK_DETECTION__BUILDER_HPP_
#define ROVER_MSGS__MSG__DETAIL__CRACK_DETECTION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "rover_msgs/msg/detail/crack_detection__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace rover_msgs
{

namespace msg
{

namespace builder
{

class Init_CrackDetection_severity_label
{
public:
  explicit Init_CrackDetection_severity_label(::rover_msgs::msg::CrackDetection & msg)
  : msg_(msg)
  {}
  ::rover_msgs::msg::CrackDetection severity_label(::rover_msgs::msg::CrackDetection::_severity_label_type arg)
  {
    msg_.severity_label = std::move(arg);
    return std::move(msg_);
  }

private:
  ::rover_msgs::msg::CrackDetection msg_;
};

class Init_CrackDetection_estimated_pixel_width
{
public:
  explicit Init_CrackDetection_estimated_pixel_width(::rover_msgs::msg::CrackDetection & msg)
  : msg_(msg)
  {}
  Init_CrackDetection_severity_label estimated_pixel_width(::rover_msgs::msg::CrackDetection::_estimated_pixel_width_type arg)
  {
    msg_.estimated_pixel_width = std::move(arg);
    return Init_CrackDetection_severity_label(msg_);
  }

private:
  ::rover_msgs::msg::CrackDetection msg_;
};

class Init_CrackDetection_estimated_pixel_length
{
public:
  explicit Init_CrackDetection_estimated_pixel_length(::rover_msgs::msg::CrackDetection & msg)
  : msg_(msg)
  {}
  Init_CrackDetection_estimated_pixel_width estimated_pixel_length(::rover_msgs::msg::CrackDetection::_estimated_pixel_length_type arg)
  {
    msg_.estimated_pixel_length = std::move(arg);
    return Init_CrackDetection_estimated_pixel_width(msg_);
  }

private:
  ::rover_msgs::msg::CrackDetection msg_;
};

class Init_CrackDetection_center_y
{
public:
  explicit Init_CrackDetection_center_y(::rover_msgs::msg::CrackDetection & msg)
  : msg_(msg)
  {}
  Init_CrackDetection_estimated_pixel_length center_y(::rover_msgs::msg::CrackDetection::_center_y_type arg)
  {
    msg_.center_y = std::move(arg);
    return Init_CrackDetection_estimated_pixel_length(msg_);
  }

private:
  ::rover_msgs::msg::CrackDetection msg_;
};

class Init_CrackDetection_center_x
{
public:
  explicit Init_CrackDetection_center_x(::rover_msgs::msg::CrackDetection & msg)
  : msg_(msg)
  {}
  Init_CrackDetection_center_y center_x(::rover_msgs::msg::CrackDetection::_center_x_type arg)
  {
    msg_.center_x = std::move(arg);
    return Init_CrackDetection_center_y(msg_);
  }

private:
  ::rover_msgs::msg::CrackDetection msg_;
};

class Init_CrackDetection_bbox_y_max
{
public:
  explicit Init_CrackDetection_bbox_y_max(::rover_msgs::msg::CrackDetection & msg)
  : msg_(msg)
  {}
  Init_CrackDetection_center_x bbox_y_max(::rover_msgs::msg::CrackDetection::_bbox_y_max_type arg)
  {
    msg_.bbox_y_max = std::move(arg);
    return Init_CrackDetection_center_x(msg_);
  }

private:
  ::rover_msgs::msg::CrackDetection msg_;
};

class Init_CrackDetection_bbox_x_max
{
public:
  explicit Init_CrackDetection_bbox_x_max(::rover_msgs::msg::CrackDetection & msg)
  : msg_(msg)
  {}
  Init_CrackDetection_bbox_y_max bbox_x_max(::rover_msgs::msg::CrackDetection::_bbox_x_max_type arg)
  {
    msg_.bbox_x_max = std::move(arg);
    return Init_CrackDetection_bbox_y_max(msg_);
  }

private:
  ::rover_msgs::msg::CrackDetection msg_;
};

class Init_CrackDetection_bbox_y_min
{
public:
  explicit Init_CrackDetection_bbox_y_min(::rover_msgs::msg::CrackDetection & msg)
  : msg_(msg)
  {}
  Init_CrackDetection_bbox_x_max bbox_y_min(::rover_msgs::msg::CrackDetection::_bbox_y_min_type arg)
  {
    msg_.bbox_y_min = std::move(arg);
    return Init_CrackDetection_bbox_x_max(msg_);
  }

private:
  ::rover_msgs::msg::CrackDetection msg_;
};

class Init_CrackDetection_bbox_x_min
{
public:
  explicit Init_CrackDetection_bbox_x_min(::rover_msgs::msg::CrackDetection & msg)
  : msg_(msg)
  {}
  Init_CrackDetection_bbox_y_min bbox_x_min(::rover_msgs::msg::CrackDetection::_bbox_x_min_type arg)
  {
    msg_.bbox_x_min = std::move(arg);
    return Init_CrackDetection_bbox_y_min(msg_);
  }

private:
  ::rover_msgs::msg::CrackDetection msg_;
};

class Init_CrackDetection_confidence
{
public:
  explicit Init_CrackDetection_confidence(::rover_msgs::msg::CrackDetection & msg)
  : msg_(msg)
  {}
  Init_CrackDetection_bbox_x_min confidence(::rover_msgs::msg::CrackDetection::_confidence_type arg)
  {
    msg_.confidence = std::move(arg);
    return Init_CrackDetection_bbox_x_min(msg_);
  }

private:
  ::rover_msgs::msg::CrackDetection msg_;
};

class Init_CrackDetection_crack_detected
{
public:
  explicit Init_CrackDetection_crack_detected(::rover_msgs::msg::CrackDetection & msg)
  : msg_(msg)
  {}
  Init_CrackDetection_confidence crack_detected(::rover_msgs::msg::CrackDetection::_crack_detected_type arg)
  {
    msg_.crack_detected = std::move(arg);
    return Init_CrackDetection_confidence(msg_);
  }

private:
  ::rover_msgs::msg::CrackDetection msg_;
};

class Init_CrackDetection_timestamp
{
public:
  Init_CrackDetection_timestamp()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CrackDetection_crack_detected timestamp(::rover_msgs::msg::CrackDetection::_timestamp_type arg)
  {
    msg_.timestamp = std::move(arg);
    return Init_CrackDetection_crack_detected(msg_);
  }

private:
  ::rover_msgs::msg::CrackDetection msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::rover_msgs::msg::CrackDetection>()
{
  return rover_msgs::msg::builder::Init_CrackDetection_timestamp();
}

}  // namespace rover_msgs

#endif  // ROVER_MSGS__MSG__DETAIL__CRACK_DETECTION__BUILDER_HPP_
