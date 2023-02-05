from enum import Enum


class EmptyDrawType(str, Enum):
    """
    https://docs.blender.org/api/current/bpy_types_enum_items/object_empty_drawtype_items.html
    """
    ARROWS = 'ARROWS'
    CIRCLE = 'CIRCLE'
    CONE = 'CONE'
    CUBE = 'CUBE'
    IMAGE = 'IMAGE'
    PLAIN_AXES = 'PLAIN_AXES'
    SINGLE_ARROW = 'SINGLE_ARROW'
    SPHERE = 'SPHERE'


class KeyframeTransition(str, Enum):
    """
    https://docs.blender.org/api/current/bpy_types_enum_items/beztriple_interpolation_mode_items.html#rna-enum-beztriple-interpolation-mode-items
    """
    CONSTANT = 'CONSTANT'
    LINEAR = 'LINEAR'
    BEZIER = 'BEZIER'


class KeyframeHandleType(str, Enum):
    """
    https://docs.blender.org/api/current/bpy_types_enum_items/keyframe_handle_type_items.html#rna-enum-keyframe-handle-type-items
    """
    FREE = 'FREE'
    ALIGNED = 'ALIGNED'
    VECTOR = 'VECTOR'
    AUTO = 'AUTO'
    AUTO_CLAMPED = 'AUTO_CLAMPED'
