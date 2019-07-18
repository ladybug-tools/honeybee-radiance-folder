# -*- coding: utf-8 -*-
"""
Radiance folder structure module.

This module includes classes for writing and reading to / from a Radiance folder
structure.

See https://github.com/ladybug-tools/radiance-folder-structure#radiance-folder-structure

"""
import os
import json
import itertools
from .folderutil import parse_dynamic_apertures, parse_dynamic_nonapertures


class _FolderCollection(object):
    """Radiance folder base class structure.

    Attributes:
        folder (str): Path to project folder.

    Args:
        folder (str): Path to project folder as a string. The folder will be created
            on write if it doesn't exist already.
    
    """
    REQUIRED = ()
    __slots__ = ('_folder',)

    def __init__(self, folder):
        self._folder = os.path.normpath(folder)

    @property
    def folder(self):
        """Return project folder."""
        return self._folder

    # TODO: extend validation
    def validate(self):
        """Validate folder.
        
        Ensure required subfolders exist.
        """
        folder = self.folder
        # ensure the folder exist
        assert os.path.isdir(folder), '{} folder does not exist!'
        # ensure all the required folders exist
        for subfolder in self.REQUIRED:
            assert os.path.isdir(os.path.join(folder, subfolder)), \
                'Required subfolder "{}" is missing from "{}"'.format(subfolder, folder)

    def _find_files(self, subfolder, ext, rel_path=True):
        """Find files in a subfolder.
        
        Args:
            subfolder (str): A subfolder.
            ext (str): File extention.
            rel_path (bool): Return relative path to root folder.
        """
        folder = os.path.join(self.folder, subfolder)
        filtered_files = [
            os.path.normpath(os.path.join(folder, f)) for f in os.listdir(folder)
            if f.endswith(ext.lower())
        ]

        if rel_path:
            return [os.path.relpath(fi, self.folder) for fi in filtered_files]
        else:
            return filtered_files

    def __repr__(self):
        return '%s: %s' % (self.__class__.__name__, self.folder)


class ModelFolder(_FolderCollection):
    """Model folder.

    Model folder includes all geometry and geometry metadata.

    Args:
        folder (str): Project folder as string. The folder will be created on write
            if it doesn't exist already.

    .. code-block:: shell

        ├───model                     [required]
            ├───bsdf
            ├───dynamic
            │   ├───aperture
            │   │   └───interior
            │   ├───nonopaque
            │   │   ├───indoor
            │   │   └───outdoor
            │   └───opaque
            │       ├───indoor
            │       └───outdoor
            └───static                [required]
                ├───aperture
                │   └───interior
                ├───nonopaque         [required]
                │   ├───indoor
                │   └───outdoor
                └───opaque            [required]
                    ├───indoor
                    └───outdoor

    """

    MODEL_ROOT = 'model'

    STATIC_ROOT = 'model/static'

    STATIC_APERTURE_ROOT = 'model/static/aperture'
    STATIC_APERTURE_EXTERIOR = 'model/static/aperture'
    STATIC_APERTURE_INTERIOR = 'model/static/aperture/interior'
    STATIC_APERTURE = STATIC_APERTURE_EXTERIOR, STATIC_APERTURE_INTERIOR

    STATIC_OPAQUE_ROOT = 'model/static/opaque'
    STATIC_OPAQUE_OUTDOOR = 'model/static/opaque/outdoor'
    STATIC_OPAQUE_INDOOR = 'model/static/opaque/indoor'
    STATIC_OPAQUE = STATIC_OPAQUE_ROOT, STATIC_OPAQUE_OUTDOOR, STATIC_OPAQUE_INDOOR

    STATIC_NONOPAQUE_ROOT = 'model/static/nonopaque'
    STATIC_NONOPAQUE_OUTDOOR = 'model/static/nonopaque/outdoor'
    STATIC_NONOPAQUE_INDOOR = 'model/static/nonopaque/indoor'

    STATIC_NONOPAQUE = STATIC_NONOPAQUE_ROOT, STATIC_NONOPAQUE_OUTDOOR, \
        STATIC_NONOPAQUE_INDOOR

    MODEL_STATIC = (STATIC_ROOT,) + STATIC_APERTURE + STATIC_OPAQUE + STATIC_NONOPAQUE

    DYNAMIC_ROOT = 'model/dynamic'

    DYNAMIC_APERTURE_ROOT = 'model/dynamic/aperture'
    DYNAMIC_APERTURE_EXTERIOR = 'model/dynamic/aperture'
    DYNAMIC_APERTURE_INTERIOR = 'model/dynamic/aperture/interior'
    DYNAMIC_APERTURE = DYNAMIC_APERTURE_EXTERIOR, DYNAMIC_APERTURE_INTERIOR

    DYNAMIC_OPAQUE_ROOT = 'model/dynamic/opaque'
    DYNAMIC_OPAQUE_OUTDOOR = 'model/dynamic/opaque/outdoor'
    DYNAMIC_OPAQUE_INDOOR = 'model/dynamic/opaque/indoor'
    DYNAMIC_OPAQUE = DYNAMIC_OPAQUE_ROOT, DYNAMIC_OPAQUE_OUTDOOR, DYNAMIC_OPAQUE_INDOOR

    DYNAMIC_NONOPAQUE_ROOT = 'model/dynamic/nonopaque'
    DYNAMIC_NONOPAQUE_OUTDOOR = 'model/dynamic/nonopaque/outdoor'
    DYNAMIC_NONOPAQUE_INDOOR = 'model/dynamic/nonopaque/indoor'

    DYNAMIC_NONOPAQUE = DYNAMIC_NONOPAQUE_ROOT, DYNAMIC_NONOPAQUE_OUTDOOR, \
        DYNAMIC_NONOPAQUE_INDOOR

    MODEL_DYNAMIC = (DYNAMIC_ROOT,) + DYNAMIC_APERTURE + DYNAMIC_OPAQUE + \
        DYNAMIC_NONOPAQUE

    BSDF = ('model/bsdf',)

    MODEL = (MODEL_ROOT,) + BSDF + MODEL_DYNAMIC + MODEL_STATIC

    REQUIRED = STATIC_ROOT, STATIC_OPAQUE_ROOT, STATIC_NONOPAQUE_ROOT

    __slots__ =(
        '_dynamic_apertures', '_dynamic_apertures_interior',
        '_dynamic_opaque', '_dynamic_opaque_indoor', '_dynamic_opaque_outdoor',
        '_dynamic_nonopaque', '_dynamic_nonopaque_indoor', '_dynamic_nonopaque_outdoor'
    )

    def __init__(self, folder):
        _FolderCollection.__init__(self, folder)
        self._dynamic_apertures = None
        self._dynamic_apertures_interior = None
        self._dynamic_opaque = None
        self._dynamic_opaque_indoor = None
        self._dynamic_opaque_outdoor = None
        self._dynamic_nonopaque = None
        self._dynamic_nonopaque_indoor = None
        self._dynamic_nonopaque_outdoor = None

    @property
    def root(self):
        """Model root folder."""
        return self.MODEL_ROOT

    def validate(self):
        # TODO: ensure minimum number of files exist
        # TODO: for matrix based studies ensure model_info is available and as expected
        raise NotImplementedError()

    @property
    def has_dynamic_aperture(self):
        """Returns true if model has dynamic aperture."""
        # check if states file exist
        if self._dynamic_apertures is None:
            self._load_dynamic_apertures()
        for aperture in (self._dynamic_apertures, self._dynamic_apertures_interior):
            if len(aperture) > 0:
                return True
        return False

    @property
    def has_dynamic_nonaperture(self):
        """Return True if model has dynamic nonaperture geometries."""
        if self._dynamic_opaque is None:
            self._load_dynamic_nonaperture()
        
        for geo in (
            self._dynamic_opaque, self._dynamic_opaque_indoor,
            self._dynamic_opaque_outdoor, self._dynamic_nonopaque,
                self._dynamic_nonopaque_indoor, self._dynamic_nonopaque_outdoor):
            if len(geo) > 0:
                return True
        return False

    def view_matrix_files(self, aperture):
        """Files to be included in view matrix calculation for an aperture."""
        # find the room and include the room shell geometry.
        # include the blacked out version of the other apertures in the room.
        # include indoor geometries with the room.
        raise NotImplementedError()

    def daylight_matrix_files(self, aperture, receiver=None):
        """Files to be included in daylight matrix calculation for an aperture.
        
        Target can be Sky or another aperture.
        """
        # find the room and include the room shell geometry.
        # include the rest of the scene except for indoor geometries for that room.
        # here is a place that light-path is necessary to be able to know what is indoor
        # and what is outdoor.
        raise NotImplementedError()

    def static_aperture_files(self, black_out=False, rel_path=True):
        """Return list of files for static apertures.

        Args:
            black_out (str): Set black_out to True for "isolated" studies for dynamic
                apertures.
            rel_path (str): Set rel_path to False for getting full path to files. By
                default the path is relative to study folder root.
        """
        material_ext = '.mat' if not black_out else '.blk'
        return self._filter_files(self.STATIC_APERTURE, material_ext, rel_path)

    def static_nonaperture_files(self, black_out=False, rel_path=True):
        """Get list of static files.

        Args:
            black_out (str): Set black_out to True for direct studies.
            rel_path (str): Set rel_path to False for getting full path to files. By
                default the path is relative to study folder root.
        
        """
        material_ext = '.mat' if not black_out else '.blk'
        # collect opaque geometries
        opaque_files = self._filter_files(self.STATIC_OPAQUE, material_ext)
        # collect nonopaque geometries
        non_opaque_files = self._filter_files(self.STATIC_NONOPAQUE, '.mat')
        return opaque_files + non_opaque_files

    def _load_dynamic_apertures(self):
        """Try to load interior and exterior dynamic apertures from folder."""
        int_folder = os.path.join(self.folder, self.DYNAMIC_APERTURE_INTERIOR)
        ext_folder = os.path.join(self.folder, self.DYNAMIC_APERTURE_EXTERIOR)

        self._dynamic_apertures_interior = \
            parse_dynamic_apertures(os.path.join(int_folder, 'states.json'))

        self._dynamic_apertures = \
            parse_dynamic_apertures(os.path.join(ext_folder, 'states.json'))

    def _load_dynamic_nonaperture(self):
        """Try to load indoor and outdoor dynamic nonapertures from folder."""
        opq_folder = os.path.join(self.folder, self.DYNAMIC_OPAQUE_ROOT)
        in_opq_folder = os.path.join(self.folder, self.DYNAMIC_OPAQUE_INDOOR)
        out_opq_folder = os.path.join(self.folder, self.DYNAMIC_OPAQUE_OUTDOOR)
        nonopq_folder = os.path.join(self.folder, self.DYNAMIC_NONOPAQUE_ROOT)
        in_nonopq_folder = os.path.join(self.folder, self.DYNAMIC_NONOPAQUE_INDOOR)
        out_nonopq_folder = os.path.join(self.folder, self.DYNAMIC_NONOPAQUE_OUTDOOR)

        self._dynamic_opaque = \
            parse_dynamic_nonapertures(os.path.join(opq_folder, 'states.json'))

        self._dynamic_opaque_indoor = \
            parse_dynamic_nonapertures(os.path.join(in_opq_folder, 'states.json'))

        self._dynamic_opaque_outdoor = \
            parse_dynamic_nonapertures(os.path.join(out_opq_folder, 'states.json'))

        self._dynamic_nonopaque = \
            parse_dynamic_nonapertures(os.path.join(nonopq_folder, 'states.json'))

        self._dynamic_nonopaque_indoor = \
            parse_dynamic_nonapertures(os.path.join(in_nonopq_folder, 'states.json'))

        self._dynamic_nonopaque_outdoor = \
            parse_dynamic_nonapertures(os.path.join(out_nonopq_folder, 'states.json'))

    def dynamic_aperture(self, interior=False, reload_folder=False):
        """List of dynamic apertures.
        
        Args:
            interior (bool): Boolean switch to return interior dynamic apertures.
            reload_folder (bool): Dynamic geometries are loaded the first time this
                method is called. To reload the files set reload_folder to True.
        Returns:
            A list of dynamic apertures.
        """
        if reload_folder or self._dynamic_apertures is None:
            # load dynamic apertures
            self._load_dynamic_apertures()
        
        return self._dynamic_apertures_interior if interior else self._dynamic_apertures

    def dynamic_nonaperture(self, opaque=True, location=0, reload_folder=False):
        """List of dynamic non-aperture geometries.
        
        Args:
            opaque (bool): A boolean switch to indicate if opaque geometries or nonopaque
                geometries should be returned. Default is True which returns opaque
                geometries.
            location (int): An integer to indicate whether to return the geometries that
                are in the enclosure, on the indoors, or in the outdoor. Default is 0 to
                return enclosure geometries. 1 returns indoor and 2 returns
                outdoor geometries.
            reload_folder (bool): Dynamic geometries are loaded the first time this
                method is called. To reload the files set reload_folder to True.
        """
        if reload_folder or self._dynamic_opaque is None:
            self._load_dynamic_nonaperture()
        assert 0 <= location <=2, \
            'Location must be 0 for enclosure, 1 for indoor or 2 for outdoor.'
        if opaque:
            return self._dynamic_opaque if location == 0 \
                else self._dynamic_opaque_indoor if location == 1 \
                else self._dynamic_opaque_outdoor
        else:
            return self._dynamic_nonopaque if location == 0 \
                else self._dynamic_nonopaque_indoor if location == 1 \
                else self._dynamic_nonopaque_outdoor

    def _filter_files(self, folder_collection, material_ext='.mat', rel_path=True):
        """Filter files in a folder collection.
        
        Args:
            folder_collection (list[str]): A list of subfolders.
            material_ext (str): Expected extension for material files (default: .mat).
            rel_path: A boolean to indicate if folders should be returned as relative
                paths in relation to root folder.
        """
        filtered_files = []
        for sf in folder_collection:
            subfolder = os.path.join(self.folder, sf)
            files = tuple(os.listdir(subfolder))
            for fi in files:
                if not fi.endswith('.rad'):
                    continue
                fn, _ = os.path.splitext(fi)
                # ensure a mat file with the same filename exist
                material_file = os.path.join(subfolder, fn + material_ext)
                assert os.path.isfile(material_file), \
                    'Failed to find the material file: {}'.format(material_file)
                
                filtered_files.extend(
                    [
                        os.path.normpath(os.path.join(subfolder, fn + material_ext)),
                        os.path.normpath(os.path.join(subfolder, fn + '.rad'))
                    ]
                )
        
        if rel_path:
            return [os.path.relpath(fi, self.folder) for fi in filtered_files]
        else:
            return filtered_files

    def write(self, overwrite=False):
        """Write model folder.
        
        Args:
            overwrite (bool): Set to True to overwrite the folder is it already exist.
        """
        root_folder = os.path.join(self.folder, self.root)
        if not overwrite and os.path.isdir(root_folder):
            raise ValueError(
                'Model folder already exist.'
                'Set overwrite to True if you want the folder to be overwritten.'
            )
        for subfolder in self.MODEL:
            directory = os.path.join(self.folder, subfolder)
            if os.path.exists(directory) and not overwrite:
                raise ValueError('{} already exist.'.format(directory))
            os.makedirs(directory)


class AssetFolder(_FolderCollection):
    """Input asset folder.
    
    This folder includes input assets for daylight model. They can be divided into
    senders and receivers.

    .. code-block:: shell

        ├───asset                     [required]
            ├───grid
            ├───ies
            ├───sky
            ├───sun
            └───view
    """
    ASSET_ROOT = 'asset'
    GRID = 'asset/grid'
    IES = 'asset/ies'
    SKY = 'asset/sky'
    SUN = 'asset/sun'
    VIEW = 'asset/view'

    ASSET = ASSET_ROOT, GRID, IES , SKY, SUN, VIEW
    REQUIRED = (ASSET_ROOT,)

    @property
    def root(self):
        """Asset root folder."""
        return self.ASSET_ROOT

    @property
    def ies_folder(self):
        """Electric light ies files folder."""
        return self.IES
    
    def ies_files(self, rel_path=True):
        """List of ies files.

        Args:
            rel_path: A boolean to indicate if folders should be returned as relative
                paths in relation to root folder.
        """
        return self._find_files(self.IES, '.ies', rel_path)

    @property
    def sky_folder(self):
        """Sky files folder."""
        return self.SKY

    def sky_files(self, rel_path=True):
        """List of sky files.
        
        Args:
            rel_path: A boolean to indicate if folders should be returned as relative
                paths in relation to root folder.
        """
        return self._find_files(self.IES, '.sky', rel_path)

    @property
    def sun_folder(self):
        """Sunpath and sun source folder."""
        return self.SUN

    def sun_files(self, rel_path=True):
        """List of sun files.
        
        Args:
            rel_path: A boolean to indicate if folders should be returned as relative
                paths in relation to root folder.
        """
        return self._find_files(self.SUN, '.sun', rel_path)

    @property
    def grid_folder(self):
        """Sensor grids folder."""
        return self.GRID

    def grid_files(self, rel_path=True):
        """List of sensor grid files.
        
        Args:
            rel_path: A boolean to indicate if folders should be returned as relative
                paths in relation to root folder.
        """
        return self._find_files(self.GRID, '.pts', rel_path)

    @property
    def view_folder(self):
        """View files folder."""
        return self.VIEW

    def view_files(self, rel_path=True):
        """List of view files.
        
        Args:
            rel_path: A boolean to indicate if folders should be returned as relative
                paths in relation to root folder.
        """
        return self._find_files(self.VIEW, '.vf', rel_path)

    def write(self, overwrite=True):
        """Write model folder.

        Args:
            overwrite (bool): Set to True to overwrite the folder is it already exist.
        """
        for subfolder in self.ASSET:
            directory = os.path.join(self.folder, subfolder)
            if os.path.exists(directory) and not overwrite:
                raise ValueError('{} already exist.'.format(directory))
            os.makedirs(directory)


# TODO: Add look up for files from output folder.
# unlike other folders output should probably be more flexible on file extension and
# accept a list of extentions. We may need to change this globally.
class OutputFolder(_FolderCollection):
    """Radiance output folder.

    .. code-block:: shell

        ├───output                    [required]
            ├───matrix
            ├───octree
            ├───postprocess
            └───temp
    """
    OUTPUT_ROOT = 'output'
    OCTREE = 'output/octree'
    MATRIX = 'output/matrix'
    TEMP = 'output/temp'
    POSTPROCESS = 'output/postprocess'
    OUTPUT = OUTPUT_ROOT, OCTREE, MATRIX, TEMP, POSTPROCESS
    REQUIRED = (OUTPUT_ROOT,)

    @property
    def root(self):
        """Output root folder."""
        return self.OUTPUT_ROOT

    @property
    def octree(self):
        """Folder for octree files."""
        return self.OCTREE

    @property
    def matrix(self):
        """Matrix outputs folder."""
        return self.MATRIX
    
    @property
    def temp(self):
        """Temporary files folder."""
        return self.TEMP
    
    @property
    def postprocess(self):
        """Postprocess folder."""
        return self.postprocess

    def write(self, overwrite=True):
        """Write model folder.

        Args:
            overwrite (bool): Set to True to overwrite the folder is it already exist.
        """
        for subfolder in self.OUTPUT:
            directory = os.path.join(self.folder, subfolder)
            if os.path.exists(directory) and not overwrite:
                raise ValueError('{} already exist.'.format(directory))
            os.makedirs(directory)


class SystemFolder(_FolderCollection):
    """System folder includes settings for runs like options, tasks.json."""
    SYSTEM_ROOT = 'system'
    SYSTEM = (SYSTEM_ROOT,)
    REQUIRED = (SYSTEM_ROOT,)

    @property
    def root(self):
        """System root folder."""
        return self.SYSTEM_ROOT

    def write(self, overwrite=True):
        """Write model folder.

        Args:
            overwrite (bool): Set to True to overwrite the folder is it already exist.
        """
        for subfolder in self.SYSTEM:
            directory = os.path.join(self.folder, subfolder)
            if os.path.exists(directory) and not overwrite:
                raise ValueError('{} already exist.'.format(directory))
            os.makedirs(directory)


class Folder(object):
    """Radiance folder structure."""

    __version__ = '2.0.1'  # radiance folder version
    def __init__(self, folder):
        """Radiance folder structure.
        
        Args:
            folder: Target folder as a string.
        """
        self._folder = folder
        self._model = ModelFolder(folder)
        self._asset = AssetFolder(folder)
        self._output = OutputFolder(folder)
        self._system = SystemFolder(folder)

    @property
    def version(self):
        """Version for supported folder structure.

        This library might be behind the latest release of radiance folder structure at:
        https://github.com/ladybug-tools/radiance-folder-structure/tags
        """
        return self.__version__

    @property
    def model(self):
        """Model folder structure."""
        return self._model

    @property
    def asset(self):
        """Asset folder structure."""
        return self._asset

    @property
    def output(self):
        """Output folder structure."""
        return self._output

    @property
    def system(self):
        """System folder structure."""
        return self._system

    @property
    def subfolders(self):
        """List of existing subfolders."""
        return itertools.chain(
            self.model.MODEL + self.asset.ASSET
            + self.output.OUTPUT + self.system.SYSTEM
        )

    def write(self, overwrite=True):
        """Write folder.

        Args:
            overwrite (bool): Set to True to overwrite the folder is it already exist.
        """
        self.model.write(overwrite)
        self.asset.write(overwrite)
        self.output.write(overwrite)
        self.system.write(overwrite)
