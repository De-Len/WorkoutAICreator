from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class TrainingProgram:
    """Доменная сущность: Программа тренировок"""
    id: UUID = field(default_factory=uuid4)
    user_profile_id: UUID = None
    content: str = None
    created_at: datetime = field(default_factory=datetime.utcnow)