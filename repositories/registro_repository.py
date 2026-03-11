from sqlalchemy.exc import IntegrityError
from database.database import Session
from models import Registro

class RegistroRepository:

    def adicionar_registro(self, descricao: str, projeto_id: int, data = None):
        with Session() as session:
            registro = Registro(descricao=descricao, projeto_id=projeto_id, data=data)
            try:
                session.add(registro)
                session.commit()

                session.refresh(registro)
                return registro
            except IntegrityError:
                session.rollback()
                return None
            except Exception: 
                return None
            
    def atualizar(self, registro_id: int, descricao: str):
        with Session() as session:
            registro = session.query(Registro).filter(Registro.id == registro_id).first()

            if not registro:
                return None
            
            # Só é permitido alterar descricao da atividade
            registro.descricao = descricao

            try:
                session.commit()
                session.refresh(registro)
                return registro
            except IntegrityError:
                session.rollback()
                return None
            except Exception:
                return None
            
    def listar_registros(self, projeto_id: int):
        with Session() as session:
            return session.query(Registro).filter(Registro.projeto_id == projeto_id).all()
    
    def buscar_registro_por_id(self, registro_id: int):
        with Session() as session:
            return session.query(Registro).filter(Registro.id == registro_id).first()
        
    def deletar_registro(self, registro_id: int):
        with Session() as session:
            count = session.query(Registro).filter(Registro.id == registro_id).delete()
            session.commit()
            return count