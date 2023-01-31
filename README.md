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

# Running code in Blender

## Install dependencies

FIXME: It is a dangerous way, because we can overwrite Blender's dependencies. 

Install `poetry`:
```
<path to blender>/Blender/3.4/python/bin/python.exe -m pip install poetry
```

Run in project root:
```
POETRY_VIRTUALENVS_CREATE=false <path to blender>/Blender/3.4/python/bin/python.exe -m poetry install
```

## Run blender

```
<path to blender>/Blender/blender.exe
```

Add this script in Blender:
```python
import sys

PROJECT_ROOT = "<path to project root>"

if PROJECT_ROOT not in sys.path:
   sys.path.append(PROJECT_ROOT)

import blendals.blender.main
import importlib
importlib.reload(blendals.blender.main)    


if __name__ == "__main__":
    blendals.blender.main.main()
```

Now you can change code in IDE and run this script in Blender.

# Blender modules autocomplete in PyCharm

Run this in Blender python console to get path to modules:
```
>>> import bpy
>>> bpy.__path__
```

It should be something like this `<path to blender>/Blender/3.4/3scripts/modules/bpy`.
Add `<path to blender>/Blender/3.4/3scripts/modules` as Content Root to your PyCharm project.