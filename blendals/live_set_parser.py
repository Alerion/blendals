import gzip
from pathlib import Path

from lxml import etree
from lxml.etree import _Element as Element

from rich import print

from blendals.live_set import (
    KeyTrack,
    LiveSet,
    Loop,
    MidiClip,
    MidiNote,
    MidiTrack,
    TimeSignature,
    AudioTrack,
    AudioClip,
)
from blendals.utils.xml import print_xml, save_xml_to_file
from blendals.extract_wave_from_audio_file import extract_points_from_audio_file


class LiveSetParser:
    def __init__(self, als_file_path: Path):
        self.als_file_path = als_file_path
        self.directory = als_file_path.parent

    def get_live_set(self) -> LiveSet:
        content = gzip.decompress(self.als_file_path.read_bytes())
        content = content.replace(b"\t", b"")
        content = content.replace(b"\n", b"")
        als_xml = etree.fromstring(content)
        live_set_element: Element = als_xml.xpath("/Ableton/LiveSet")[0]

        live_set = LiveSet(
            bpm=get_bpm(live_set_element),
            midi_tracks=get_midi_tracks(live_set_element),
            audio_tracks=get_audio_tracks(live_set_element, self.directory),
            _element=live_set_element,
        )

        return live_set


def get_bpm(live_set_element: Element) -> int:
    tempo_element = live_set_element.xpath(".//Tempo")[0]
    bpm = int(tempo_element.xpath("./Manual")[0].get("Value"))
    return bpm


def get_audio_tracks(live_set_element: Element, directory: Path) -> list[AudioTrack]:
    bpm = get_bpm(live_set_element)
    output = []
    for audio_track_element in live_set_element.xpath("./Tracks/AudioTrack"):
        midi_track = AudioTrack(
            name=_get_track_name(audio_track_element),
            audio_clips=get_audio_clips(audio_track_element, bpm, directory),
            _element=audio_track_element,
        )
        output.append(midi_track)
    return output


def get_audio_clips(
    audio_track_element: Element, bpm: int, directory: Path
) -> list[AudioClip]:
    output = []
    xpath = "./DeviceChain/MainSequencer/Sample/ArrangerAutomation/Events/AudioClip"
    for audio_clip_element in audio_track_element.xpath(xpath):
        # TODO: Time is always equal to start. Find out what is the difference.
        # time = float(audio_clip_element.get("Time"))
        save_xml_to_file(audio_clip_element.xpath("./SampleRef")[0], "sample_ref.xml")
        audio_file_path = get_audio_file_path(
            audio_clip_element.xpath("./SampleRef")[0], directory
        )
        left_channel_points, right_channel_points = extract_points_from_audio_file(
            audio_file_path, bpm
        )

        audio_clip = AudioClip(
            id=audio_clip_element.get("Id"),
            name=audio_clip_element.xpath("./Name")[0].get("Value"),
            start=get_clip_start(audio_clip_element),
            end=get_clip_end(audio_clip_element),
            loop=get_loop(audio_clip_element),
            time_signature=get_time_signature(audio_clip_element),
            left_channel_points=left_channel_points,
            right_channel_points=right_channel_points,
            _element=audio_clip_element,
        )
        save_xml_to_file(
            audio_clip_element,
            f"audio_clip_{audio_clip.start}_{audio_clip.end}_{audio_clip.name}.xml",
        )
        output.append(audio_clip)
    return output


def get_audio_file_path(sample_ref_element: Element, directory: Path) -> Path:
    file_ref_element = sample_ref_element.xpath("./FileRef")[0]
    has_relative_path = (
        file_ref_element.xpath("HasRelativePath")[0].get("Value") == "true"
    )
    if not has_relative_path:
        raise Exception("Not implemented")

    path_elements = file_ref_element.xpath("./RelativePath/RelativePathElement")
    path_parts = []
    for path_element in path_elements:
        path_part = path_element.get("Dir")
        if path_part == "":
            path_part = ".."
        path_parts.append(path_part)
    name = file_ref_element.xpath("./Name")[0].get("Value")
    path_parts.append(name)
    audio_file_path = "/".join(path_parts)
    return directory.joinpath(audio_file_path)


def get_midi_tracks(live_set_element: Element) -> list[MidiTrack]:
    output = []
    for midi_track_element in live_set_element.xpath("./Tracks/MidiTrack"):
        midi_track = MidiTrack(
            name=_get_track_name(midi_track_element),
            midi_clips=get_midi_clips(midi_track_element),
            _element=midi_track_element,
        )
        output.append(midi_track)
    return output


def _get_track_name(element: Element) -> str:
    name = element.xpath("./Name/UserName")[0].get("Value")
    # You can add # to the name in Ableton and track number is inserter there.
    if name.startswith("#"):
        name = name[1:].strip()
    return name


def get_midi_clips(midi_track_element: Element) -> list[MidiClip]:
    output = []
    xpath = (
        "./DeviceChain/MainSequencer/ClipTimeable/ArrangerAutomation/Events/MidiClip"
    )
    for midi_clip_element in midi_track_element.xpath(xpath):
        # TODO: Time is always equal to start. Find out what is the difference.
        # time = float(midi_clip_element.get("Time"))
        midi_clip = MidiClip(
            id=midi_clip_element.get("Id"),
            start=get_clip_start(midi_clip_element),
            end=get_clip_end(midi_clip_element),
            loop=get_loop(midi_clip_element),
            time_signature=get_time_signature(midi_clip_element),
            key_tracks=get_key_tracks(midi_clip_element),
            _element=midi_clip_element,
        )
        output.append(midi_clip)
    return output


def get_loop(clip_element: Element) -> Loop:
    loop_element = clip_element.xpath("./Loop")[0]
    return Loop(
        start=float(loop_element.xpath("./LoopStart")[0].get("Value")),
        end=float(loop_element.xpath("./LoopEnd")[0].get("Value")),
        enabled=loop_element.xpath("./LoopOn")[0].get("Value") == "true",
        _element=loop_element,
    )


def get_time_signature(clip_element: Element) -> TimeSignature:
    xpath = "./TimeSignature/TimeSignatures/RemoteableTimeSignature"
    signature_element = clip_element.xpath(xpath)[0]
    # TODO: Time is always equal to 0. Find out what is it.
    # time = float(signature_element.xpath("./Time")[0].get("Value"))
    return TimeSignature(
        numerator=int(signature_element.xpath("./Numerator")[0].get("Value")),
        denominator=int(signature_element.xpath("./Denominator")[0].get("Value")),
        _element=signature_element,
    )


def get_clip_start(clip_element: Element) -> float:
    return float(clip_element.xpath("./CurrentStart")[0].get("Value"))


def get_clip_end(clip_element: Element) -> float:
    return float(clip_element.xpath("./CurrentEnd")[0].get("Value"))


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
