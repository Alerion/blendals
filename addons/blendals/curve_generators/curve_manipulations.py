import bpy

from blendals.blnder_utils.enums import KeyframeTransition


def set_keyframe_point(
    animation_curve: bpy.types.FCurve, frame: float, value: float
) -> None:
    keyframe_points: bpy.types.FCurveKeyframePoints = animation_curve.keyframe_points
    keyframe_point: bpy.types.Keyframe = keyframe_points.insert(frame, value)
    keyframe_point.interpolation = KeyframeTransition.LINEAR
