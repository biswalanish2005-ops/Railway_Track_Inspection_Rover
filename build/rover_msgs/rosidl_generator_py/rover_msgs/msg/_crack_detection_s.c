// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from rover_msgs:msg/CrackDetection.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "rover_msgs/msg/detail/crack_detection__struct.h"
#include "rover_msgs/msg/detail/crack_detection__functions.h"

#include "rosidl_runtime_c/string.h"
#include "rosidl_runtime_c/string_functions.h"

ROSIDL_GENERATOR_C_IMPORT
bool builtin_interfaces__msg__time__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * builtin_interfaces__msg__time__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool rover_msgs__msg__crack_detection__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[47];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("rover_msgs.msg._crack_detection.CrackDetection", full_classname_dest, 46) == 0);
  }
  rover_msgs__msg__CrackDetection * ros_message = _ros_message;
  {  // timestamp
    PyObject * field = PyObject_GetAttrString(_pymsg, "timestamp");
    if (!field) {
      return false;
    }
    if (!builtin_interfaces__msg__time__convert_from_py(field, &ros_message->timestamp)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // crack_detected
    PyObject * field = PyObject_GetAttrString(_pymsg, "crack_detected");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->crack_detected = (Py_True == field);
    Py_DECREF(field);
  }
  {  // confidence
    PyObject * field = PyObject_GetAttrString(_pymsg, "confidence");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->confidence = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // bbox_x_min
    PyObject * field = PyObject_GetAttrString(_pymsg, "bbox_x_min");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->bbox_x_min = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // bbox_y_min
    PyObject * field = PyObject_GetAttrString(_pymsg, "bbox_y_min");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->bbox_y_min = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // bbox_x_max
    PyObject * field = PyObject_GetAttrString(_pymsg, "bbox_x_max");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->bbox_x_max = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // bbox_y_max
    PyObject * field = PyObject_GetAttrString(_pymsg, "bbox_y_max");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->bbox_y_max = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // center_x
    PyObject * field = PyObject_GetAttrString(_pymsg, "center_x");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->center_x = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // center_y
    PyObject * field = PyObject_GetAttrString(_pymsg, "center_y");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->center_y = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // estimated_pixel_length
    PyObject * field = PyObject_GetAttrString(_pymsg, "estimated_pixel_length");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->estimated_pixel_length = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // estimated_pixel_width
    PyObject * field = PyObject_GetAttrString(_pymsg, "estimated_pixel_width");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->estimated_pixel_width = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // severity_label
    PyObject * field = PyObject_GetAttrString(_pymsg, "severity_label");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->severity_label, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * rover_msgs__msg__crack_detection__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of CrackDetection */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("rover_msgs.msg._crack_detection");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "CrackDetection");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  rover_msgs__msg__CrackDetection * ros_message = (rover_msgs__msg__CrackDetection *)raw_ros_message;
  {  // timestamp
    PyObject * field = NULL;
    field = builtin_interfaces__msg__time__convert_to_py(&ros_message->timestamp);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "timestamp", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // crack_detected
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->crack_detected ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "crack_detected", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // confidence
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->confidence);
    {
      int rc = PyObject_SetAttrString(_pymessage, "confidence", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // bbox_x_min
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->bbox_x_min);
    {
      int rc = PyObject_SetAttrString(_pymessage, "bbox_x_min", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // bbox_y_min
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->bbox_y_min);
    {
      int rc = PyObject_SetAttrString(_pymessage, "bbox_y_min", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // bbox_x_max
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->bbox_x_max);
    {
      int rc = PyObject_SetAttrString(_pymessage, "bbox_x_max", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // bbox_y_max
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->bbox_y_max);
    {
      int rc = PyObject_SetAttrString(_pymessage, "bbox_y_max", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // center_x
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->center_x);
    {
      int rc = PyObject_SetAttrString(_pymessage, "center_x", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // center_y
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->center_y);
    {
      int rc = PyObject_SetAttrString(_pymessage, "center_y", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // estimated_pixel_length
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->estimated_pixel_length);
    {
      int rc = PyObject_SetAttrString(_pymessage, "estimated_pixel_length", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // estimated_pixel_width
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->estimated_pixel_width);
    {
      int rc = PyObject_SetAttrString(_pymessage, "estimated_pixel_width", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // severity_label
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->severity_label.data,
      strlen(ros_message->severity_label.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "severity_label", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
