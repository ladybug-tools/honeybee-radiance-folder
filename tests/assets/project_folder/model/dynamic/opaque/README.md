# dynamic opaque geometry

`/model/dynamic/opaque`

Dynamic opaque geometries are useful to model indoor and outdoor opaque geometries
that change during the course of the simulation. A separate simulation for each state of
the dynamic geometry will be executed.

Indoor dynamic geometries will only be included in view matrix calculation while the
outdoor dynamic opaque geometries like a snow-covered ground will only be included in
daylight matrix calculation.

You should use a `states.json` file to indicate the files for each state. In this sample
case we don't have any dynamic opaque geometries but we could have modeled the ground
with two different materials for winter versus summer.

```json
{
  "ground": {
    "0": {
      "name": "grass_covered",
      "default": "ground..summer..000.rad",
      "direct": "ground..direct..000.rad",
    },
    "1": {
      "name": "snow_covered",
      "default": "ground..winter..001.rad",
      "direct": "ground..direct..000.rad"
    }
  }
}

```

Note that we can use the same file with black materials for direct studies.
