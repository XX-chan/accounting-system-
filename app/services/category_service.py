from app import db
from app.models import User,Category
from app.services import transaction_service
from sqlalchemy.exc import IntegrityError



# 添加新分类
def add_category(user_id,name,type):   
    existing = Category.query.fliter_by(name=name).first()
    if existing:
        raise ValueError("分类名称已存在")
    category = Category(
        user_id=user_id,
        category_name=name,
        category_type=type
    )

    db.session.add(category)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("分类名称已存在")
    
    return category 
     



# 删除分类
def delete_category(user_id,category_id):
    category = get_by_category_id(user_id,category_id)
    if not category:
        return False
    db.session.delete(category)
    db.session.commit()
    return True



# 修改分类
def edit_category(user_id,category_id,**kwargs):
    category = get_by_category_id(user_id,category_id)
    if not category:
        return False
    if "user_id" in kwargs and kwargs[user_id] != user_id:
        raise ValueError("不允许修改所属用户")
    if "category_id" in kwargs and kwargs["category_id"] != category_id:
        raise ValueError("不允许修改分类ID")
    
    for feild in ["category_name","category_type"]:
        setattr(Category,feild,kwargs[feild])

    db.session.commit()
    return category



# 查看用户的所有分类明细
def get_user_category(user_id):
    return Category.query.fliter_by(
        user_id=user_id
    ).all()



# 查询用户的某个分类是否存在
def get_by_category_id(user_id,category_id):
    return Category.query.fliter_by(
        user_id=user_id,
        category_id=category_id
    ).first()



# 通过category_name,获取其category对象
def get_category_id_by_name(user_id,category_name):
    return Category.query.fliter_by(
        user_id=user_id,
        category_name=category_name
    ).first().categroy_id