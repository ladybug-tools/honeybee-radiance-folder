# -*- coding: utf-8 -*-
import os
import json
import filecmp

from honeybee_radiance_folder.gridutil import redistribute_sensors, \
    restore_original_distribution
from honeybee_radiance_folder.folderutil import _nukedir


def test_dist_grids():
    input_folder = r'./tests/assets/grids'
    output_folder = r'./tests/assets/temp'
    _nukedir(output_folder, False)
    redistribute_sensors(
        input_folder, output_folder, grid_count=9, min_sensor_count=2000
    )
    files = list(os.listdir(output_folder))
    assert len(files) == 11
    assert '_info.json' in files
    assert '_redist_info.json' in files
    with open(os.path.join(output_folder, '_info.json')) as inf:
        data = json.load(inf)
    assert len(data) == 9
    counts = [d['count'] for d in data]
    assert counts == [2298, 2298, 2298, 2298, 2298, 2298, 2298, 2298, 2300]
    _nukedir(output_folder, False)


def test_rebuild_grids():
    original_folder = r'./tests/assets/grids'
    input_folder = r'./tests/assets/grids_dist'
    output_folder = r'./tests/assets/temp'
    _nukedir(output_folder, False)
    restore_original_distribution(input_folder, output_folder)
    files = [f for f in os.listdir(output_folder) if f.endswith('.pts')]
    # compare the newly created files with the original files and ensure they are
    # identical
    for f in files:
        assert filecmp.cmp(
            os.path.join(original_folder, f), os.path.join(output_folder, f)
        )
    _nukedir(output_folder, False)

def test_dist_grids_split():
    input_folder = r'./tests/assets/grids_split'
    output_folder = r'./tests/assets/temp'
    _nukedir(output_folder, False)
    redistribute_sensors(
        input_folder, output_folder, grid_count=4, min_sensor_count=200
    )
    files = list(os.listdir(output_folder))
    assert len(files) == 6
    assert '_info.json' in files
    assert '_redist_info.json' in files
    with open(os.path.join(output_folder, '_info.json')) as inf:
        data = json.load(inf)
    assert len(data) == 4
    counts = [d['count'] for d in data]
    assert counts == [900, 900, 900, 900]
    with open(os.path.join(output_folder, '_redist_info.json')) as inf:
        data = json.load(inf)
    for i in range(len(data)):
        for j in range(len(data[i]['dist_info'])):
            assert data[i]['dist_info'][j]['end_ln'] != -1
    _nukedir(output_folder, False)

def test_dist_grids_outf_index():
    input_folder = r'./tests/assets/grids_sample_model'
    output_folder = r'./tests/assets/temp'
    _nukedir(output_folder, False)
    redistribute_sensors(
        input_folder, output_folder, grid_count=50, min_sensor_count=1
    )
    files = list(os.listdir(output_folder))
    assert len(files) == 52
    assert '_info.json' in files
    assert '_redist_info.json' in files
    with open(os.path.join(output_folder, '_info.json')) as inf:
        data = json.load(inf)
    assert len(data) == 50
    counts = [d['count'] for d in data]
    assert counts == [20]*49 + [40] 
    with open(os.path.join(output_folder, '_redist_info.json')) as inf:
        data = json.load(inf)
    for i in range(len(data)):
        for j in range(len(data[i]['dist_info'])):
            assert data[i]['dist_info'][j]['identifier'] < 50
    _nukedir(output_folder, False)
