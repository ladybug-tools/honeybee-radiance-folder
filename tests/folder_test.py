from honeybee_radiance.folder import Folder
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


# TODO: Add a test to load the sample folder
