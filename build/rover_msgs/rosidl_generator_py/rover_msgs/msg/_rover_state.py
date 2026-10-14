# generated from rosidl_generator_py/resource/_idl.py.em
# with input from rover_msgs:msg/RoverState.idl
# generated code does not contain a copyright notice

# This is being done at the module level and not on the instance level to avoid looking
# for the same variable multiple times on each instance. This variable is not supposed to
# change during runtime so it makes sense to only look for it once.
from os import getenv

ros_python_check_fields = getenv('ROS_PYTHON_CHECK_FIELDS', default='')


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_RoverState(type):
    """Metaclass of message 'RoverState'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('rover_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'rover_msgs.msg.RoverState')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__rover_state
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__rover_state
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__rover_state
            cls._TYPE_SUPPORT = module.type_support_msg__msg__rover_state
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__rover_state

            from builtin_interfaces.msg import Time
            if Time.__class__._TYPE_SUPPORT is None:
                Time.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class RoverState(metaclass=Metaclass_RoverState):
    """Message class 'RoverState'."""

    __slots__ = [
        '_timestamp',
        '_current_state',
        '_current_linear_speed',
        '_current_angular_speed',
        '_emergency_stop_active',
        '_motor_enabled',
        '_watchdog_active',
        '_status_message',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'timestamp': 'builtin_interfaces/Time',
        'current_state': 'string',
        'current_linear_speed': 'float',
        'current_angular_speed': 'float',
        'emergency_stop_active': 'boolean',
        'motor_enabled': 'boolean',
        'watchdog_active': 'boolean',
        'status_message': 'string',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['builtin_interfaces', 'msg'], 'Time'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        if 'check_fields' in kwargs:
            self._check_fields = kwargs['check_fields']
        else:
            self._check_fields = ros_python_check_fields == '1'
        if self._check_fields:
            assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
                'Invalid arguments passed to constructor: %s' % \
                ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from builtin_interfaces.msg import Time
        self.timestamp = kwargs.get('timestamp', Time())
        self.current_state = kwargs.get('current_state', str())
        self.current_linear_speed = kwargs.get('current_linear_speed', float())
        self.current_angular_speed = kwargs.get('current_angular_speed', float())
        self.emergency_stop_active = kwargs.get('emergency_stop_active', bool())
        self.motor_enabled = kwargs.get('motor_enabled', bool())
        self.watchdog_active = kwargs.get('watchdog_active', bool())
        self.status_message = kwargs.get('status_message', str())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.get_fields_and_field_types().keys(), self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    if self._check_fields:
                        assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.timestamp != other.timestamp:
            return False
        if self.current_state != other.current_state:
            return False
        if self.current_linear_speed != other.current_linear_speed:
            return False
        if self.current_angular_speed != other.current_angular_speed:
            return False
        if self.emergency_stop_active != other.emergency_stop_active:
            return False
        if self.motor_enabled != other.motor_enabled:
            return False
        if self.watchdog_active != other.watchdog_active:
            return False
        if self.status_message != other.status_message:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def timestamp(self):
        """Message field 'timestamp'."""
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        if self._check_fields:
            from builtin_interfaces.msg import Time
            assert \
                isinstance(value, Time), \
                "The 'timestamp' field must be a sub message of type 'Time'"
        self._timestamp = value

    @builtins.property
    def current_state(self):
        """Message field 'current_state'."""
        return self._current_state

    @current_state.setter
    def current_state(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'current_state' field must be of type 'str'"
        self._current_state = value

    @builtins.property
    def current_linear_speed(self):
        """Message field 'current_linear_speed'."""
        return self._current_linear_speed

    @current_linear_speed.setter
    def current_linear_speed(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'current_linear_speed' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'current_linear_speed' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._current_linear_speed = value

    @builtins.property
    def current_angular_speed(self):
        """Message field 'current_angular_speed'."""
        return self._current_angular_speed

    @current_angular_speed.setter
    def current_angular_speed(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'current_angular_speed' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'current_angular_speed' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._current_angular_speed = value

    @builtins.property
    def emergency_stop_active(self):
        """Message field 'emergency_stop_active'."""
        return self._emergency_stop_active

    @emergency_stop_active.setter
    def emergency_stop_active(self, value):
        if self._check_fields:
            assert \
                isinstance(value, bool), \
                "The 'emergency_stop_active' field must be of type 'bool'"
        self._emergency_stop_active = value

    @builtins.property
    def motor_enabled(self):
        """Message field 'motor_enabled'."""
        return self._motor_enabled

    @motor_enabled.setter
    def motor_enabled(self, value):
        if self._check_fields:
            assert \
                isinstance(value, bool), \
                "The 'motor_enabled' field must be of type 'bool'"
        self._motor_enabled = value

    @builtins.property
    def watchdog_active(self):
        """Message field 'watchdog_active'."""
        return self._watchdog_active

    @watchdog_active.setter
    def watchdog_active(self, value):
        if self._check_fields:
            assert \
                isinstance(value, bool), \
                "The 'watchdog_active' field must be of type 'bool'"
        self._watchdog_active = value

    @builtins.property
    def status_message(self):
        """Message field 'status_message'."""
        return self._status_message

    @status_message.setter
    def status_message(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'status_message' field must be of type 'str'"
        self._status_message = value
