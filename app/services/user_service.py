from app import db
from app.models import User,Category
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy.exc import IntegrityError

# 默认常量分类
DEFAULT_CATEGORIES=[
    {"category_name":"餐饮","category_type":"expense"},
    {"category_name":"交通","category_type":"expense"},
    {"category_name":"购物","category_type":"expense"},
    {"category_name":"住房","category_type":"expense"},
    {"category_name":"其他","category_type":"expense"},
    {"category_name":"工资","category_type":"expense"},
    {"category_name":"兼职","category_type":"expense"},
    {"category_name":"理财","category_type":"expense"},
    {"category_name":"礼金","category_type":"expense"},
    {"category_name":"其他","category_type":"expense"},
]
# 创建新用户
def create_user(username,password):
    existing = User.query.filter_by(username=username).first()
    if existing:
        raise ValueError("用户名已存在")
    
    hash_pw = generate_password_hash(password)
    user = User(username=username, password_hash=hash_pw)
    db.session.add(user)

    #初始化分类
    categories=[
        Category(
            user_id=user.user_id,
            category_name=c["category_name"],
            category_type=c["category_type"]
        )
        for c in DEFAULT_CATEGORIES
    ]
    db.session.add_all(categories)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("用户名已存在")

    return user

# 验证登录，检查用户名和密码
def verify_user(username,password):
    user = User.query.fliter_by(username=username).first()
    if user and check_password_hash(user.password_hash,password):
        return user
    return None 

