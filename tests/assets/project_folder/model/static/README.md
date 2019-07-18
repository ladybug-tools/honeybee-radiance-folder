# static

`./model/static`

This folder includes all the static geometries in model. The files should be copied into
one of the three subfolders:

1. `aperture`: Includes all the static aperture geometries.
2. `nonopaque`: Includes all transparent and translucent geometries that are not part of
   the apertures.
3. `opaque`: Includes all geometries with opaque modifiers.


In direct sunlight calculation the content in `opaque` folder will be blacked out but the
geometry in `nonopaque` and `aperture` folders will be used as is. 


In most cases there are only 3 files in this folder:

1. `*.rad`: This file includes only radiance geometries. It should not include any
   of the radiance modifiers / materials. Materials should be included in
2. `*.mat`: This file includes all the modifiers for geometries in `*.rad`.
3. `*.blk`: This file includes materials for geometries in `*.rad` that will
   be used for direct calculation. In most of the cases the materials in `*.blk`
   are black plastic.

Honeybee uses `.blk` and `.rad` files for direct calculation and uses `.mat` and `.rad`
files for other cases.

You have several files in this folder as long as you follow naming convention below:

1. `*.rad`
2. `*.mat`
3. `*.blk`

