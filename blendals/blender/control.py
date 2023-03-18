import bpy
from bpy_types import Collection, Object

from blendals.types import Location
from blendals.blender.create_controls_collection import (
    create_controls_collection,
    create_control_object,
)


class Control:

    def __init__(self, name: str):
        self.name = name
        self.location: Location = (0, 0, 0)
        self._blender_object: Object

    def create_blender_object(self, controls_collection: Collection) -> None:
        blender_object = bpy.context.scene.objects.get(self.name)
        if blender_object is None:
            blender_object = create_control_object(self.name)
            controls_collection.objects.link(blender_object)
        self._blender_object = blender_object

        blender_object.animation_data_clear()
        blender_object.animation_data_create()

        blender_object.location = self.location

    def animate(self, curve_generator, *, data_path: str, scale_index: int = 0) -> None:
        name = f"{data_path}[{data_path}]: {curve_generator.name}"
        print(f"Generate {name} animation")
        self._blender_object.animation_data.action = bpy.data.actions.new(name=name)
        animation_curve = self._blender_object.animation_data.action.fcurves.new(
            data_path=data_path, index=scale_index
        )
        curve_generator.apply_track_to_curve(animation_curve)
