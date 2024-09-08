from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import date
import re

app = FastAPI()

# Modelo de dados atualizado
class User(BaseModel):
    nome: str
    cpf: str
    data_nascimento: date

    # Validação simples para CPF
    @classmethod
    def validar_cpf(cls, cpf):
        cpf = re.sub(r'\D', '', cpf)  # Remove caracteres não numéricos
        if len(cpf) != 11:
            raise ValueError("CPF inválido")
        return cpf

# Lista de usuários armazenados (simulação)
usuarios: List[User] = []

# Rota para listar todos os usuários
@app.get("/usuarios", summary="Listar todos os usuários", description="Retorna uma lista de todos os usuários cadastrados.")
def listar_usuarios():
    return usuarios

# Rota para adicionar um novo usuário
@app.post("/usuarios", summary="Adicionar um novo usuário", response_description="O usuário foi adicionado com sucesso.")
def adicionar_usuario(usuario: User):
    # Validação de CPF (opcional, pode ser ajustada conforme regras)
    try:
        usuario.cpf = User.validar_cpf(usuario.cpf)
    except ValueError as e:
        return {"message": str(e)}
    
    usuarios.append(usuario)
    return {"message": "Usuário adicionado com sucesso"}

# Rota para buscar um usuário por índice
@app.get("/usuarios/{usuario_id}", summary="Obter um usuário por ID", description="Retorna os detalhes de um usuário específico.")
def obter_usuario(usuario_id: int):
    if usuario_id >= len(usuarios) or usuario_id < 0:
        return {"message": "Usuário não encontrado"}, 404
    return usuarios[usuario_id]