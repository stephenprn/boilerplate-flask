from abc import ABC
from typing import Generic, List, Optional

from sqlalchemy.orm.query import Query
from sqlalchemy.sql.expression import func

from app.repositories._common.filter import FilterInt, FilterText
from app.repositories._common.order_by import ORDER_BY_CLAUSE_MAPPING, OrderBy
from app.types.generic import T_MODEL
from app.types.result import ResultWithNbr


class RepositoryBase(ABC, Generic[T_MODEL]):
    model: T_MODEL

    def list_with_nbr_results(self, *args, **kwargs) -> ResultWithNbr:
        query = self.model.query
        query = self._build_query(query, *args, **kwargs)

        return self._execute_with_nbr_results(query, *args, **kwargs)

    def list_(self, *args, **kwargs) -> List[T_MODEL]:
        query = self.model.query
        query = self._build_query(query, *args, **kwargs)

        return self._execute(query, *args, **kwargs)

    def count(self, *args, **kwargs) -> int:
        query = self.model.query
        query = self._build_query(query, *args, **kwargs)

        return query.count()

    def exists(self, *args, **kwargs) -> bool:
        return self.count(*args, **kwargs) > 0

    def get(self, *args, **kwargs) -> Optional[T_MODEL]:
        kwargs.pop("limit", None)  # we force limit to 1
        kwargs.pop("with_nbr_results", None)  # we want a raw list of results

        results: List[T_MODEL] = self.list_(*args, **kwargs, limit=1)

        return results[0] if results else None

    def _build_query(self, query: Query, *args, **kwargs) -> Query:
        query = self._filter_query(query, *args, **kwargs)
        query = self._load_only(query, *args, **kwargs)
        query = self._eager_load(query, *args, **kwargs)
        query = self._sort_query(query, *args, **kwargs)

        return query

    def _filter_query(self, query: Query, *args, **kwargs) -> Query:
        return self._filter_query_common(query, *args, **kwargs)

    def _load_only(self, query, *args, **kwargs) -> Query:
        return query

    def _eager_load(self, query, *args, **kwargs) -> Query:
        return query

    def _sort_query(self, query, *args, **kwargs) -> Query:
        return self._sort_query_common(query, *args, **kwargs)

    def _sort_query_common(
        self,
        query: Query,
        order_creation_date: Optional[OrderBy] = None,
        order_update_date: Optional[OrderBy] = None,
        order_random: Optional[OrderBy] = None,
        *args,
        **kwargs,
    ) -> Query:
        if order_random:
            query = query.order_by(func.random())

        if order_creation_date is not None:
            order_func = ORDER_BY_CLAUSE_MAPPING[order_creation_date]
            query = query.order_by(order_func(self.model.creation_date))

        if order_update_date is not None:
            order_func = ORDER_BY_CLAUSE_MAPPING[order_update_date]
            query = query.order_by(order_func(self.model.update_date))

        return query

    def _filter_query_common(
        self,
        query: Query,
        filter_uuid_in: Optional[List[str]] = None,
        filter_id_in: Optional[List[int]] = None,
        *args,
        **kwargs,
    ) -> Query:
        if filter_uuid_in is not None:
            query = query.filter(self.model.uuid.in_(filter_uuid_in))

        if filter_id_in is not None:
            query = query.filter(self.model.id.in_(filter_id_in))

        return query

    def _apply_filter_int(self, query: Query, field, filter_int: FilterInt) -> Query:
        if filter_int.min_value is not None:
            if filter_int.min_strict:
                query = query.filter(field > filter_int.min_value)
            else:
                query = query.filter(field >= filter_int.min_value)

        if filter_int.max_value is not None:
            if filter_int.max_strict:
                query = query.filter(field < filter_int.max_value)
            else:
                query = query.filter(field <= filter_int.max_value)

        return query

    def _apply_filter_text(self, query: Query, field, filter_text: FilterText) -> Query:
        if filter_text.text is None:
            return query

        if filter_text.partial_match:
            content = f"%{filter_text.text}%"
        else:
            content = filter_text.text

        if filter_text.ignore_case:
            query = query.filter(field.ilike(content))
        else:
            query = query.filter(field.like(content))

        return query

    def _execute(
        self,
        query: Query,
        nbr_results: Optional[int] = None,
        page_nbr: Optional[int] = None,
        *args,
        **kwargs,
    ) -> List[T_MODEL]:
        if nbr_results is not None:
            query = query.limit(nbr_results)

        if page_nbr is not None and nbr_results is not None:
            query = query.offset(page_nbr * nbr_results)

        return query.all()

    def _execute_with_nbr_results(
        self,
        query: Query,
        nbr_results: Optional[int] = None,
        page_nbr: Optional[int] = None,
        *args,
        **kwargs,
    ) -> ResultWithNbr:
        res = query.paginate(page=(page_nbr or 0) + 1, per_page=nbr_results, error_out=False)
        return ResultWithNbr(total=res.total, data=res.items)
