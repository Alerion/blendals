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

import sys
import os.path
from importlib import reload

DEPENDENCIES_PATH = os.path.join(os.path.dirname(__file__), '../dependencies')
sys.path.insert(0, DEPENDENCIES_PATH)

if "bpy" not in locals():
    from . import parse_song
else:
    reload(parse_song)


import bpy


def register():
    parse_song.register_module()


def unregister():
    parse_song.unregister_module()
