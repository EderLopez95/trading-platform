class ConfigurationRegistry:
    def __init__(self):
        self._configs = {}

    def register(self, config):
        self._configs[str(config.id)] = config

    def unregister(self, configuration_id: str):
        self._configs.pop(configuration_id, None)

    def all(self):
        return list(self._configs.values())

    def load(self, configs):
        self._configs = {
            str(config.id): config
            for config in configs
        }
    
    def update(self, configuration):
        self._configs[str(configuration.id)] = configuration
