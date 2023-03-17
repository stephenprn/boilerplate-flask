from enum import Enum

from sqlalchemy import asc, desc


class OrderBy(Enum):
    ASC = "ASC"
    DESC = "DESC"


ORDER_BY_CLAUSE_MAPPING = {OrderBy.ASC: asc, OrderBy.DESC: desc}
