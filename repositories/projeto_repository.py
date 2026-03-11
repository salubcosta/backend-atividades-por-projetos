from sqlalchemy.exc import IntegrityError
from database.database import Session
from models import Projeto

class ProjetoRepository:

    def criar_projeto(self, nome: str, descricao: str, categoria_id: int):
        with Session() as session:
            projeto = Projeto(nome=nome, descricao=descricao, categoria_id=categoria_id)
            try:
                session.add(projeto)
                session.commit()

                session.refresh(projeto)
                return projeto
            except IntegrityError:
                session.rollback()
                return None
            except Exception: 
                return None
    
    def atualizar(self, projeto_id: int, nome: str, descricao: str, categoria_id: int):
        with Session() as session:
            projeto = session.query(Projeto).filter(Projeto.id == projeto_id).first()

            if not projeto:
                return None
            
            projeto.nome = nome
            projeto.descricao = descricao
            projeto.categoria_id = categoria_id
            try:
                session.commit()
                session.refresh(projeto)
                return projeto
            except IntegrityError:
                session.rollback()
                return None

    def listar_projetos(self):
        with Session() as session:
            return session.query(Projeto).all()
        
    def busar_por_id(self, projeto_id: int):
        with Session() as session:
            return session.query(Projeto).filter(Projeto.id == projeto_id).first()
    
    def deletar_projeto(self, projeto_id: int):
        with Session() as session:
            count = session.query(Projeto).filter(Projeto.id == projeto_id).delete()
            session.commit()
            return count