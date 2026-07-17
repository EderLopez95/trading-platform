class ConfigurationRegistry:
    def __init__(self):
        self._configurations = {}

    def load(self, configurations):
        self._configurations = {
            str(configuration.id): configuration
            for configuration in configurations
        }

    def register(self, configuration):
        self._configurations[str(configuration.id)] = configuration

    def remove(self, configuration_id: str):
        self._configurations.pop(str(configuration_id), None)

    def get_users(self):

        return list(self._configurations.values())

    def count(self):

        return len(self._configurations)
