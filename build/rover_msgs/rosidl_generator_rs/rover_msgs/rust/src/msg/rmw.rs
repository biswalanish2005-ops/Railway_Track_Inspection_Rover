#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "rover_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__rover_msgs__msg__RoverState() -> *const std::ffi::c_void;
}

#[link(name = "rover_msgs__rosidl_generator_c")]
extern "C" {
    fn rover_msgs__msg__RoverState__init(msg: *mut RoverState) -> bool;
    fn rover_msgs__msg__RoverState__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RoverState>, size: usize) -> bool;
    fn rover_msgs__msg__RoverState__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RoverState>);
    fn rover_msgs__msg__RoverState__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RoverState>, out_seq: *mut rosidl_runtime_rs::Sequence<RoverState>) -> bool;
}

// Corresponds to rover_msgs__msg__RoverState
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RoverState {

    // This member is not documented.
    #[allow(missing_docs)]
    pub timestamp: builtin_interfaces::msg::rmw::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub current_state: rosidl_runtime_rs::String,


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
    pub status_message: rosidl_runtime_rs::String,

}



impl Default for RoverState {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !rover_msgs__msg__RoverState__init(&mut msg as *mut _) {
        panic!("Call to rover_msgs__msg__RoverState__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RoverState {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rover_msgs__msg__RoverState__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rover_msgs__msg__RoverState__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rover_msgs__msg__RoverState__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RoverState {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RoverState where Self: Sized {
  const TYPE_NAME: &'static str = "rover_msgs/msg/RoverState";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__rover_msgs__msg__RoverState() }
  }
}


#[link(name = "rover_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__rover_msgs__msg__CrackDetection() -> *const std::ffi::c_void;
}

#[link(name = "rover_msgs__rosidl_generator_c")]
extern "C" {
    fn rover_msgs__msg__CrackDetection__init(msg: *mut CrackDetection) -> bool;
    fn rover_msgs__msg__CrackDetection__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<CrackDetection>, size: usize) -> bool;
    fn rover_msgs__msg__CrackDetection__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<CrackDetection>);
    fn rover_msgs__msg__CrackDetection__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<CrackDetection>, out_seq: *mut rosidl_runtime_rs::Sequence<CrackDetection>) -> bool;
}

// Corresponds to rover_msgs__msg__CrackDetection
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CrackDetection {

    // This member is not documented.
    #[allow(missing_docs)]
    pub timestamp: builtin_interfaces::msg::rmw::Time,


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
    pub severity_label: rosidl_runtime_rs::String,

}



impl Default for CrackDetection {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !rover_msgs__msg__CrackDetection__init(&mut msg as *mut _) {
        panic!("Call to rover_msgs__msg__CrackDetection__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for CrackDetection {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rover_msgs__msg__CrackDetection__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rover_msgs__msg__CrackDetection__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rover_msgs__msg__CrackDetection__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for CrackDetection {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for CrackDetection where Self: Sized {
  const TYPE_NAME: &'static str = "rover_msgs/msg/CrackDetection";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__rover_msgs__msg__CrackDetection() }
  }
}


#[link(name = "rover_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__rover_msgs__msg__InspectionResult() -> *const std::ffi::c_void;
}

#[link(name = "rover_msgs__rosidl_generator_c")]
extern "C" {
    fn rover_msgs__msg__InspectionResult__init(msg: *mut InspectionResult) -> bool;
    fn rover_msgs__msg__InspectionResult__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<InspectionResult>, size: usize) -> bool;
    fn rover_msgs__msg__InspectionResult__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<InspectionResult>);
    fn rover_msgs__msg__InspectionResult__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<InspectionResult>, out_seq: *mut rosidl_runtime_rs::Sequence<InspectionResult>) -> bool;
}

// Corresponds to rover_msgs__msg__InspectionResult
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct InspectionResult {

    // This member is not documented.
    #[allow(missing_docs)]
    pub timestamp: builtin_interfaces::msg::rmw::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub inspection_id: rosidl_runtime_rs::String,


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
    pub severity_rating: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub image_saved_path: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub rover_state: rosidl_runtime_rs::String,

}



impl Default for InspectionResult {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !rover_msgs__msg__InspectionResult__init(&mut msg as *mut _) {
        panic!("Call to rover_msgs__msg__InspectionResult__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for InspectionResult {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rover_msgs__msg__InspectionResult__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rover_msgs__msg__InspectionResult__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rover_msgs__msg__InspectionResult__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for InspectionResult {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for InspectionResult where Self: Sized {
  const TYPE_NAME: &'static str = "rover_msgs/msg/InspectionResult";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__rover_msgs__msg__InspectionResult() }
  }
}


