from dataclasses import dataclass

@dataclass
class UserSettings:
    id: str
    user_id: str
    analysis_enabled: bool
