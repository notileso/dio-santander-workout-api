# app/repositories/base.py
import operator
from typing import Any, Generic, TypeVar, AsyncContextManager
from collections.abc import Sequence, Callable
import math

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase



__all__ = ["RepositoryBase", "AsyncSessionCallable", "Page", "PageInput", "get_pagineted_input"]

# Tipos para injeção de dependência da sessão
#type AsyncSessionCallable = Callable[[], AsyncGenerator[AsyncContextManager[AsyncSession, None]]]
AsyncSessionCallable = Callable[[], AsyncContextManager[AsyncSession]]

# Tipos genéricos para o repositório
ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
FilterSchemaType = TypeVar("FilterSchemaType", bound=BaseModel)

T = TypeVar("T")

class PageInput(BaseModel):
    page: int = Field(ge=1, default=1, exclude=True)
    size: int = Field(ge=1, le=100, default=20, exclude=True)
    model_config = ConfigDict(arbitrary_types_allowed=True)

def get_pagineted_input(page: int = 1, size: int = 20) -> PageInput:
    return PageInput(page=page, size=size)

class Page(BaseModel, Generic[T]):
    """Define a estrutura de uma resposta paginada."""
    items: Sequence[T]
    total: int
    page: int
    size: int
    pages: int
    model_config = ConfigDict(arbitrary_types_allowed=True)


class ModelNotFound(Exception):
    pass

class AsyncSessionError(Exception):
    pass

class RepositoryBase(
    Generic[ModelType, CreateSchemaType, UpdateSchemaType, FilterSchemaType]
):
    """
    Classe base para operações CRUD com SQLAlchemy 2.0 Async.

    :param model: O modelo SQLAlchemy da tabela (ex: Company)
    """

    def __init__(
        self,
        model: type[ModelType],
        create_schema: type[CreateSchemaType],
        update_schema: type[UpdateSchemaType],
        filter_schema: type[FilterSchemaType],
        session_callable: AsyncSessionCallable | None = None,
    ):
        self.model = model
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.filter_schema = filter_schema
        self._session_callable = session_callable

        # Mapeia os sufixos do filtro para as funções de operador correspondentes.
        # Nenhuma alteração necessária aqui.
        self.filter_operators: dict[str, Any] = {
            "eq": operator.eq,
            "neq": operator.ne,
            "gt": operator.gt,
            "gte": operator.ge,
            "lt": operator.lt,
            "lte": operator.le,
            "like": lambda col, val: col.like(val), # type: ignore
            "ilike": lambda col, val: col.ilike(val), # type: ignore
            "in": lambda col, val: col.in_(val), # type: ignore
            "notin": lambda col, val: col.not_in(val), # type: ignore
        }
    async def _get_session(self, async_session: AsyncSession | None = None) -> AsyncSession:
        if async_session is None:
            if self._session_callable is None:
                raise AsyncSessionError()
            async with self._session_callable() as async_session:
                return async_session
        return async_session

    async def get(self, id: Any, async_session: AsyncSession | None = None) -> ModelType | None:
        """Busca um objeto pelo seu ID."""
        db_session = await self._get_session(async_session)
        return await db_session.get(self.model, id)

    async def paginate(
        self,
        *,
        filter_in: FilterSchemaType,
        sort_by: dict[str, int] | None = None,
        page: int = 1,
        size: int = 20,
        async_session: AsyncSession | None = None,
    ) -> Page[ModelType]:
        """
        Busca objetos com paginação estruturada, filtro e ordenação.

        Retorna um objeto Page contendo os itens da página e metadados de paginação.

        :param filter_in: Schema com os filtros a serem aplicados.
        :param sort_by: Dicionário para ordenação (ex: {"name": 1} para asc).
        :param page: O número da página a ser retornada (começa em 1).
        :param size: O número de itens por página.
        :param async_session: Sessão SQLAlchemy opcional.
        :return: Um objeto Page com os itens e informações de paginação.
        """
        db_session = await self._get_session(async_session)

        # 1. Construir a query de filtro e ordenação (sem paginação ainda)
        query = select(self.model)
        filter_params = filter_in.model_dump(exclude_none=True, by_alias=True)

        for key, value in filter_params.items():
            field_name, op_suffix = key.rsplit("__", 1) if "__" in key else (key, "eq")
            op_func = self.filter_operators[op_suffix]
            column = getattr(self.model, field_name)
            query = query.where(op_func(column, value))

        # 2. Criar uma query para contar o total de itens que correspondem ao filtro
        # A subquery é usada para garantir que a contagem respeite os filtros
        count_query = select(func.count()).select_from(query.order_by(None).subquery())
        total_items = (await db_session.execute(count_query)).scalar_one()

        # 3. Aplicar ordenação à query principal
        if sort_by:
            for field, direction in sort_by.items():
                column = getattr(self.model, field)
                query = query.order_by(column.desc() if direction == -1 else column.asc())
        
        # 4. Aplicar paginação (offset/limit) para buscar os itens da página
        offset = (page - 1) * size
        paginated_query = query.offset(offset).limit(size)
        
        result = await db_session.execute(paginated_query)
        items = result.scalars().all()

        # 5. Calcular o total de páginas e construir o objeto de resposta
        total_pages = math.ceil(total_items / size) if size > 0 else 0

        return Page(
            items=items,
            total=total_items,
            page=page,
            size=size,
            pages=total_pages,
        )


    async def list_all(
        self, *, skip: int = 0, limit: int = 100, async_session: AsyncSession | None = None
    ) -> Sequence[ModelType]:
        """Busca múltiplos objetos com paginação."""
        db_session = await self._get_session(async_session)
        statement = select(self.model).offset(skip).limit(limit)
        result = await db_session.execute(statement)
        return result.scalars().all()

    async def find_all(
        self,
        *,
        filter_in: FilterSchemaType,
        sort_by: dict[str, int] | None = None,
        skip: int = 0,
        limit: int = 100,
        async_session: AsyncSession | None = None,
    ) -> Sequence[ModelType]:
        """
        Busca objetos com base em um schema de filtro dinâmico e avançado.
        A lógica de construção da query é idêntica à versão síncrona.
        """
        db_session = await self._get_session(async_session)
        statement = select(self.model)
        filter_params = filter_in.model_dump(exclude_none=True, by_alias=True)

        for key, value in filter_params.items():
            field_name, op_suffix = key.rsplit("__", 1) if "__" in key else (key, "eq")

            if op_suffix not in self.filter_operators:
                raise ValueError(f"Operador de filtro '{op_suffix}' não é suportado.")

            op_func = self.filter_operators[op_suffix]
            column = getattr(self.model, field_name, None)

            if column is None:
                raise AttributeError(
                    f"O modelo '{self.model.__name__}' não tem o campo '{field_name}'."
                )

            statement = statement.where(op_func(column, value))
            
        if sort_by:
            for field, direction in sort_by.items():
                column = getattr(self.model, field, None)
                if column is None:
                    raise AttributeError(
                        f"O modelo '{self.model.__name__}' não tem o campo de ordenação '{field}'."
                    )
                if direction == -1:
                    statement = statement.order_by(column.desc())
                elif direction == 1:
                    statement = statement.order_by(column.asc())
                else:
                    raise ValueError(
                        f"Direção de ordenação inválida para '{field}': {direction}. Use 1 para asc ou -1 para desc."
                    )
                    
        statement = statement.offset(skip).limit(limit)
        result = await db_session.execute(statement)
        return result.scalars().all()

    async def find_one(
        self,
        *,
        filter_in: FilterSchemaType,
        sort_by: dict[str, int] | None = None,
        async_session: AsyncSession | None = None
    ) -> ModelType | None:
        """Busca um único objeto com base no filtro."""
        db_session = await self._get_session(async_session)
        db_objs = await self.find_all(filter_in=filter_in, async_session=db_session, limit=1, sort_by=sort_by)
        return db_objs[0] if db_objs else None

    async def create(
        self, *, obj_in: CreateSchemaType | ModelType, async_session: AsyncSession | None = None
    ) -> ModelType:
        """Cria um novo objeto no banco."""
        db_session = await self._get_session(async_session)
        if isinstance(obj_in, self.model):
            db_obj = obj_in
        elif isinstance(obj_in, dict):
            db_obj = self.model(**obj_in)
        elif isinstance(obj_in, self.create_schema):
            db_obj = self.model(**obj_in.model_dump())
        else:
            raise TypeError
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

    async def create_many(
        self, *, obj_in: Sequence[CreateSchemaType], async_session: AsyncSession | None = None
    ) -> Sequence[ModelType]:
        """Cria múltiplos objetos no banco."""
        db_session = await self._get_session(async_session)
        db_objs = [self.model(**obj.model_dump()) for obj in obj_in]
        db_session.add_all(db_objs)
        await db_session.commit()
        for db_obj in db_objs:
            await db_session.refresh(db_obj)
        return db_objs

    async def update(
        self, *, id: Any, obj_in: UpdateSchemaType, async_session: AsyncSession | None = None
    ) -> ModelType:
        """Atualiza um objeto existente no banco."""
        db_session = await self._get_session(async_session)
        db_obj = await self.get(id, async_session=db_session)
        if not db_obj:
            raise ModelNotFound(f"Objeto com ID '{id}' não encontrado.")

        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

    async def remove(self, *, id: Any, async_session: AsyncSession | None = None) -> ModelType | None:
        """Remove um objeto do banco pelo seu ID."""
        db_session = await self._get_session(async_session)
        obj = await db_session.get(self.model, id)
        if obj:
            await db_session.delete(obj)
            await db_session.commit()
        return obj