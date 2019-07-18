# -*- coding: utf-8 -*-
from honeybee_radiance_folder import Folder
import os
import shutil


def test_writer():
    """Test creating a new folder."""
    folder_path = r'./tests/assets/temp/rad_folder'
    shutil.rmtree(folder_path, ignore_errors=True)
    rad_folder = Folder(folder_path)
    rad_folder.write()
    
    assert os.path.isdir(folder_path)
    subfolders = [
        f for f in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, f))
    ]

    assert len(subfolders) == 4
    assert 'asset' in subfolders
    assert 'model' in subfolders
    assert 'output' in subfolders
    assert 'system' in subfolders

    # try to remove the folder
    shutil.rmtree(folder_path, ignore_errors=True)


radiance_folder = r'./tests/assets/project_folder'


def test_static_model():
    folder = Folder(radiance_folder)
    files = folder.model.static_nonaperture_files(black_out=False, rel_path=True)
    assert len(files) == 8
    assert r'model\static\opaque\sample_case.mat'.replace('\\', os.sep) in files
    assert r'model\static\opaque\sample_case.rad'.replace('\\', os.sep) in files
    assert r'model\static\opaque\outdoor\context.mat'.replace('\\', os.sep) in files
    assert r'model\static\opaque\outdoor\context.rad'.replace('\\', os.sep) in files
    assert r'model\static\opaque\indoor\partition.mat'.replace('\\', os.sep) in files
    assert r'model\static\opaque\indoor\partition.rad'.replace('\\', os.sep) in files
    assert r'model\static\nonopaque\indoor\partition_glass.mat'.replace('\\', os.sep) in files
    assert r'model\static\nonopaque\indoor\partition_glass.rad'.replace('\\', os.sep) in files


def test_static_aperture():
    folder = Folder(radiance_folder)
    files = folder.model.static_aperture_files(black_out=False, rel_path=True)
    assert r'model\static\aperture\sample_case.mat'.replace('\\', os.sep) in files
    assert r'model\static\aperture\sample_case.rad'.replace('\\', os.sep) in files


def test_dynamic_aperture():
    folder = Folder(radiance_folder)
    apertures = folder.model.dynamic_aperture(interior=False)
    assert len(apertures) == 1
    ap = apertures[0]
    assert ap.states[0].name == 'clear'
    assert ap.states[0].default == 'south_window..default..000.rad'
    assert ap.states[1].name == 'diffuse'
    assert ap.states[1].default == 'south_window..default..001.rad'
