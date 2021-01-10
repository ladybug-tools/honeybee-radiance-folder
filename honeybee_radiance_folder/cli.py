import click

import sys
import logging
import os
import json

from honeybee_radiance_folder.folder import ModelFolder as Folder


# command group for all radiance extension commands.
@click.group(help='honeybee folder commands.')
@click.version_option()
def folder():
    pass


_logger = logging.getLogger(__name__)


@folder.command('aperture-files')
@click.argument(
    'radiance-folder', type=click.Path(exists=True, file_okay=False, resolve_path=True)
)
@click.option(
    '-m', '--model', help='Optional name for model folder', default='model',
    show_default=True
)
@click.option(
    '--default/--black', is_flag=True, default=True, show_default=True,
    help='Flag to note whether black material files must be returned.'
)
@click.option(
    '-lf', '--log-file', help='Optional log file to export the output. By default this '
    'will be printed to stdout', type=click.File('w'), default='-'
)
def aperture_files(radiance_folder, model, default, log_file):
    """Return aperture files."""
    try:
        folder = Folder(radiance_folder, model_folder=model)
        black_out = not default
        aperture_files = folder.aperture_files(black_out=black_out)
        log_file.write(json.dumps(aperture_files))
    except Exception as e:
        _logger.exception('Failed to retrieve aperture files.\n{}'.format(e))
        sys.exit(1)
    else:
        sys.exit(0)


@folder.command('scene-files')
@click.argument(
    'radiance-folder', type=click.Path(exists=True, file_okay=False, resolve_path=True)
)
@click.option(
    '-m', '--model', help='Optional name for model folder', default='model',
    show_default=True
)
@click.option(
    '--default/--black', is_flag=True, default=True, show_default=True,
    help='Flag to note whether black material files must be returned.'
)
@click.option(
    '-lf', '--log-file', help='Optional log file to export the output. By default this '
    'will be printed to stdout', type=click.File('w'), default='-'
)
def scene_files(radiance_folder, model, default, log_file):
    """Return scene files."""
    try:
        folder = Folder(radiance_folder, model_folder=model)
        black_out = not default
        scene_files = folder.scene_files(black_out=black_out)
        log_file.write(json.dumps(scene_files))
    except Exception as e:
        _logger.exception('Failed to retrieve scene files.\n{}'.format(e))
        sys.exit(1)
    else:
        sys.exit(0)


@folder.command('grid-files')
@click.argument(
    'radiance-folder', type=click.Path(exists=True, file_okay=False, resolve_path=True)
)
@click.option(
    '-m', '--model', help='Optional name for model folder', default='model',
    show_default=True
)
@click.option(
    '-lf', '--log-file', help='Optional log file to export the output. By default this '
    'will be printed to stdout', type=click.File('w'), default='-'
)
def grid_files(radiance_folder, model, log_file):
    """Return grid files."""
    try:
        folder = Folder(radiance_folder, model_folder=model)
        grid_files = folder.grid_files()
        log_file.write(json.dumps(grid_files))
    except Exception as e:
        _logger.exception('Failed to retrieve grid files.\n{}'.format(e))
        sys.exit(1)
    else:
        sys.exit(0)


@folder.command('grid-info-files')
@click.argument(
    'radiance-folder', type=click.Path(exists=True, file_okay=False, resolve_path=True)
)
@click.option(
    '-m', '--model', help='Optional name for model folder', default='model',
    show_default=True
)
@click.option(
    '-lf', '--log-file', help='Optional log file to export the output. By default this '
    'will be printed to stdout', type=click.File('w'), default='-'
)
def grid_info_files(radiance_folder, model, log_file):
    """Return grid information files."""
    try:
        folder = Folder(radiance_folder, model_folder=model)
        grid_info_files = folder.grid_info_files()
        log_file.write(json.dumps(grid_info_files))
    except Exception as e:
        _logger.exception('Failed to retrieve grid information files.\n{}'.format(e))
        sys.exit(1)
    else:
        sys.exit(0)


@folder.command('view-files')
@click.argument(
    'radiance-folder', type=click.Path(exists=True, file_okay=False, resolve_path=True)
)
@click.option(
    '-m', '--model', help='Optional name for model folder', default='model',
    show_default=True
)
@click.option(
    '-lf', '--log-file', help='Optional log file to export the output. By default this '
    'will be printed to stdout', type=click.File('w'), default='-'
)
def view_files(radiance_folder, model, log_file):
    """Return view files."""
    try:
        folder = Folder(radiance_folder, model_folder=model)
        view_files = folder.view_files()
        log_file.write(json.dumps(view_files))
    except Exception as e:
        _logger.exception('Failed to retrieve view files.\n{}'.format(e))
        sys.exit(1)
    else:
        sys.exit(0)


@folder.command('view-info-files')
@click.argument(
    'radiance-folder', type=click.Path(exists=True, file_okay=False, resolve_path=True)
)
@click.option(
    '-m', '--model', help='Optional name for model folder', default='model',
    show_default=True
)
@click.option(
    '-lf', '--log-file', help='Optional log file to export the output. By default this '
    'will be printed to stdout', type=click.File('w'), default='-'
)
def view_info_files(radiance_folder, model, log_file):
    """Return view information files."""
    try:
        folder = Folder(radiance_folder, model_folder=model)
        view_info_files = folder.view_info_files()
        log_file.write(json.dumps(view_info_files))
    except Exception as e:
        _logger.exception('Failed to retrieve view information files.\n{}'.format(e))
        sys.exit(1)
    else:
        sys.exit(0)


@folder.command('aperture-groups')
@click.argument(
    'radiance-folder', type=click.Path(exists=True, file_okay=False, resolve_path=True)
)
@click.option(
    '-m', '--model', help='Optional name for model folder', default='model',
    show_default=True
)
@click.option(
    '--exterior/--interior', is_flag=True, default=True, show_default=True,
    help='Flag to note whether interior or exterior aperture groups must be returned.'
)
@click.option(
    '-lf', '--log-file', help='Optional log file to export the output. By default this '
    'will be printed to stdout', type=click.File('w'), default='-'
)
def aperture_groups(radiance_folder, model, exterior, log_file):
    """Return aperture groups."""
    try:
        folder = Folder(radiance_folder, model_folder=model)
        aperture_groups = folder.aperture_groups(not exterior, reload=True)
        log_file.write(json.dumps(aperture_groups))
    except Exception as e:
        _logger.exception('Failed to retrieve view files.\n{}'.format(e))
        sys.exit(1)
    else:
        sys.exit(0)


@folder.command('dynamic-scene')
@click.argument(
    'radiance-folder', type=click.Path(exists=True, file_okay=False, resolve_path=True)
)
@click.option(
    '-m', '--model', help='Optional name for model folder', default='model',
    show_default=True
)
@click.option(
    '--outdoor/--indoor', is_flag=True, default=True, show_default=True,
    help='Flag to note whether indoor or outdoor dynamic scene must be returned.'
)
@click.option(
    '-lf', '--log-file', help='Optional log file to export the output. By default this '
    'will be printed to stdout', type=click.File('w'), default='-'
)
def dynamic_scene(radiance_folder, model, outdoor, log_file):
    """Return dynamic scene."""
    try:
        folder = Folder(radiance_folder, model_folder=model)
        dynamic_scene = folder.dynamic_scene(not outdoor, reload=True)
        log_file.write(json.dumps(dynamic_scene))
    except Exception as e:
        _logger.exception('Failed to retrieve view files.\n{}'.format(e))
        sys.exit(1)
    else:
        sys.exit(0)


@folder.command('filter')
@click.argument(
    'radiance-folder', type=click.Path(exists=True, file_okay=False, resolve_path=True)
)
@click.argument('sub-folder')
@click.argument('pattern')
@click.option(
    '-m', '--model', help='Optional name for model folder', default='model',
    show_default=True
)
@click.option(
    '-lf', '--log-file', help='Optional log file to export the output. By default this '
    'will be printed to stdout', type=click.File('w'), default='-'
)
def filter_folder(radiance_folder, model, sub_folder, pattern, log_file):
    """Filter files in a sub_folder inside Radiance folder."""
    try:
        folder = Folder(radiance_folder, model_folder=model)
        files = folder._find_files(subfolder=sub_folder, pattern=pattern)
        log_file.write(json.dumps(files))
    except Exception as e:
        _logger.exception('Failed to filter files inside folder.\n{}'.format(e))
        sys.exit(1)
    else:
        sys.exit(0)

# filter
# {stem, suffix, name, parent}
