from app import db

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer,primary_key=True)
    
    username = db.Column(
        db.String(50),
        unique = True,   # 必须唯一
        nullable = False  #不允许为空
        )
    
    password_hash = db.Column(db.String(255),nullable = False)

    create_at = db.Column(db.Date,nullable = False)

