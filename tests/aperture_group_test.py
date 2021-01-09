# -*- coding: utf-8 -*-
from honeybee_radiance_folder import ModelFolder as Folder


def test_static_aperture():
    radiance_folder = r'./tests/assets/project_folder'
    folder = Folder(radiance_folder)
    files = folder.aperture_files(black_out=False, rel_path=True)
    assert 'model/aperture/aperture.mat' in files
    assert 'model/aperture/aperture.rad' in files


def test_aperture_group():
    radiance_folder = r'./tests/assets/project_folder'
    folder = Folder(radiance_folder)
    apertures = folder.aperture_groups(interior=False)
    assert len(apertures) == 1
    ap = apertures[0]
    assert ap.states[0].identifier == '0_clear'
    assert ap.states[0].default == 'south_window..default..000.rad'
    assert ap.states[1].identifier == '1_diffuse'
    assert ap.states[1].default == 'south_window..default..001.rad'
