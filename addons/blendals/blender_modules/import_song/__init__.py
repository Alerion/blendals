from importlib import reload

import bpy

from . import song_info
from . import parse_song
from . import midi_track_info

MODULES = (
    song_info,
    parse_song,
    midi_track_info,
)

DO_MODULES_RELOAD = ("register_module" in locals())

if DO_MODULES_RELOAD:
    for addon_module in MODULES:
        reload(addon_module)

classes = (
    song_info.BlendalsSongProperties,
    song_info.BLENDALS_PT_SongInfo,
    midi_track_info.BlendalsMidiTrackProperties,
    midi_track_info.BLENDALS_PT_MidiTrackInfo,
    midi_track_info.BLENDALS_OT_ApplyAnimation,
    parse_song.BLENDALS_OT_ParseSong,
    parse_song.BLENDALS_PT_ParseSong,
)


def register_module():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister_module():
    for cls in classes:
        bpy.utils.unregister_class(cls)
