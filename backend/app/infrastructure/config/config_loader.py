import json
import os
from pathlib import Path
from app.domain.models.config_model import AppConfigModel
from app.domain.exceptions import ConfigNotFoundError

class ConfigLoader:
    def __init__(self, file_name="config.json"):
        base_dir = Path(__file__).resolve().parents[3]
        self.config_dir = base_dir / "config"
        # create folder if not exists
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.config_dir / file_name
        # create file if not exists
        if not self.file_path.exists():
            self._create_default()

    def load(self) -> AppConfigModel:
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
            return AppConfigModel(**data)
        except Exception as e:
            raise ConfigNotFoundError(f"Invalid config file: {e}")
        
    def save(self, config: AppConfigModel):
        data = config.model_dump(mode="json")
        temp_path = self.file_path.with_suffix(".tmp")
        with open(temp_path, "w") as f:
            json.dump(data, f, indent=4)
            f.flush()
            os.fsync(f.fileno())
        temp_path.replace(self.file_path)

    def _create_default(self):
        default_config = AppConfigModel(
            execution_interval=60,
            configurations=[]
        )
        with open(self.file_path, "w") as f:
            json.dump(default_config.model_dump(mode="json"), f, indent=4)
