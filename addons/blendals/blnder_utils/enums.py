from enum import Enum


class EmptyDrawType(str, Enum):
    """
    https://docs.blender.org/api/current/bpy_types_enum_items/object_empty_drawtype_items.html
    """

    ARROWS = "ARROWS"
    CIRCLE = "CIRCLE"
    CONE = "CONE"
    CUBE = "CUBE"
    IMAGE = "IMAGE"
    PLAIN_AXES = "PLAIN_AXES"
    SINGLE_ARROW = "SINGLE_ARROW"
    SPHERE = "SPHERE"


class KeyframeTransition(str, Enum):
    """
    https://docs.blender.org/api/current/bpy_types_enum_items/beztriple_interpolation_mode_items.html
    """

    CONSTANT = "CONSTANT"
    LINEAR = "LINEAR"
    BEZIER = "BEZIER"


class KeyframeHandleType(str, Enum):
    """
    https://docs.blender.org/api/current/bpy_types_enum_items/keyframe_handle_type_items.html
    """

    FREE = "FREE"
    ALIGNED = "ALIGNED"
    VECTOR = "VECTOR"
    AUTO = "AUTO"
    AUTO_CLAMPED = "AUTO_CLAMPED"


class PropertySubtypeNumber(str, Enum):
    """
    https://docs.blender.org/api/current/bpy_types_enum_items/property_subtype_number_items.html
    """

    PIXEL = "PIXEL"
    UNSIGNED = "UNSIGNED"
    PERCENTAGE = "PERCENTAGE"
    FACTOR = "FACTOR"
    ANGLE = "ANGLE"
    TIME = "TIME"
    TIME_ABSOLUTE = "TIME_ABSOLUTE"
    DISTANCE = "DISTANCE"
    DISTANCE_CAMERA = "DISTANCE_CAMERA"
    POWER = "POWER"
    TEMPERATURE = "TEMPERATURE"
    NONE = "NONE"


class WMReport(str, Enum):
    """
    https://docs.blender.org/api/current/bpy_types_enum_items/wm_report_items.html
    """

    DEBUG = "DEBUG"
    INFO = "INFO"
    OPERATOR = "OPERATOR"
    PROPERTY = "PROPERTY"
    WARNING = "WARNING"
    ERROR = "ERROR"
    ERROR_INVALID_INPUT = "ERROR_INVALID_INPUT"
    ERROR_INVALID_CONTEXT = "ERROR_INVALID_CONTEXT"
    ERROR_OUT_OF_MEMORY = "ERROR_OUT_OF_MEMORY"


class OperatorReturn(str, Enum):
    """
    https://docs.blender.org/api/current/bpy_types_enum_items/operator_return_items.html
    """

    RUNNING_MODAL = "RUNNING_MODAL"
    CANCELLED = "CANCELLED"
    FINISHED = "FINISHED"
    PASS_THROUGH = "PASS_THROUGH"
    INTERFACE = "INTERFACE"


class OperatorTypeFlag(str, Enum):
    """
    https://docs.blender.org/api/current/bpy_types_enum_items/operator_type_flag_items.html
    """

    REGISTER = "REGISTER"
    UNDO = "UNDO"
    UNDO_GROUPED = "UNDO_GROUPED"
    BLOCKING = "BLOCKING"
    MACRO = "MACRO"
    GRAB_CURSOR = "GRAB_CURSOR"
    GRAB_CURSOR_X = "GRAB_CURSOR_X"
    GRAB_CURSOR_Y = "GRAB_CURSOR_Y"
    DEPENDS_ON_CURSOR = "DEPENDS_ON_CURSOR"
    PRESET = "PRESET"
    INTERNAL = "INTERNAL"


class FModifierType(str, Enum):
    """
    https://docs.blender.org/api/current/bpy_types_enum_items/fmodifier_type_items.html
    """
    NULL = "NULL"
    GENERATOR = "GENERATOR"
    FNGENERATOR = "FNGENERATOR"
    ENVELOPE = "ENVELOPE"
    CYCLES = "CYCLES"
    NOISE = "NOISE"
    LIMITS = "LIMITS"
    STEPPED = "STEPPED"
