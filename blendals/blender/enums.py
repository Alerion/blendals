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
