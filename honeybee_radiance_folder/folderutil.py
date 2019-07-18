# -*- coding: utf-8 -*-
"""Utilities for Radiance folder structure."""
import os
import json


class NonApertureState(object):
    """A state for a dynamic non-aperture geometry from Radiance files.
    
    Attributes:
        name
        default
        direct

    Args:
        name (str): Name for state.
        default (str): Path to file to be used for normal representation of the geometry.
        direct (str): Path to file to be used for direct studies.

    """
    def __init__(self, name, default, direct):
        self.name = name
        self.default = default
        self.direct = direct

    @classmethod
    def from_dict(cls, input_dict):
        """Create a state from an input dictionary.

        .. code-block:: python

            {
            "name": "grass_covered",
            "default": "ground..summer..000.rad",
            "direct": "ground..direct..000.rad",
            }
        """
        # TODO: add checks for keys
        name = input_dict['name']
        default = input_dict['default']
        direct = input_dict['direct']
        return cls(name, default, direct)

    def validate(self, folder):
        """Validate files in this state."""
        assert os.path.isfile(os.path.join(folder, self.default)), \
            'Failed to find default file for %s' % self.name
        assert os.path.isfile(os.path.join(folder, self.direct)), \
            'Failed to find direct file for %s' % self.name

    def __repr__(self):
        return 'NonApertureState: {}'.format(self.name)


class ApertureState(NonApertureState):
    """A state for a dynamic aperture from Radiance files.
    
    Attributes:
        name
        default
        direct
        black
        tmtx
        vmtx
        dmtx

    Args:
        name (str): Name for state.
        default (str): Path to file to be used for normal representation of the geometry.
        direct (str): Path to file to be used for direct studies.
        black (str): Path to file for blacking out the window.
        tmtx (str): Path to file for transmittance matrix.
        vmtx (str): Path to file for transmittance matrix.
        dmtx (str): Path to file for transmittance matrix.
    """

    def __init__(self, name, default, direct,
            black=None, tmtx=None, vmtx=None, dmtx=None):
        NonApertureState.__init__(self, name, default, direct)
        self.black = black
        self.tmtx = tmtx
        self.vmtx = vmtx
        self.dmtx = dmtx

    @classmethod
    def from_dict(cls, input_dict):
        """Create a state from an input dictionary.
        
        .. code-block:: python

            {
                "name": "clear",
                "default": "./south_window..default..000.rad",
                "direct": "./south_window..direct..000.rad",
                "black": "./south_window..black.rad",
                "tmtx": "clear.xml",
                "vmtx": "./south_window..mtx.rad",
                "dmtx": "./south_window..mtx.rad"
            }

        """
        # TODO: add checks for keys
        name = input_dict['name']
        default = os.path.normpath(input_dict['default'])
        direct = os.path.normpath(input_dict['direct'])
        try:
            black = input_dict['black']
        except KeyError:
            black = None
        try:
            tmtx = input_dict['tmtx']
        except KeyError:
            tmtx = None
        try:
            vmtx = os.path.normpath(input_dict['vmtx'])
        except KeyError:
            vmtx = None
        try:
            dmtx = os.path.normpath(input_dict['dmtx'])
        except KeyError:
            dmtx = None
        return cls(name, default, direct, black, tmtx, vmtx, dmtx)

    def validate(self, folder):
        """Validate files in this state."""
        assert os.path.isfile(os.path.join(folder, self.default)), \
            'Failed to find default file for %s' % self.name
        assert os.path.isfile(os.path.join(folder, self.direct)), \
            'Failed to find direct file for %s' % self.name
        if self.black is not None:
            assert os.path.isfile(os.path.join(folder, self.black)), \
                'Failed to find black file for %s' % self.name
        if self.tmtx is not None:
            # find the root folder
            try:
                root, _ = folder.split('model')
            except ValueError:
                raise ValueError(
                    'Invalid input folder. See Radiance folder structure.'
                    '\nSee https://github.com/ladybug-tools/radiance-folder-structure#radiance-folder-structure'
                )
            assert os.path.isfile(os.path.join(root, 'model', 'bsdf', self.tmtx)), \
                'Failed to find tmtx file for %s' % self.name
        if self.vmtx is not None:
            assert os.path.isfile(os.path.join(folder, self.vmtx)), \
                'Failed to find vmtx file for %s' % self.name
        if self.dmtx is not None:
            assert os.path.isfile(os.path.join(folder, self.dmtx)), \
                'Failed to find dmtx file for %s' % self.name

    def __repr__(self):
        return 'ApertureState: {}'.format(self.name)


class DynamicNonAperture(object):
    """Representation of a Dynamic nonaperture geometry in Radiance folder.
    
    Attributes:
        name
        states

    Args:
        name (str): Dynamic nonaperture geometry name.
        states(list[NonApertureState]): A list of nonaperture states.
    """

    def __init__(self, name, states):
        self.name = name
        self.states = states

    @classmethod
    def from_dict(cls, input_dict):
        """Create a dynamic aperture from a dictionary.

        .. code-block:: python

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
        """
        keys = list(input_dict.keys())
        assert len(keys) == 1, 'There must be only one window group in input dictionary.'
        name = keys[0]

        states_dict = input_dict[name]
        states = [
            NonApertureState.from_dict(states_dict[str(state)]) 
            for state in range(len(states_dict))
        ]
        return cls(name, states)

    def validate(self, folder):
        """Validate this dynamic geometry."""
        for state in self.states:
            state.validate(folder)

    def __repr__(self):
        return 'DynamicNonAperture: {}'.format(self.name)


class DynamicAperture(DynamicNonAperture):
    """Representation of a Dynamic aperture in Radiance folder.
    
    Attributes:
        name
        states

    Args:
        name: Dynamic aperture name.
        states: A list of aperture states.
    """

    @classmethod
    def from_dict(cls, input_dict):
        """Create a dynamic aperture from a dictionary.

        .. code-block:: python

            {
                "south_window": {
                    "0": {
                    "name": "clear",
                    "default": "./south_window..default..000.rad",
                    "direct": "./south_window..direct..000.rad",
                    "black": "./south_window..black.rad",
                    "tmtx": "clear.xml",
                    "vmtx": "./south_window..mtx.rad",
                    "dmtx": "./south_window..mtx.rad"
                    },
                    "1": {
                    "name": "diffuse",
                    "default": "./south_window..default..001.rad",
                    "direct": "./south_window..direct..001.rad",
                    "black": "./south_window..black.rad",
                    "tmtx": "diffuse50.xml",
                    "vmtx": "./south_window..mtx.rad",
                    "dmtx": "./south_window..mtx.rad"
                    }
                }
            }

        """
        keys = list(input_dict.keys())
        assert len(keys) == 1, 'There must be only one window group in input dictionary.'
        name = keys[0]

        states_dict = input_dict[name]
        states = [
            ApertureState.from_dict(states_dict[str(state)]) 
            for state in range(len(states_dict))
        ]
        return cls(name, states)
    
    def __repr__(self):
        return 'DynamicAperture: {}'.format(self.name)


def parse_dynamic_apertures(states_file, validate=True):
    """Parse dynamic apertures from a state file.
    
    Args:
        states_file: Path to states JSON file.
        validate: Validate the files in states files exist in the folder.
    Returns:
        A list of dynamic apertures
    """
    if not os.path.isfile(states_file):
        return []

    with open(states_file) as inf:
        data = json.load(inf)
    
    apertures = [DynamicAperture.from_dict({key: value}) for key, value in data.items()]

    if validate:
        # check for the files to exist
        folder = os.path.dirname(states_file)
        for aperture in apertures:
            aperture.validate(folder)

    return apertures


def parse_dynamic_nonapertures(states_file, validate=True):
    """Parse dynamic nonaperture geometries from a state file.
    
    Args:
        states_file: Path to states JSON file.
    
    Returns:
        A list of dynamic nonaperture geometries
    """
    if not os.path.isfile(states_file):
        return []

    with open(states_file) as inf:
        data = json.load(inf)

    geometries = [DynamicNonAperture.from_dict({key: value}) for key, value in data.items()]

    if validate:
        # check for the files to exist
        folder = os.path.dirname(states_file)
        for geometry in geometries:
            geometry.validate(folder)

    return geometries
