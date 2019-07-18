# dynamic nonopaque geometry

`/model/dynamic/nonopaque`

Dynamic nonopaque geometries are useful to model indoor and outdoor nonopaque geometries
that change during the course of the simulation. A separate simulation for each state of
the dynamic geometry will be executed.

Indoor dynamic geometries will only be included in view matrix calculation while the
outdoor dynamic nonopaque geometries like deciduous trees will only be included in
daylight matrix calculation.

You should use a `states.json` file to indicate the files for each state. In this sample
case we don't have any dynamic nonopaque geometries but adding deciduous trees with
summer and winter conditions could look lik this.

The `JSON` file will look like this:

```json
{
  "outdoor_trees": {
    "0": {
      "name": "summer_condition",
      "default": "trees..summer..000.rad",
      "direct": "trees..direct..000.rad",
    },
    "1": {
      "name": "winter_condition",
      "default": "trees..winter..001.rad",
      "direct": "trees..direct..001.rad"
    }
  }
}

```
