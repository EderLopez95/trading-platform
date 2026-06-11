import json
import os
from pathlib import Path

class SignalTracker:
    def __init__(self, file_name="signal_state.json"):
        base_dir = Path(__file__).resolve().parents[3]
        data_dir = base_dir / "data"
        # create folder if not exists
        data_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = data_dir / file_name
        # create file if not exists
        if not self.file_path.exists():
            self._create_empty_file()
        self.state = self._load()

    def is_duplicate(self, key, candle_time):
        last = self.state.get(key)

        if last == candle_time:
            return True

        self.state[key] = candle_time
        self._save()
        return False
    
    def _create_empty_file(self):
        with open(self.file_path, "w") as f:
            json.dump({}, f)

    def _load(self):
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except:
            return {}
            
    def _save(self):
        # up to 100 records
        if len(self.state) > 100:
            self.state = dict(list(self.state.items())[-100:])

        temp_path = self.file_path.with_suffix(".tmp")
        with open(temp_path, "w") as f:
            json.dump(self.state, f, indent=4)
            f.flush()
            os.fsync(f.fileno())
        temp_path.replace(self.file_path)
