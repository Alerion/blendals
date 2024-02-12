bl_info = {
    "name": "Blendals",
    "author": "Dmytro Kostochko",
    "version": (0, 1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Properties > Blendals",
    "description": "Convert Ableton file into animations.",
    "doc_url": "https://github.com/Alerion/blendals",
    "tracker_url": "https://github.com/Alerion/blendals/issues",
    "category": "3D View",
}

from importlib import reload

if "bpy" not in locals():
    from . import parse_song
else:
    reload(parse_song)


import bpy


def register():
    parse_song.register_module()


def unregister():
    parse_song.unregister_module()
