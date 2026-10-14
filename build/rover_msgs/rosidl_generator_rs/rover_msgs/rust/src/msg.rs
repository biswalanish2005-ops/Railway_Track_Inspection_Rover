#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to rover_msgs__msg__RoverState

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RoverState {

    // This member is not documented.
    #[allow(missing_docs)]
    pub timestamp: builtin_interfaces::msg::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub current_state: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub current_linear_speed: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub current_angular_speed: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub emergency_stop_active: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub motor_enabled: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub watchdog_active: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub status_message: std::string::String,

}



impl Default for RoverState {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::RoverState::default())
  }
}

impl rosidl_runtime_rs::Message for RoverState {
  type RmwMsg = super::msg::rmw::RoverState;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        timestamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.timestamp)).into_owned(),
        current_state: msg.current_state.as_str().into(),
        current_linear_speed: msg.current_linear_speed,
        current_angular_speed: msg.current_angular_speed,
        emergency_stop_active: msg.emergency_stop_active,
        motor_enabled: msg.motor_enabled,
        watchdog_active: msg.watchdog_active,
        status_message: msg.status_message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        timestamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.timestamp)).into_owned(),
        current_state: msg.current_state.as_str().into(),
      current_linear_speed: msg.current_linear_speed,
      current_angular_speed: msg.current_angular_speed,
      emergency_stop_active: msg.emergency_stop_active,
      motor_enabled: msg.motor_enabled,
      watchdog_active: msg.watchdog_active,
        status_message: msg.status_message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      timestamp: builtin_interfaces::msg::Time::from_rmw_message(msg.timestamp),
      current_state: msg.current_state.to_string(),
      current_linear_speed: msg.current_linear_speed,
      current_angular_speed: msg.current_angular_speed,
      emergency_stop_active: msg.emergency_stop_active,
      motor_enabled: msg.motor_enabled,
      watchdog_active: msg.watchdog_active,
      status_message: msg.status_message.to_string(),
    }
  }
}


// Corresponds to rover_msgs__msg__CrackDetection

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CrackDetection {

    // This member is not documented.
    #[allow(missing_docs)]
    pub timestamp: builtin_interfaces::msg::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub crack_detected: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub confidence: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub bbox_x_min: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub bbox_y_min: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub bbox_x_max: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub bbox_y_max: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub center_x: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub center_y: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub estimated_pixel_length: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub estimated_pixel_width: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub severity_label: std::string::String,

}



impl Default for CrackDetection {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::CrackDetection::default())
  }
}

impl rosidl_runtime_rs::Message for CrackDetection {
  type RmwMsg = super::msg::rmw::CrackDetection;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        timestamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.timestamp)).into_owned(),
        crack_detected: msg.crack_detected,
        confidence: msg.confidence,
        bbox_x_min: msg.bbox_x_min,
        bbox_y_min: msg.bbox_y_min,
        bbox_x_max: msg.bbox_x_max,
        bbox_y_max: msg.bbox_y_max,
        center_x: msg.center_x,
        center_y: msg.center_y,
        estimated_pixel_length: msg.estimated_pixel_length,
        estimated_pixel_width: msg.estimated_pixel_width,
        severity_label: msg.severity_label.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        timestamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.timestamp)).into_owned(),
      crack_detected: msg.crack_detected,
      confidence: msg.confidence,
      bbox_x_min: msg.bbox_x_min,
      bbox_y_min: msg.bbox_y_min,
      bbox_x_max: msg.bbox_x_max,
      bbox_y_max: msg.bbox_y_max,
      center_x: msg.center_x,
      center_y: msg.center_y,
      estimated_pixel_length: msg.estimated_pixel_length,
      estimated_pixel_width: msg.estimated_pixel_width,
        severity_label: msg.severity_label.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      timestamp: builtin_interfaces::msg::Time::from_rmw_message(msg.timestamp),
      crack_detected: msg.crack_detected,
      confidence: msg.confidence,
      bbox_x_min: msg.bbox_x_min,
      bbox_y_min: msg.bbox_y_min,
      bbox_x_max: msg.bbox_x_max,
      bbox_y_max: msg.bbox_y_max,
      center_x: msg.center_x,
      center_y: msg.center_y,
      estimated_pixel_length: msg.estimated_pixel_length,
      estimated_pixel_width: msg.estimated_pixel_width,
      severity_label: msg.severity_label.to_string(),
    }
  }
}


// Corresponds to rover_msgs__msg__InspectionResult

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct InspectionResult {

    // This member is not documented.
    #[allow(missing_docs)]
    pub timestamp: builtin_interfaces::msg::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub inspection_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub crack_detected: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub confidence: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub crack_length_mm: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub crack_max_width_mm: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub crack_avg_width_mm: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub apparent_depth_mm: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub severity_rating: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub image_saved_path: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub rover_state: std::string::String,

}



impl Default for InspectionResult {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::InspectionResult::default())
  }
}

impl rosidl_runtime_rs::Message for InspectionResult {
  type RmwMsg = super::msg::rmw::InspectionResult;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        timestamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.timestamp)).into_owned(),
        inspection_id: msg.inspection_id.as_str().into(),
        crack_detected: msg.crack_detected,
        confidence: msg.confidence,
        crack_length_mm: msg.crack_length_mm,
        crack_max_width_mm: msg.crack_max_width_mm,
        crack_avg_width_mm: msg.crack_avg_width_mm,
        apparent_depth_mm: msg.apparent_depth_mm,
        severity_rating: msg.severity_rating.as_str().into(),
        image_saved_path: msg.image_saved_path.as_str().into(),
        rover_state: msg.rover_state.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        timestamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.timestamp)).into_owned(),
        inspection_id: msg.inspection_id.as_str().into(),
      crack_detected: msg.crack_detected,
      confidence: msg.confidence,
      crack_length_mm: msg.crack_length_mm,
      crack_max_width_mm: msg.crack_max_width_mm,
      crack_avg_width_mm: msg.crack_avg_width_mm,
      apparent_depth_mm: msg.apparent_depth_mm,
        severity_rating: msg.severity_rating.as_str().into(),
        image_saved_path: msg.image_saved_path.as_str().into(),
        rover_state: msg.rover_state.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      timestamp: builtin_interfaces::msg::Time::from_rmw_message(msg.timestamp),
      inspection_id: msg.inspection_id.to_string(),
      crack_detected: msg.crack_detected,
      confidence: msg.confidence,
      crack_length_mm: msg.crack_length_mm,
      crack_max_width_mm: msg.crack_max_width_mm,
      crack_avg_width_mm: msg.crack_avg_width_mm,
      apparent_depth_mm: msg.apparent_depth_mm,
      severity_rating: msg.severity_rating.to_string(),
      image_saved_path: msg.image_saved_path.to_string(),
      rover_state: msg.rover_state.to_string(),
    }
  }
}


