# About

The basic idea is to parse the Ableton Live project file(.als) 
and create a .json file with a track structure. Then you can use data from
this file to create a track visualization.

Use [blendals_parser](https://github.com/Alerion/blendals_parser) to get `song.json` file
from Ableton Live project file.

# Installation

```
python3.10 -m venv venv
. venv/bin/activate
poetry install
```

# Running code in Blender

## Install Blendals Addon

Find path to Blender executable. Fo Steam version it will be something like `<path to Steam>/steamapps/common/Blender/blender.exe`.

```
export BLENDER=<path to Blender>/blender.exe
$BLENDER
```

Add project root to [Script Directories](https://docs.blender.org/manual/en/latest/editors/preferences/file_paths.html#script-directories),
so Blendals addon can be loaded directly from a project folder.

You can find Script Directories here: `Edit > Preferences > File Paths`.

Restart Blender and activate addon. You should see the Blendas panel on the sidebar of the 3D View main window.

## Making changes to Addon

Make changes to code and reload scripts inb Blender. To do this click on Blender icon in Menu and `System > Reload Scripts`.
You can right click on this menu and add it to `Quick Favourits` for quick access with `Q` button.

# Blender modules autocomplete in PyCharm

Run this in Blender python console to get path to modules:
```
>>> import bpy
>>> bpy.__path__
```

It should be something like this `<path to blender>/Blender/4.0/3scripts/modules/bpy`.
Add `<path to blender>/Blender/4.0/3scripts/modules` as Content Root to your PyCharm project.





## Install dependencies (DEPRECATED)

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

PROJECT_ROOT = "<Path to project>"

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import blendals123.blender.main

import importlib

modules_to_reload = []
for name, module in sys.modules.items():
    if name.startswith("blendals"):
        modules_to_reload.append(module)

for module in modules_to_reload:
    importlib.reload(module)

for module in modules_to_reload:
    importlib.reload(module)

if __name__ == "__main__":
    blendals.blender.main.main()
```

Now you can change code in IDE and run this script in Blender.

