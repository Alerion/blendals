import bpy

from blendals.config import settings


def add_audio_to_sequence_editor(channel: int = 1, frame_start: int = 1) -> None:
    scene = bpy.context.scene

    # Create sequences editor
    if not scene.sequence_editor:
        scene.sequence_editor_create()

    # Remove existing sequence
    existing_sequence = None
    for sequence in scene.sequence_editor.sequences.values():
        if sequence.channel == channel:
            existing_sequence = sequence
            break

    if existing_sequence is not None:
        scene.sequence_editor.sequences.remove(existing_sequence)

    # Add audio file as a sequence
    # TODO: Get frame_start from animation properties
    scene.sequence_editor.sequences.new_sound(
        "Audio track", settings.AUDIO_FILE_PATH, channel, frame_start
    )
