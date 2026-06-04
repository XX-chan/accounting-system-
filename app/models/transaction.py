from app import db

class Transaction(db.Model):

    __tablename__ = "transactions"

    transaction_id = db.Column(db.Integer,primary_key=True)

    amount = db.Column(db.Float,nullable=False)

    note = db.Column(db.String(255))

    date = db.Column(db.Date,nullable=False)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id"),
        nullable=False
    )