# indoor opaque geometries

`/model/opaque/indoor`

This in an optional folder for <u>indoor-only</u> geometries. File naming convention is
the same as `./model/opaque`. These files will only be included in view matrix
calculation and will not be part of daylight matrix. Separating the files is helpful to
relax radiance parameters for different phases of matrix-based studies.

<u>This folder is only useful for 3-Phase and 5-Phase studies</u>. For other recipes the
files in `indoor` folder will be part of the study just like any other geometry file in
`/model/opaque` folder.

In this sample case the bottom part of the indoor partition is included in this folder.

![opaque_indoor](https://user-images.githubusercontent.com/38131342/53503555-489c3d80-3a7e-11e9-9679-1b0284243be8.jpg)
