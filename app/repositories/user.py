from typing import List, Optional

from sqlalchemy.orm.query import Query

from app.models.user import User

from ._common.base import RepositoryBase


class UserRepository(RepositoryBase[User]):
    model = User

    def _filter_query(
        self,
        query: Query,
        filter_email_in: Optional[List[str]] = None,
        filter_username_in: Optional[List[str]] = None,
        *args,
        **kwargs
    ) -> Query:
        if filter_email_in is not None:
            query = query.filter(self.model.email.in_(filter_email_in))

        if filter_username_in is not None:
            query = query.filter(self.model.username.in_(filter_username_in))

        return self._filter_query_common(query, *args, **kwargs)
