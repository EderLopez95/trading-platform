from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid

@dataclass
class User:
    id: uuid.UUID
    email: str
    password_hash: str
    telegram_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
