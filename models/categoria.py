from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.database import Base

class Categoria(Base):
    """
    Model Categoria:
        Responsável pela tabela de Categoria

    Variáveis:
        id: pk da tabela categoria
        nome: nome da categoria
    
    Relacionamento:
        projetos: Todo projeto está relacionado com alguma categoria, Exemplo: Leitura, Curso, Certificação e etc.
    """
    __tablename__ = "categoria"

    id      =   Column(Integer, primary_key=True)
    nome    =   Column(String(100), unique=True, nullable=False)

    # Relacionamento: Infomando para sqlalchemy que a tabela categoria, possui relacionamento com projetos
    
    # back_populates - cria uma referência bidirecional. Então a partir da categoria, 
    # eu consigo buscar um projeto. Exemplo: categoria.projetos e projeto.categoria.nome
    projetos=   relationship("Projeto", back_populates="categoria")