import os
import json

import bpy
import bpy_types
from bpy.props import StringProperty, BoolProperty
from bpy.types import Operator, Panel
from bpy_extras.io_utils import ImportHelper


class BLENDALS_OT_ParseSong(Operator, ImportHelper):
    bl_idname = "blendals.parse_song"
    bl_label = "Parse Song"

    filter_glob: StringProperty(default='*.json', options={'HIDDEN'})
    some_boolean: BoolProperty(name='Do a thing', description='Do a thing with the file you\'ve selected',
                               default=True, )

    def execute(self, context: bpy_types.Context) -> set[str]:
        # See https://docs.blender.org/api/current/bpy.types.WindowManager.html#bpy.types.WindowManager.fileselect_add
        filename, extension = os.path.splitext(self.filepath)
        print('Selected file:', self.filepath)
        print('File name:', filename)
        print('File extension:', extension)
        print('Some Boolean:', self.some_boolean)

        with open(self.filepath, "r") as song_file:
            data = json.loads(song_file.read())

        midi_tracks_count = len(data["midi_tracks"])
        audio_tracks_count = len(data["audio_tracks"])

        self.report({"INFO"}, f"{midi_tracks_count} MIDI and {audio_tracks_count} audio tracks parsed!")
        return {'FINISHED'}


class BLENDALS_PT_ParseSong(Panel):
    bl_idname = "BLENDALS_PT_ParseSong"
    bl_label = "Parse Song"
    bl_category = "Blendals"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    # bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context: bpy_types.Context) -> None:
        layout = self.layout

        col = layout.column(align=True)
        col.operator(BLENDALS_OT_ParseSong.bl_idname, text="Parse Song")


classes = (
    BLENDALS_OT_ParseSong,
    BLENDALS_PT_ParseSong,
)


def register_module():
    print("REGISTER PARSE SONG")
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister_module():
    print("UNREGISTER PARSE SONG")
    for cls in classes:
        bpy.utils.unregister_class(cls)
