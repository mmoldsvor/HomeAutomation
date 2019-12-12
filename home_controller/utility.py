import os
import configparser
import pickle


class ConfigHandler:
    def __init__(self, required_parameters, config_dir):
        self.config = configparser.ConfigParser()
        self.required_parameters = required_parameters
        self.config_dir = config_dir

    def __str__(self):
        return '\n'.join([f'{section.upper()} {option.upper()}: {self.config[section][option]}'
                          for section in self.required_parameters.keys()
                          for option in self.required_parameters[section]])

    def validate(self):
        self.create_config_dir()

        path = os.path.join(self.config_dir, 'config.ini')
        if not os.path.exists(path):
            self.write_config()
        else:
            self.config.read(path)
            if not self.config_is_valid():
                self.write_config()

    def create_config_dir(self):
        """
        Checks if config directory exists. If not it will create it
        """
        if not os.path.exists(self.config_dir):
            print(f'CREATED DIR {self.config_dir}')
            os.makedirs(self.config_dir)

    def write_config(self):
        for section in self.required_parameters.keys():
            self.config.add_section(section)

            for option in self.required_parameters[section]:
                self.config.set(section, option, f'YOUR {section.upper()} {option.upper()} HERE')

        path = os.path.join(self.config_dir, 'config.ini')
        with open(path, 'w') as config_file:
            self.config.write(config_file)

    def config_is_valid(self):
        """
        Checks whether config has all required sections and options
        :return: True if config is valid, False otherwise
        """

        for section in self.required_parameters.keys():
            if not self.config.has_section(section):
                return False

            for option in self.required_parameters[section]:
                if not self.config.has_option(section, option):
                    return False
        return True

    def load_data(self):
        path = os.path.join(self.config_dir, 'data.pickle')
        try:
            with open(path, 'rb') as input_file:
                device_data = pickle.load(input_file)
                sensor_data = pickle.load(input_file)
                return device_data, sensor_data
        except FileNotFoundError:
            with open(path, 'wb') as output_file:
                pickle.dump([], output_file, protocol=pickle.HIGHEST_PROTOCOL)
                pickle.dump([], output_file, protocol=pickle.HIGHEST_PROTOCOL)
        return [], []

    def save_data(self, device_data, sensor_data):
        path = os.path.join(self.config_dir, 'data.pickle')
        with open(path, 'wb') as output_file:
            pickle.dump(device_data, output_file, protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(sensor_data, output_file, protocol=pickle.HIGHEST_PROTOCOL)
