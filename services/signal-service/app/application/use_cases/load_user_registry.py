class LoadUserRegistryUseCase:
    def __init__(self, repository, registry):
        self.repository = repository
        self.registry = registry

    def execute(self):
        settings = self.repository.get_all()
        self.registry.load(settings)

        return len(settings)
