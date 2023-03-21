from typing import List, Optional

from app.models.user import User
from app.repositories._common.order_by import OrderBy
from app.repositories.user import UserRepository

repo_user = UserRepository()


def list_(nbr_results: int, page_nbr: int) -> List[User]:
    return repo_user.list_(
        nbr_results=nbr_results,
        page_nbr=page_nbr,
        order_creation_date=OrderBy.DESC,
        with_nbr_results=True,
    )


def get(uuid: str) -> Optional[User]:
    return repo_user.get(filter_uuid_in=[uuid])
