# generated from rosidl_generator_py/resource/_idl.py.em
# with input from rover_msgs:msg/CrackDetection.idl
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


class Metaclass_CrackDetection(type):
    """Metaclass of message 'CrackDetection'."""

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
                'rover_msgs.msg.CrackDetection')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__crack_detection
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__crack_detection
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__crack_detection
            cls._TYPE_SUPPORT = module.type_support_msg__msg__crack_detection
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__crack_detection

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


class CrackDetection(metaclass=Metaclass_CrackDetection):
    """Message class 'CrackDetection'."""

    __slots__ = [
        '_timestamp',
        '_crack_detected',
        '_confidence',
        '_bbox_x_min',
        '_bbox_y_min',
        '_bbox_x_max',
        '_bbox_y_max',
        '_center_x',
        '_center_y',
        '_estimated_pixel_length',
        '_estimated_pixel_width',
        '_severity_label',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'timestamp': 'builtin_interfaces/Time',
        'crack_detected': 'boolean',
        'confidence': 'float',
        'bbox_x_min': 'float',
        'bbox_y_min': 'float',
        'bbox_x_max': 'float',
        'bbox_y_max': 'float',
        'center_x': 'float',
        'center_y': 'float',
        'estimated_pixel_length': 'float',
        'estimated_pixel_width': 'float',
        'severity_label': 'string',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['builtin_interfaces', 'msg'], 'Time'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
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
        self.crack_detected = kwargs.get('crack_detected', bool())
        self.confidence = kwargs.get('confidence', float())
        self.bbox_x_min = kwargs.get('bbox_x_min', float())
        self.bbox_y_min = kwargs.get('bbox_y_min', float())
        self.bbox_x_max = kwargs.get('bbox_x_max', float())
        self.bbox_y_max = kwargs.get('bbox_y_max', float())
        self.center_x = kwargs.get('center_x', float())
        self.center_y = kwargs.get('center_y', float())
        self.estimated_pixel_length = kwargs.get('estimated_pixel_length', float())
        self.estimated_pixel_width = kwargs.get('estimated_pixel_width', float())
        self.severity_label = kwargs.get('severity_label', str())

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
        if self.crack_detected != other.crack_detected:
            return False
        if self.confidence != other.confidence:
            return False
        if self.bbox_x_min != other.bbox_x_min:
            return False
        if self.bbox_y_min != other.bbox_y_min:
            return False
        if self.bbox_x_max != other.bbox_x_max:
            return False
        if self.bbox_y_max != other.bbox_y_max:
            return False
        if self.center_x != other.center_x:
            return False
        if self.center_y != other.center_y:
            return False
        if self.estimated_pixel_length != other.estimated_pixel_length:
            return False
        if self.estimated_pixel_width != other.estimated_pixel_width:
            return False
        if self.severity_label != other.severity_label:
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
    def bbox_x_min(self):
        """Message field 'bbox_x_min'."""
        return self._bbox_x_min

    @bbox_x_min.setter
    def bbox_x_min(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'bbox_x_min' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'bbox_x_min' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._bbox_x_min = value

    @builtins.property
    def bbox_y_min(self):
        """Message field 'bbox_y_min'."""
        return self._bbox_y_min

    @bbox_y_min.setter
    def bbox_y_min(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'bbox_y_min' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'bbox_y_min' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._bbox_y_min = value

    @builtins.property
    def bbox_x_max(self):
        """Message field 'bbox_x_max'."""
        return self._bbox_x_max

    @bbox_x_max.setter
    def bbox_x_max(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'bbox_x_max' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'bbox_x_max' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._bbox_x_max = value

    @builtins.property
    def bbox_y_max(self):
        """Message field 'bbox_y_max'."""
        return self._bbox_y_max

    @bbox_y_max.setter
    def bbox_y_max(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'bbox_y_max' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'bbox_y_max' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._bbox_y_max = value

    @builtins.property
    def center_x(self):
        """Message field 'center_x'."""
        return self._center_x

    @center_x.setter
    def center_x(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'center_x' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'center_x' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._center_x = value

    @builtins.property
    def center_y(self):
        """Message field 'center_y'."""
        return self._center_y

    @center_y.setter
    def center_y(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'center_y' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'center_y' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._center_y = value

    @builtins.property
    def estimated_pixel_length(self):
        """Message field 'estimated_pixel_length'."""
        return self._estimated_pixel_length

    @estimated_pixel_length.setter
    def estimated_pixel_length(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'estimated_pixel_length' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'estimated_pixel_length' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._estimated_pixel_length = value

    @builtins.property
    def estimated_pixel_width(self):
        """Message field 'estimated_pixel_width'."""
        return self._estimated_pixel_width

    @estimated_pixel_width.setter
    def estimated_pixel_width(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'estimated_pixel_width' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'estimated_pixel_width' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._estimated_pixel_width = value

    @builtins.property
    def severity_label(self):
        """Message field 'severity_label'."""
        return self._severity_label

    @severity_label.setter
    def severity_label(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'severity_label' field must be of type 'str'"
        self._severity_label = value
