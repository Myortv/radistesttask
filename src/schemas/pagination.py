from typing import List, Any, Dict, Generic, TypeVar


from pydantic import BaseModel


PaginatedType = TypeVar("PaginatedType")


class Paginated(BaseModel, Generic[PaginatedType]):
    limit: int
    offset: int
    total: int
    data: List[PaginatedType]
