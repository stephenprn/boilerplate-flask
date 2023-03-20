from app.database import db
from app.enums.user import UserRole
from app.models._common import ModelBase
from app.utils.hash import hash_password


class User(ModelBase):
    __tablename__ = "users"
    __exclude_cols_serialize__ = ["id", "password_hashed", "password_salt"]

    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)

    password_hashed = db.Column(db.String(128), nullable=False)
    password_salt = db.Column(db.String(128), nullable=False)

    def __init__(
        self,
        username: str,
        email: str,
        password: str,
        role: UserRole = UserRole.USER,
    ):
        super().__init__()

        self.username = username
        self.email = email
        self.role = role

        password_hashed, password_salt = hash_password(password)

        self.password_hashed = password_hashed
        self.password_salt = password_salt
