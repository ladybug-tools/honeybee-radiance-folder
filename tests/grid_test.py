# -*- coding: utf-8 -*-
from honeybee_radiance_folder import ModelFolder as Folder
import os


def test_grids():
    project_folder = r'./tests/assets/project_folder'
    folder = Folder(project_folder)
    files = folder.grid_files(rel_path=True)
    assert os.path.normpath('model/grid/cubical.pts') in files
    assert os.path.normpath('model/grid/hallway.pts') in files


def test_grids_info():
    project_folder = r'./tests/assets/project_folder'
    folder = Folder(project_folder)
    files = folder.grid_info_files(rel_path=True)
    assert os.path.normpath('model/grid/cubical.json') in files
    assert os.path.normpath('model/grid/hallway.json') in files
