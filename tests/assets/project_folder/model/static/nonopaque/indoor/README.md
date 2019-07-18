# Interior nonopaque geometries

`/model/nonopaque/indoor`

This in an optional folder for <u>indoor-only</u> nonopaque geometries. Naming convention
is the same as `./model/nonopaque`. In 3 and 5 phase daylight simulation these files will
only be included in view matrix calculation and will not be part of daylight matrix.
Separating the files is helpful to relax radiance parameters for different phases of
matrix-based studies.

<u>This folder is only useful for 3-Phase and 5-Phase studies</u>. For other recipes the
files in `indoor` folder will be part of the study just like any other geometry file in
`/model/nonopaque` folder.

In this sample case the only transparent geometry which is not part of the apertures is
the top part of the partition inside the room which is included in this folder.

![nonopaque_indoor](https://user-images.githubusercontent.com/2915573/53506467-05dd6400-3a84-11e9-9d15-a1a859135234.jpg)
