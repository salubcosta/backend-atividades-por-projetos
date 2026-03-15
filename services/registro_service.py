from repositories import RegistroRepository, ProjetoRepository
from schemas import RegistroCreateSchema, RegistroUpdateSchema, RegistroResponseSchema

repository = RegistroRepository()

class RegistroService:

    def adicionar(self, form: RegistroCreateSchema):
        """Adiciona um novo registro de atividade"""
        repo_projeto = ProjetoRepository()
        projeto = repo_projeto.buscar_por_id(form.projeto_id)
        if not projeto:
            return {"erro": "Projeto não encontrado"}, 404
        
        resultado = repository.adicionar_registro(
            descricao=form.descricao,
            projeto_id=form.projeto_id,
        )
        if not resultado:
            return {"erro": "Erro ao criar registro"}, 409
        return RegistroResponseSchema.model_validate(resultado).model_dump(), 200

    def atualizar(self, registro_id: int, body: RegistroUpdateSchema):
        """Atualiza a descrição de um registro"""

        repo_projeto = ProjetoRepository()
        projeto = repo_projeto.buscar_por_id(body.projeto_id)
        if not projeto:
            return {"erro": "Projeto não encontrado"}, 404
        
        resultado = repository.atualizar(
            registro_id=registro_id,
            descricao=body.descricao
        )
        if not resultado:
            return {"erro": "Registro não encontrado"}, 404
        return RegistroResponseSchema.model_validate(resultado).model_dump(), 200

    def listar(self, projeto_id: int):
        """Lista todos os registros de um projeto"""
        registros = repository.listar_registros(projeto_id=projeto_id)
        return {
            "registros": [RegistroResponseSchema.model_validate(r).model_dump() for r in registros],
            "total": len(registros)
        }, 200

    def buscar_por_id(self, registro_id: int):
        """Busca um registro pelo ID"""
        resultado = repository.buscar_registro_por_id(registro_id=registro_id)
        if not resultado:
            return {"erro": "Registro não encontrado"}, 404
        return RegistroResponseSchema.model_validate(resultado).model_dump(), 200

    def deletar(self, registro_id: int):
        """Deleta um registro pelo ID"""
        count = repository.deletar_registro(registro_id=registro_id)
        if not count:
            return {"erro": "Registro não encontrado"}, 404
        return {"mensagem": "Registro deletado com sucesso"}, 200