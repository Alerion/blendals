from dataclasses import dataclass
from typing import List

from blendals import live_set


def live_set_to_song(liveset: live_set.LiveSet) -> "Song":
    song = Song(
        tempo=liveset.tempo,
        tracks=[]
    )

    for midi_track in liveset.tracks:
        # Generate notes for each midi key from all midi clips.
        tracks_notes = {}
        for midi_clip in midi_track.midi_clips:
            midi_clip_track_notes = get_track_notes_from_midi_clip(midi_clip)
            for midi_key, notes in midi_clip_track_notes.items():
                if midi_key not in tracks_notes:
                    tracks_notes[midi_key] = []
                tracks_notes[midi_key].extend(notes)

        # Generate unique notes sequence per midi track and midi key.
        name = midi_track.name
        for midi_key, notes in tracks_notes.items():
            track = Track(
                id=f"{name}:{midi_key}",
                notes=notes,
            )
            song.tracks.append(track)

    return song


def get_track_notes_from_midi_clip(
    midi_clip: live_set.MidiClip,
) -> dict[int, list["Note"]]:
    tracks_notes = {}
    for key_track in midi_clip.key_tracks:
        notes = get_notes_from_key_track(
            midi_clip.start, midi_clip.end, key_track, midi_clip.loop
        )
        tracks_notes[key_track.midi_key] = notes
    return tracks_notes


def get_notes_from_key_track(
    start: float, end: float, key_track: live_set.KeyTrack, loop: live_set.Loop
) -> list["Note"]:
    """
    If loop is enabled its length is equal to the length of the key_track.
    So midi_notes_in_loop contains only notes that are in the loop.
    And loops_count is equal to 1.
    """
    # In Ableton Live you can create a long key track and add only part of it into the midi track.
    # Get midi notes that are in the loop. Other midi notes are not used in the midi track.
    midi_notes_in_loop = []
    for midi_note in key_track.midi_notes:
        if loop.start <= midi_note.time <= loop.end:
            midi_notes_in_loop.append(midi_note)

    loop_length = loop.end - loop.start
    track_length = end - start
    notes = []

    # You can loop a ket track and resize it into any length inside the midi clip.
    # So we generate notes for each loop.
    loops_count = int(track_length // loop_length)
    for i in range(loops_count):
        start_offset = start + i * loop_length
        for midi_note in midi_notes_in_loop:
            note_start = start_offset + midi_note.time
            node_end = note_start + midi_note.duration
            notes.append(
                Note(
                    start=note_start,
                    end=node_end,
                    velocity=midi_note.velocity,
                )
            )

    # You resize a ket track to any length inside the midi clip.
    # So the last loop can be shorter than the others.
    start_offset = start + loops_count * loop_length
    last_loop_length = track_length % loop_length
    for midi_note in midi_notes_in_loop:
        if midi_note.time > (loop.start + last_loop_length):
            break
        note_start = start_offset + midi_note.time
        node_end = note_start + midi_note.duration
        notes.append(
            Note(
                start=note_start,
                end=node_end,
                velocity=midi_note.velocity,
            )
        )

    return notes


@dataclass
class Song:
    tempo: int
    # Dacite does not work with build in list that is supported from 3.9. So use List instead of list.
    tracks: List["Track"]


@dataclass
class Track:
    id: str
    notes: List["Note"]


@dataclass
class Note:
    start: float
    end: float
    velocity: int
