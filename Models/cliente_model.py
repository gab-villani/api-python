from __future__ import annotations


from pydantic import BaseModel


class ClienteModel(BaseModel):
    id: int
    nome: str
    email: str
    senha: int