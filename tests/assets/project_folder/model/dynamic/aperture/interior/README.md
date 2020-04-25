# dynamic aperture

`/model/dynamic/aperture/interior`

Interior dynamic apertures are similar to exterior dynamic apertures with the difference
that they receive daylight and sunlight after it passes through another aperture.

Defining an interior aperture is no different than defining an exterior aperture as
discussed in `/model/dynamic/aperture`.

In multi-phase studies, the daylight matrix coefficient calculation of an interior
aperture is calculated against visible exterior apertures.

The best practice is to provide the information for the path of light for each
interior aperture in this folder. Here is a possible schema to define light-paths
for a sensor grid in a room with a side window to an atrium and a skylight:

```json
{
  "sensor_grid_0": {
    "light_path": [
      ["exterior_window", "sky"],
      ["interior_side_window", "atrium-skylight", "sky"]
    ]
  }
}
```
