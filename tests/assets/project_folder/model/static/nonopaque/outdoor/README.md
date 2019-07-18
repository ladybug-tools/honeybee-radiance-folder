# Outdoor nonopaque geometries

`/model/static/nonopaque/outdoor`

This in an optional folder for <u>outdoor-only</u> geometries. File naming convention is
the same as `./model/static/nonopaque`. In 3 and 5 phase simulations these files will
only be included in daylight matrix calculation and will not be part of the view matrix
calculation. Separating the files is helpful to relax Radiance parameters for view matrix
calculation by minimizing the size of the scene.

<u>This folder is only useful for 3-Phase and 5-Phase studies</u>. For other recipes the
files in `outdoor` folder will be part of the scene just like any other geometry file in
`/model/static/nonopaque` folder.

In this sample case there is no outdoor nonopaque geometry.
