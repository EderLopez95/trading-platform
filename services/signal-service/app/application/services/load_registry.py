class LoadRegistryUseCase:

    def __init__(
        self,
        repository,
        registry,
    ):
        self.repository = repository

        self.registry = registry

    def execute(self):

        configs = (
            self.repository.get_enabled()
        )

        self.registry.load(configs)
