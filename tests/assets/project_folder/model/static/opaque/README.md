# opaque geometry

`/model/static/opaque`

This folder includes all opaque geometries in the model which are not part of the
apertures. The files must follow a certain naming convention.

1. `<filename>.rad`: Includes Radiance geometries / surfaces.
2. `<filename>.mat`: Includes Radiance materials / modifiers.
3. `<filename>.blk`: Includes the alternative version of the materials in `<filename>.mat`
   file that should be used for direct studies. This file is needed to black out the
   scene when calculating direct sunlight.

In this sample case room geometry as well as ground plane and the neighbor building are
opaque. There is also the bottom part of the partition inside the room which is opaque.

Even though all these geometries can be included in this folder you should separate the
indoor and outdoor geometries from the shell geometries that separate inside of the
building from outside.

Enclosure / Shell geometry (`/model/static/opaque`)

![opaque](https://user-images.githubusercontent.com/38131342/53503554-489c3d80-3a7e-11e9-82c5-0d815a2fda14.jpg)

Outdoor geometry (`/model/static/opaque/outdoor`)
![context](https://user-images.githubusercontent.com/38131342/53503552-4803a700-3a7e-11e9-9083-29614294fa38.jpg)

Indoor geometry (`/model/static/opaque/indoor`)
![opaque_indoor](https://user-images.githubusercontent.com/38131342/53503555-489c3d80-3a7e-11e9-9679-1b0284243be8.jpg)

This separation will help to relax the calculation parameters for view-matrix versus
daylight-matrix in multi-phase daylight simulation.
