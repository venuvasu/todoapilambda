import uuid
from datetime import UTC, datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class Todo:
    title: str
    completed: bool = False
    id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.now(UTC).replace(tzinfo=None).isoformat()
        self.updated_at = datetime.now(UTC).replace(tzinfo=None).isoformat()
    
    def update(self, /, **kwargs) -> None:  # Python 3.8 positional-only
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ['id', 'created_at']:
                setattr(self, key, value)
        self.updated_at = datetime.now(UTC).replace(tzinfo=None).isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Todo':
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})
