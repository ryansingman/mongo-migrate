from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    host: str
    port: int
    database: str
    username: Optional[str]
    password: Optional[str]
