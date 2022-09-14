from __future__ import annotations

from pydantic import BaseModel


class UsuarioModel(BaseModel):
    id: int
    nome: str
