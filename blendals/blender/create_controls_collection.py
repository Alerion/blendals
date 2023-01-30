import bpy
from bpy_types import Collection, Object

from blendals.config import settings
from blendals.blender.enums import EmptyDrawType
from rich import print


def create_controls_collection(name: str = settings.LIVE_SET_CONTROLS_COLLECTION) -> Collection:
    collection = bpy.context.scene.collection.children.get(name)
    if collection is None:
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
    return collection


def create_control_object(name: str) -> Object:
    empty_obj = bpy.data.objects.new(name=name, object_data=None)
    empty_obj.empty_display_type = EmptyDrawType.ARROWS
    empty_obj.empty_display_size = 1
    empty_obj.location = (5.0, 5.0, 5.0)
    return empty_obj
