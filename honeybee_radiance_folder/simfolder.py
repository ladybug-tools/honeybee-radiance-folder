import os.path

from honeybee_radiance_folder.folder import ModelFolder
import honeybee_radiance_folder.config as config

try:
    from ConfigParser import SafeConfigParser as CP
except ImportError:
    # python 3
    from configparser import ConfigParser as CP


class SimFolder(ModelFolder):
    __slots__ = ('_sim_folder', '_view_dif_folder')

    def __init__(self, project_folder, sim_folder=None,
                 view_dif_folder='matrices/view_dif',
                 model_folder='model', config_file=None):
        ModelFolder.__init__(project_folder=project_folder, model_folder=model_folder,
                             config_file=config_file)

        self.sim_folder = sim_folder
        self.view_dif_folder = view_dif_folder

    @staticmethod
    def _load_sim_config_file(cfg_file):
        """Load a simfolder config file and return it as JSON."""

        cfg_file = cfg_file or os.path.join(os.path.dirname(__file__), 'simfolder.cfg')
        assert os.path.isfile(cfg_file), 'Failed to find config file at: %s' % cfg_file
        parser = CP()
        parser.read(cfg_file)
        config = {}
        for section in parser.sections():
            config[section] = {}
            for option in parser.options(section):
                config[section][option] = \
                    parser.get(section, option).split('#')[0].strip()
        return config, cfg_file.replace('\\', '/')

    @property
    def sim_folder(self):
        return self._sim_folder

    @sim_folder.setter
    def sim_folder(self, value):
        self._sim_folder = value

    @property
    def view_dif_folder(self):
        return self._view_dif_folder

    @view_dif_folder.setter
    def view_dif_folder(self, value):
        self._view_dif_folder = value

    def write(self):
        pass