# honeybee-radiance-folder
Honeybee Radiance folder is a python library to read, write and validate
[Radiance folder structure](https://github.com/ladybug-tools/radiance-folder-structure).


# Usage

```python
# create a Radiance folder
from honeybee_radiance_folder import Folder
import os

rf = 'c:/ladybug/sample_folder'
folder = Folder(rf)
folder.write(overwrite=True)

# check the folders created in folder
for f in os.listdir(rf):
    print(f)
```

```shell
asset
model
output
system
```

```python
# load a Radiance folder

# in this case we are loading the folder from sample folder in radiance folder repository
# you can download it from here
# https://github.com/ladybug-tools/radiance-folder-structure/tree/master/project_folder
from honeybee_radiance_folder import Folder

rf = 'c:/ladybug/sample_folder'
folder = Folder(rf)

# get input files for static scene
for f in folder.model.static_nonaperture_files(black_out=False, rel_path=True):
    print(f)
```

```shell
model\static\opaque\sample_case.mat
model\static\opaque\sample_case.rad
model\static\opaque\outdoor\context.mat
model\static\opaque\outdoor\context.rad
model\static\opaque\indoor\partition.mat
model\static\opaque\indoor\partition.rad
model\static\nonopaque\indoor\partition_glass.mat
model\static\nonopaque\indoor\partition_glass.rad
```

```python
# and static aperture
for f in folder.model.static_aperture_files(black_out=False, rel_path=True):
    print(f)
```

```shell
model\static\aperture\sample_case.mat
model\static\aperture\sample_case.rad
```

```python
# and finally get the dynamic aperture - south window in this case
# and check each state
for count, ap in enumerate(folder.model.aperture_group(interior=False)):
    print('dynamic aperture %d: %s' % (count + 1, ap.identifier))
    for state in ap.states:
        print('- %s: %s' % (state.identifier, state.default))
```

```shell
dynamic aperture 1: south_window
- clear: south_window..default..000.rad
- diffuse: south_window..default..001.rad
```
