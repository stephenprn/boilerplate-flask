from typing import Dict, List, Optional
from uuid import uuid4

from sqlalchemy import inspect

from app.database import db
from app.utils.mixin import SerializableMixin


class ModelCommonMeta(type(db.Model), type(SerializableMixin)):
    pass


class ModelCommon(SerializableMixin, db.Model, metaclass=ModelCommonMeta):
    __tablename__: str
    __abstract__ = True
    __exclude_cols_serialize__: List[str] = ["id"]

    def __repr__(self):
        state = inspect(self)

        def get_attr(attr_name: str):
            return repr(getattr(self, attr_name)) if attr_name not in state.unloaded else "<deferred>"

        attrs = " ".join([f"{attr.key}={get_attr(attr.key)}" for attr in state.attrs])
        return f"<{self.__tablename__} {attrs}>"

    def serialize(
        self,
        exclude_cols: Optional[List[str]] = None,
        include_cols: Optional[List[str]] = None,
    ) -> Dict:
        state = inspect(self)
        exclude_cols_ = exclude_cols if exclude_cols is not None else self.__exclude_cols_serialize__

        col_names_to_load = include_cols if include_cols is not None else [col.name for col in self.__mapper__.columns]
        col_names_to_load = list(set(col_names_to_load) - set(exclude_cols_))

        res = {col_name: getattr(self, col_name) for col_name in col_names_to_load}

        # load of relationship propeties
        for rel in state.mapper.relationships:
            key = rel.key

            if key not in state.unloaded:
                value = getattr(self, key)

                if isinstance(value, list):
                    res[key] = [elt.serialize() for elt in value]
                else:
                    res[key] = value.serialize()

        return res


class ModelAssociation(ModelCommon):
    __abstract__ = True


class ModelBase(ModelCommon):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, default=lambda: str(uuid4()), unique=True, nullable=False)

    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    update_date = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )
