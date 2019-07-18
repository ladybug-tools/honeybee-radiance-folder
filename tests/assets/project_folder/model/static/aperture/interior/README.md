# interior static aperture

`/model/static/aperture/interior`

This folder includes static interior apertures. Similar to static exterior apertures
these apertures have a single material. There is no indoor aperture in this sample case.

## Naming convention

The files in this folder should be named as:

1. `<filename>.rad`: Includes Radiance geometries / surfaces.
2. `<filename>.mat`: Includes Radiance materials / modifiers.

NOTE: There is no need for `.blk` file for interior apertures since they will not be
blacked out from the scene.
