// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from rover_msgs:srv/EmergencyStop.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rover_msgs/srv/emergency_stop.hpp"


#ifndef ROVER_MSGS__SRV__DETAIL__EMERGENCY_STOP__BUILDER_HPP_
#define ROVER_MSGS__SRV__DETAIL__EMERGENCY_STOP__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "rover_msgs/srv/detail/emergency_stop__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace rover_msgs
{

namespace srv
{

namespace builder
{

class Init_EmergencyStop_Request_reason
{
public:
  explicit Init_EmergencyStop_Request_reason(::rover_msgs::srv::EmergencyStop_Request & msg)
  : msg_(msg)
  {}
  ::rover_msgs::srv::EmergencyStop_Request reason(::rover_msgs::srv::EmergencyStop_Request::_reason_type arg)
  {
    msg_.reason = std::move(arg);
    return std::move(msg_);
  }

private:
  ::rover_msgs::srv::EmergencyStop_Request msg_;
};

class Init_EmergencyStop_Request_set_estop
{
public:
  Init_EmergencyStop_Request_set_estop()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_EmergencyStop_Request_reason set_estop(::rover_msgs::srv::EmergencyStop_Request::_set_estop_type arg)
  {
    msg_.set_estop = std::move(arg);
    return Init_EmergencyStop_Request_reason(msg_);
  }

private:
  ::rover_msgs::srv::EmergencyStop_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::rover_msgs::srv::EmergencyStop_Request>()
{
  return rover_msgs::srv::builder::Init_EmergencyStop_Request_set_estop();
}

}  // namespace rover_msgs


namespace rover_msgs
{

namespace srv
{

namespace builder
{

class Init_EmergencyStop_Response_message
{
public:
  explicit Init_EmergencyStop_Response_message(::rover_msgs::srv::EmergencyStop_Response & msg)
  : msg_(msg)
  {}
  ::rover_msgs::srv::EmergencyStop_Response message(::rover_msgs::srv::EmergencyStop_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::rover_msgs::srv::EmergencyStop_Response msg_;
};

class Init_EmergencyStop_Response_success
{
public:
  Init_EmergencyStop_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_EmergencyStop_Response_message success(::rover_msgs::srv::EmergencyStop_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_EmergencyStop_Response_message(msg_);
  }

private:
  ::rover_msgs::srv::EmergencyStop_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::rover_msgs::srv::EmergencyStop_Response>()
{
  return rover_msgs::srv::builder::Init_EmergencyStop_Response_success();
}

}  // namespace rover_msgs


namespace rover_msgs
{

namespace srv
{

namespace builder
{

class Init_EmergencyStop_Event_response
{
public:
  explicit Init_EmergencyStop_Event_response(::rover_msgs::srv::EmergencyStop_Event & msg)
  : msg_(msg)
  {}
  ::rover_msgs::srv::EmergencyStop_Event response(::rover_msgs::srv::EmergencyStop_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::rover_msgs::srv::EmergencyStop_Event msg_;
};

class Init_EmergencyStop_Event_request
{
public:
  explicit Init_EmergencyStop_Event_request(::rover_msgs::srv::EmergencyStop_Event & msg)
  : msg_(msg)
  {}
  Init_EmergencyStop_Event_response request(::rover_msgs::srv::EmergencyStop_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_EmergencyStop_Event_response(msg_);
  }

private:
  ::rover_msgs::srv::EmergencyStop_Event msg_;
};

class Init_EmergencyStop_Event_info
{
public:
  Init_EmergencyStop_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_EmergencyStop_Event_request info(::rover_msgs::srv::EmergencyStop_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_EmergencyStop_Event_request(msg_);
  }

private:
  ::rover_msgs::srv::EmergencyStop_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::rover_msgs::srv::EmergencyStop_Event>()
{
  return rover_msgs::srv::builder::Init_EmergencyStop_Event_info();
}

}  // namespace rover_msgs

#endif  // ROVER_MSGS__SRV__DETAIL__EMERGENCY_STOP__BUILDER_HPP_
