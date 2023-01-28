from dataclasses import dataclass, field
from typing import Optional

from lxml.etree import _Element as Element


@dataclass
class LiveSet:
    tempo: int
    tracks: list["MidiTrack"]
    _element: Optional[Element] = field(default=None, repr=False)


@dataclass
class MidiTrack:
    name: str
    midi_clips: list["MidiClip"]
    _element: Optional[Element] = field(default=None, repr=False)


@dataclass
class MidiClip:
    id: str
    start: float
    end: float
    loop: "Loop"
    time_signature: "TimeSignature"
    key_tracks: list["KeyTrack"]
    _element: Optional[Element] = field(default=None, repr=False)


@dataclass
class Loop:
    start: float
    end: float
    enabled: bool
    _element: Optional[Element] = field(default=None, repr=False)


@dataclass
class TimeSignature:
    numerator: int
    denominator: int
    _element: Optional[Element] = field(default=None, repr=False)


@dataclass
class KeyTrack:
    id: str
    midi_key: int
    midi_notes: list["MidiNote"]
    _element: Optional[Element] = field(default=None, repr=False)


@dataclass
class MidiNote:
    time: float
    duration: float
    velocity: int
    _element: Optional[Element] = field(default=None, repr=False)
