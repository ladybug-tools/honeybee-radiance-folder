""" Minimal folder config."""
minimal = {
    'APERTURE': True,
    'APERTURE-GROUP': False,
    'SCENE': True,
    'GRID': False,
    'VIEW': False,
    'INTERIOR-APERTURE-GROUP': False,
    'BSDF': False,
    'IES': False,
    'DYNAMIC-SCENE': False,
    'INDOOR-DYNAMIC-SCENE': False
}

""" Config for model with aperture groups."""
aperture_groups = {
    'APERTURE': True,
    'APERTURE-GROUP': True,
    'SCENE': True,
    'GRID': False,
    'VIEW': False,
    'INTERIOR-APERTURE-GROUP': True,
    'BSDF': False,
    'IES': False,
    'DYNAMIC-SCENE': False,
    'INDOOR-DYNAMIC-SCENE': False
}

"""Full folder with all subfolders."""
full = {k: True for k in minimal}

""" Minimal folder config for simulations"""
sim_minimal = {
    'DC-MATRIX': False,
    'VIEW-MATRIX': False,
    'DAYLIGHT-MATRIX': False,
    'SUN-MATRIX': False,
    'SKY-VECTOR': False,
    'ASSETS': True,
    'TEMP': False,
    'TEMP-ILLUMINANCE': False,
    'TEMP-HDR': False,
    'RESULTS-ILL': False,
    'RESULTS-HDR': False
}

""" Folder configuration for dc-based illuminance simulations"""
sim_DC_ill = {
    'DC-MATRIX': True,
    'VIEW-MATRIX': False,
    'DAYLIGHT-MATRIX': False,
    'SUN-MATRIX': True,
    'SKY-VECTOR': True,
    'ASSETS': True,
    'TEMP': True,
    'TEMP-ILLUMINANCE': True,
    'TEMP-HDR': False,
    'RESULTS-ILL': True,
    'RESULTS-HDR': False
}

""" Folder configuration for three-phase illuminance simulations"""
sim_tph_ill = {
    'DC-MATRIX': False,
    'VIEW-MATRIX': True,
    'DAYLIGHT-MATRIX': True,
    'SUN-MATRIX': False,
    'SKY-VECTOR': True,
    'ASSETS': True,
    'TEMP': True,
    'TEMP-ILLUMINANCE': True,
    'TEMP-HDR': False,
    'RESULTS-ILL': True,
    'RESULTS-HDR': False
}
