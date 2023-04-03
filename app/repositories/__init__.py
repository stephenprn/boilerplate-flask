from typing import Dict, Type

from app.models._common import ModelBase
from app.models.user import User
from app.repositories._common.base import RepositoryBase
from app.repositories.user import UserRepository

MODEL_REPOSITORY_MAPPING: Dict[Type[ModelBase], Type[RepositoryBase]] = {
    User: UserRepository,
}
