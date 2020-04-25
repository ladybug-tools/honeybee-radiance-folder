# dynamic opaque geometry

`/model/dynamic/opaque`

Dynamic opaque geometries are useful to model indoor and outdoor opaque geometries
that change during the course of the simulation. A separate simulation for each state of
the dynamic geometry will be executed.

Indoor dynamic geometries will only be included in view matrix calculation while the
outdoor dynamic opaque geometries like a snow-covered ground will only be included in
daylight matrix calculation.

You should use a `states.json` file to indicate the files for each state. In this sample
case, we don't have any dynamic opaque geometries but we could have modeled the ground
with two different materials for winter versus summer like so:

```json
{
  "ground": [
    {
      "name": "0_grass_covered",
      "default": "ground..summer..000.rad",
      "direct": "ground..direct..000.rad",
    },
    {
      "name": "1_snow_covered",
      "default": "ground..winter..001.rad",
      "direct": "ground..direct..000.rad"
    }
  ]
}

```

Note that the `"direct"` file is only used in direct studies (2-phase and 5-phase)
and, for isolation studies of individual apertures (any phase study with dynamic
apertures), the `"default"` files have to be used.

Because the example here has completely opaque geometry in all states and this
geometry is not changing between states, the same .rad file can be used for
direct studies of all states. So, for the example here of snow-covered ground,
this `"direct"` file contains a "blacked-out" version of the ground geometry.
