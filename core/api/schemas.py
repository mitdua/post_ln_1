from pydantic import BaseModel
from typing import Any


class Resposta(BaseModel):
    erro: Any | None = None
    success: Any | None = None

