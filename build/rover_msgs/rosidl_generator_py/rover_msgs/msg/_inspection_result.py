# generated from rosidl_generator_py/resource/_idl.py.em
# with input from rover_msgs:msg/InspectionResult.idl
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


class Metaclass_InspectionResult(type):
    """Metaclass of message 'InspectionResult'."""

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
                'rover_msgs.msg.InspectionResult')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__inspection_result
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__inspection_result
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__inspection_result
            cls._TYPE_SUPPORT = module.type_support_msg__msg__inspection_result
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__inspection_result

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


class InspectionResult(metaclass=Metaclass_InspectionResult):
    """Message class 'InspectionResult'."""

    __slots__ = [
        '_timestamp',
        '_inspection_id',
        '_crack_detected',
        '_confidence',
        '_crack_length_mm',
        '_crack_max_width_mm',
        '_crack_avg_width_mm',
        '_apparent_depth_mm',
        '_severity_rating',
        '_image_saved_path',
        '_rover_state',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'timestamp': 'builtin_interfaces/Time',
        'inspection_id': 'string',
        'crack_detected': 'boolean',
        'confidence': 'float',
        'crack_length_mm': 'float',
        'crack_max_width_mm': 'float',
        'crack_avg_width_mm': 'float',
        'apparent_depth_mm': 'float',
        'severity_rating': 'string',
        'image_saved_path': 'string',
        'rover_state': 'string',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['builtin_interfaces', 'msg'], 'Time'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
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
        self.inspection_id = kwargs.get('inspection_id', str())
        self.crack_detected = kwargs.get('crack_detected', bool())
        self.confidence = kwargs.get('confidence', float())
        self.crack_length_mm = kwargs.get('crack_length_mm', float())
        self.crack_max_width_mm = kwargs.get('crack_max_width_mm', float())
        self.crack_avg_width_mm = kwargs.get('crack_avg_width_mm', float())
        self.apparent_depth_mm = kwargs.get('apparent_depth_mm', float())
        self.severity_rating = kwargs.get('severity_rating', str())
        self.image_saved_path = kwargs.get('image_saved_path', str())
        self.rover_state = kwargs.get('rover_state', str())

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
        if self.inspection_id != other.inspection_id:
            return False
        if self.crack_detected != other.crack_detected:
            return False
        if self.confidence != other.confidence:
            return False
        if self.crack_length_mm != other.crack_length_mm:
            return False
        if self.crack_max_width_mm != other.crack_max_width_mm:
            return False
        if self.crack_avg_width_mm != other.crack_avg_width_mm:
            return False
        if self.apparent_depth_mm != other.apparent_depth_mm:
            return False
        if self.severity_rating != other.severity_rating:
            return False
        if self.image_saved_path != other.image_saved_path:
            return False
        if self.rover_state != other.rover_state:
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
    def inspection_id(self):
        """Message field 'inspection_id'."""
        return self._inspection_id

    @inspection_id.setter
    def inspection_id(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'inspection_id' field must be of type 'str'"
        self._inspection_id = value

    @builtins.property
    def crack_detected(self):
        """Message field 'crack_detected'."""
        return self._crack_detected

    @crack_detected.setter
    def crack_detected(self, value):
        if self._check_fields:
            assert \
                isinstance(value, bool), \
                "The 'crack_detected' field must be of type 'bool'"
        self._crack_detected = value

    @builtins.property
    def confidence(self):
        """Message field 'confidence'."""
        return self._confidence

    @confidence.setter
    def confidence(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'confidence' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'confidence' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._confidence = value

    @builtins.property
    def crack_length_mm(self):
        """Message field 'crack_length_mm'."""
        return self._crack_length_mm

    @crack_length_mm.setter
    def crack_length_mm(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'crack_length_mm' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'crack_length_mm' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._crack_length_mm = value

    @builtins.property
    def crack_max_width_mm(self):
        """Message field 'crack_max_width_mm'."""
        return self._crack_max_width_mm

    @crack_max_width_mm.setter
    def crack_max_width_mm(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'crack_max_width_mm' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'crack_max_width_mm' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._crack_max_width_mm = value

    @builtins.property
    def crack_avg_width_mm(self):
        """Message field 'crack_avg_width_mm'."""
        return self._crack_avg_width_mm

    @crack_avg_width_mm.setter
    def crack_avg_width_mm(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'crack_avg_width_mm' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'crack_avg_width_mm' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._crack_avg_width_mm = value

    @builtins.property
    def apparent_depth_mm(self):
        """Message field 'apparent_depth_mm'."""
        return self._apparent_depth_mm

    @apparent_depth_mm.setter
    def apparent_depth_mm(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'apparent_depth_mm' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'apparent_depth_mm' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._apparent_depth_mm = value

    @builtins.property
    def severity_rating(self):
        """Message field 'severity_rating'."""
        return self._severity_rating

    @severity_rating.setter
    def severity_rating(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'severity_rating' field must be of type 'str'"
        self._severity_rating = value

    @builtins.property
    def image_saved_path(self):
        """Message field 'image_saved_path'."""
        return self._image_saved_path

    @image_saved_path.setter
    def image_saved_path(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'image_saved_path' field must be of type 'str'"
        self._image_saved_path = value

    @builtins.property
    def rover_state(self):
        """Message field 'rover_state'."""
        return self._rover_state

    @rover_state.setter
    def rover_state(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'rover_state' field must be of type 'str'"
        self._rover_state = value
