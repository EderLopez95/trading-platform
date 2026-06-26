class ConfigurationRegistryService:
    def __init__(self, repository, registry):
        self.repository = repository
        self.registry = registry

    def load(self):
        configurations = self.repository.get_enabled()
        self.registry.load(configurations)

        return len(configurations)
