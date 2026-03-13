from repositories import ProjetoRepository, CategoriaRepository
from schemas import ProjetoCreateSchema, ProjetoUpdateSchema, ProjetoResponseSchema

repository = ProjetoRepository()

class ProjetoService:
    def criar(self, form: ProjetoCreateSchema):
        """Cria um novo projeto"""
        repo_categoria = CategoriaRepository()
        categoria = repo_categoria.buscar_por_id(form.categoria_id)
        if not categoria:
            return {"erro": "Categoria não encontrada"}, 404
        
        resultado = repository.criar_projeto(
            nome=form.nome,
            descricao=form.descricao,
            categoria_id=form.categoria_id
        )
        if not resultado:
            return {"erro": "Projeto já existe ou dados inválidos"}, 400
        return ProjetoResponseSchema.model_validate(resultado).model_dump(), 200
    
    def atualizar(self, id: int, body: ProjetoUpdateSchema):
        """Atualiza um projeto pelo ID"""
        repo_categoria = CategoriaRepository()
        categoria = repo_categoria.buscar_por_id(categoria_id=body.categoria_id)

        if not categoria:
            return {"erro": "Categoria não encontrada"}, 404

        resultado = repository.atualizar(
            projeto_id=id,
            nome=body.nome,
            descricao=body.descricao,
            categoria_id=body.categoria_id
        )
        if not resultado:
            return {"erro": "Projeto não encontrado"}, 404
        return ProjetoResponseSchema.model_validate(resultado).model_dump(), 200
    
    def listar(self):
        """Lista todos os projetos"""
        projetos = repository.listar_projetos()
        return {
            "projetos": [ProjetoResponseSchema.model_validate(p).model_dump() for p in projetos],
            "total": len(projetos)
            }, 200
        
    def buscar_por_id(self, projeto_id: int):
        """Busca um projeto pelo ID"""
        resultado = repository.buscar_por_id(projeto_id=projeto_id)
        if not resultado:
            return {"erro": "Projeto não encontrado"}, 404
        return ProjetoResponseSchema.model_validate(resultado).model_dump(), 200

    def deletar(self, projeto_id: int):
        """Deleta um projeto pelo ID"""
        count = repository.deletar_projeto(projeto_id=projeto_id)
        if not count:
            return {"erro": "Projeto não encontrado"}, 404
        return {"mensagem": "Projeto deletado com sucesso"}, 200