import yaml

class ConfigLoader:
    def __init__(self, config_file):
        self.config_file = config_file

    def load_config(self):
        """
        Load configuration from the YAML file.
        """
        with open(self.config_file, "r") as file:
            config = yaml.safe_load(file)
        return config