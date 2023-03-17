from bpy.types import FCurve, FCurveKeyframePoints

from blendals.blender.enums import KeyframeTransition


def set_keyframe_point(
    animation_curve: FCurve, frame: float, value: float
) -> None:
    keyframe_points: FCurveKeyframePoints = animation_curve.keyframe_points
    keyframe_point = keyframe_points.insert(frame, value)
    keyframe_point.interpolation = KeyframeTransition.LINEAR
