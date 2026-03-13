from repositories import CategoriaRepository
from schemas import CategoriaCreateSchema, CategoriaUpdateSchema, CategoriaResponseSchema, CategoriaGetId

respository = CategoriaRepository()

class CategoriaService:

    def criar(self, form: CategoriaCreateSchema):
        """Cria uma nova categoria"""
        resultado = respository.criar_categoria(nome=form.nome)
        if not resultado:
            # https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Reference/Status#respostas_de_erro_do_cliente 
            # 409 = conflito
            return {"erro": "Categoria já existe ou dados inválidos"}, 409 
        return CategoriaResponseSchema.model_validate(resultado).model_dump(), 200
    
    def atualizar(self, id: int, body: CategoriaUpdateSchema):
        """Atualiza uma categoria pelo ID"""
        resultado = respository.atualizar(categoria_id=id, nome=body.nome)
        if not resultado:
            return {"erro": "Categoria não encontrada"}, 404
        return CategoriaResponseSchema.model_validate(resultado).model_dump(), 200
    
    def listar(self):
        """Lista todas as categorias"""
        categorias = respository.listar_categorias()
        return {
            "categorisa": [CategoriaResponseSchema.model_validate(c).model_dump() for c in categorias],
            "total": len(categorias)
        }, 200
    
    def buscar_por_id(self, categoria_id: int):
        """Busca uma categoria pelo ID"""
        resultado = respository.buscar_por_id(categoria_id=categoria_id)
        if not resultado:
            return {"erro": "Categoria não encontrada"}, 404
        return CategoriaResponseSchema.model_validate(resultado).model_dump(), 200
    
    def deletar(self, categoria_id: int):
        """Deleta uma categoria pelo ID"""
        count = respository.deletar_categoria(categoria_id=categoria_id)
        if not count:
            return {"erro": "Categoria não encontrada"}, 404
        return {"mensagem": "Categoria deletada com sucesso"}, 200