import bpy

__all__ = (
    "BlendalsSongProperties",
    "BLENDALS_PT_SongInfo",
)


class BlendalsSongProperties(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name")
    bpm: bpy.props.IntProperty(name="BPM")

    @classmethod
    def register(cls):
        bpy.types.Object.blendals_song = bpy.props.PointerProperty(
            name="Blendals Song",
            description="Blendals Song Properties",
            type=cls,
        )

    @classmethod
    def unregister(cls):
        del bpy.types.Object.blendals_song


class BLENDALS_PT_SongInfo(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Blendals Song Info"
    bl_idname = "OBJECT_PT_blendals_song_info"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    @classmethod
    def poll(cls, context) -> bool:
        if context.object is None:
            return False

        if not context.object.blendals_song.name:
            return False

        return True

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text=f"Song: {obj.blendals_song.name}")
        row = layout.row()
        row.prop(obj.blendals_song, "bpm")
