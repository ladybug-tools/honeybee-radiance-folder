# -*- coding: utf-8 -*-
import os

from honeybee_radiance_folder import ModelFolder as Folder


def test_grid_mapping():
    folder_path = r'./tests/assets/model_folders/simple/model'
    model_folder = Folder.from_model_folder(folder_path)

    # two phase
    grid_mapping = model_folder.grid_mapping(exclude_static=False, phase=2)
    os.remove(r'./tests/assets/model_folders/simple/grid_mapping.json')
    assert 'two_phase' in grid_mapping
    assert 'three_phase' not in grid_mapping
    assert 'five_phase' not in grid_mapping
    assert len(grid_mapping['two_phase']) == 6

    # three phase
    grid_mapping = model_folder.grid_mapping(exclude_static=False, phase=3)
    os.remove(r'./tests/assets/model_folders/simple/grid_mapping.json')
    assert 'two_phase' in grid_mapping
    assert 'three_phase' in grid_mapping
    assert 'five_phase' not in grid_mapping
    assert len(grid_mapping['two_phase']) == 2
    assert len(grid_mapping['three_phase']) == 4

    # five phase
    grid_mapping = model_folder.grid_mapping(exclude_static=False, phase=5)
    os.remove(r'./tests/assets/model_folders/simple/grid_mapping.json')
    assert 'two_phase' in grid_mapping
    assert 'three_phase' in grid_mapping
    assert 'five_phase' in grid_mapping
    assert len(grid_mapping['two_phase']) == 2
    assert len(grid_mapping['three_phase']) == 4
    assert len(grid_mapping['five_phase']) == 4
