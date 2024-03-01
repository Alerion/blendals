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

import logging
import sys
import os.path
from importlib import reload

logger = logging.getLogger(__name__)

# Inject external dependencies.
DEPENDENCIES_PATH = os.path.join(os.path.dirname(__file__), '../dependencies')
sys.path.insert(0, DEPENDENCIES_PATH)

# Import modules to register.
# It should contain `register_module` and `unregister_module` functions.
from .blender_modules import import_song

MODULES = (
    import_song,
)

DO_MODULES_RELOAD = ("register" in locals())


def register():
    """
    This function is executed by Blender when addon is loaded.
    """
    _register_addon_modules()


def unregister():
    """
    This function is executed by Blender when addon is loaded.
    """
    _unregister_addon_modules()


def _register_addon_modules():
    for addon_module in MODULES:
        if DO_MODULES_RELOAD:
            reload(addon_module)

        if hasattr(addon_module, "register_module"):
            addon_module.register_module()


def _unregister_addon_modules():
    for addon_module in MODULES:
        if hasattr(addon_module, "unregister_module"):
            addon_module.unregister_module()
