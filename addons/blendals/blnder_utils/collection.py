import bpy
import bpy_types


def create_or_get_collection(name: str) -> bpy_types.Collection:
    collection = bpy.context.scene.collection.children.get(name)
    if collection is None:
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
    return collection
