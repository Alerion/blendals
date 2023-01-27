# About

The basic idea is to parse the Ableton Live project file(.als) 
and create a .json file with a track structure. Then you can use data from
this file to create a track visualization.

# Installation

```
python3.9 -m venv venv
. venv/bin/activate
poetry install
```

# Usage

```
python -m main parse <path to .als file>
```
