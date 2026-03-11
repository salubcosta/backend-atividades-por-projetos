from sqlalchemy.exc import IntegrityError
from database.database import Session
from models import Categoria

class CategoriaRepository:

    def criar_categoria(self, nome: str) -> Categoria:
        with Session() as session:
            categoria = Categoria(nome=nome)
            try:
                session.add(categoria)
                session.commit()

                # Evitar erro de detachedInstanceError
                session.refresh(categoria)
                return categoria
            except IntegrityError:
                session.rollback()
                return None
            except Exception:
                return None
        
    def atualizar(self, categoria_id: int,  nome: str):
        with Session() as session:
            categoria = session.query(Categoria).filter(Categoria.id == categoria_id).first()

            if not categoria:
                return None
            
            categoria.nome = nome

            try:
                session.commit()
                session.refresh(Categoria)
                return categoria
            except IntegrityError:
                session.rollback()
                return None
            except Exception:
                return None

    def listar_categorias(self):
        with Session() as session:
            return session.query(Categoria).all()
    
    def buscar_por_id(self, categoria_id: int):
        with Session() as session:
            return session.query(Categoria).filter(Categoria.id == categoria_id).first()
        
    def deletar_categoria(self, categoria_id: int):
        with Session() as session:
            count = session.query(Categoria).filter(Categoria.id == categoria_id).delete()
            session.commit()
            return count