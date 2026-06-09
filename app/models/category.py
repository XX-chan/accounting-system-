import enum
from app import db

class CategoryType(enum.Enum):
    income = "income"
    expense = "expense"


class Category(db.Model):

    __tablename__ = "categories"

    category_id = db.Column(db.Integer,primary_key=True)

    category_name = db.Column(
        db.String(50),
        unique = True,
        nullable=False)

    category_type = db.Column(
        db.Enum(CategoryType),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.user_id"),
        nullable=False
    )

