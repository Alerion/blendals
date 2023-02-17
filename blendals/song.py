from dataclasses import dataclass


@dataclass
class Song:
    bpm: int
    # Dacite does not work with build in list that is supported from 3.9. So use List instead of list.
    midi_tracks: list["MidiTrack"]
    audio_tracks: list["AudioTrack"]

    def get_midi_track(self, track_id: str) -> "MidiTrack":
        for track in self.midi_tracks:
            if track.id == track_id:
                return track
        raise KeyError(track_id)


@dataclass
class MidiTrack:
    id: str
    notes: list["Note"]


@dataclass
class Note:
    start: float
    end: float
    velocity: int


@dataclass
class AudioTrack:
    id: str
    points: list["Point"]


@dataclass
class Point:
    time: float
    value: float
