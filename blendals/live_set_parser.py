from lxml.etree import _Element as Element

from blendals.live_set import (
    KeyTrack,
    LiveSet,
    Loop,
    MidiClip,
    MidiNote,
    MidiTrack,
    TimeSignature,
)


def parse_als_file_content(element: Element) -> LiveSet:
    live_set_element: Element = element.xpath("/Ableton/LiveSet")[0]

    live_set = LiveSet(
        tempo=get_tempo(live_set_element),
        tracks=get_midi_tracks(live_set_element),
        _element=live_set_element,
    )

    return live_set


def get_tempo(live_set_element: Element) -> int:
    tempo_element = live_set_element.xpath(".//Tempo")[0]
    tempo = int(tempo_element.xpath("./Manual")[0].get("Value"))
    return tempo


def get_midi_tracks(live_set_element: Element) -> list[MidiTrack]:
    output = []
    for midi_track_element in live_set_element.xpath("./Tracks/MidiTrack"):
        name = midi_track_element.xpath("./Name/UserName")[0].get("Value")
        # You can add # to the name in Ableton and track number is inserter there.
        if name.startswith("#"):
            name = name[1:].strip()
        midi_track = MidiTrack(
            name=name,
            midi_clips=get_midi_clips(midi_track_element),
            _element=midi_track_element,
        )
        output.append(midi_track)
    return output


def get_midi_clips(midi_track_element: Element) -> list[MidiClip]:
    output = []
    xpath = (
        "./DeviceChain/MainSequencer/ClipTimeable/ArrangerAutomation/Events/MidiClip"
    )
    for midi_clip_element in midi_track_element.xpath(xpath):
        # TODO: Time is always equal to start. Find out what is the difference.
        # time = float(midi_clip_element.get("Time"))
        start = float(midi_clip_element.xpath("./CurrentStart")[0].get("Value"))
        end = float(midi_clip_element.xpath("./CurrentEnd")[0].get("Value"))
        midi_clip = MidiClip(
            id=midi_clip_element.get("Id"),
            start=start,
            end=end,
            loop=get_loop(midi_clip_element),
            time_signature=get_time_signature(midi_clip_element),
            key_tracks=get_key_tracks(midi_clip_element),
            _element=midi_clip_element,
        )
        output.append(midi_clip)
    return output


def get_loop(midi_clip_element: Element) -> Loop:
    loop_element = midi_clip_element.xpath("./Loop")[0]
    return Loop(
        start=float(loop_element.xpath("./LoopStart")[0].get("Value")),
        end=float(loop_element.xpath("./LoopEnd")[0].get("Value")),
        enabled=loop_element.xpath("./LoopOn")[0].get("Value") == "true",
        _element=loop_element,
    )


def get_time_signature(midi_clip_element: Element) -> TimeSignature:
    xpath = "./TimeSignature/TimeSignatures/RemoteableTimeSignature"
    signature_element = midi_clip_element.xpath(xpath)[0]
    # TODO: Time is always equal to 0. Find out what is it.
    # time = float(signature_element.xpath("./Time")[0].get("Value"))
    return TimeSignature(
        numerator=int(signature_element.xpath("./Numerator")[0].get("Value")),
        denominator=int(signature_element.xpath("./Denominator")[0].get("Value")),
        _element=signature_element,
    )


def get_key_tracks(midi_clip_element: Element) -> list[KeyTrack]:
    output = []
    for key_track_element in midi_clip_element.xpath("./Notes/KeyTracks/KeyTrack"):
        key_track = KeyTrack(
            id=key_track_element.get("Id"),
            midi_key=int(key_track_element.xpath("./MidiKey")[0].get("Value")),
            midi_notes=get_midi_notes(key_track_element),
            _element=key_track_element,
        )
        output.append(key_track)
    return output


def get_midi_notes(key_track_element: Element) -> list[MidiNote]:
    output = []
    for midi_note_element in key_track_element.xpath("./Notes/MidiNoteEvent"):
        if midi_note_element.get("IsEnabled") == "false":
            continue
        midi_note = MidiNote(
            # id=midi_note_element.get("NoteId"),
            time=float(midi_note_element.get("Time")),
            velocity=round(float(midi_note_element.get("Velocity"))),
            duration=float(midi_note_element.get("Duration")),
            _element=midi_note_element,
        )
        output.append(midi_note)
    return output
