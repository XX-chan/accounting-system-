from app import db
from app.models import Transaction,Category
from app.services import transaction_service
from sqlalchemy.exc import IntegrityError



# 添加新分类
def add_category(user_id,name,type):   
    existing = Category.query.filter_by(name=name).first()
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
#不允许删除已有记账记录的分类。
def delete_category(user_id,category_id):
    category=get_by_category_id(user_id,category_id)
    if not category:
        raise ValueError("分类不存在")
    
    
    transaction=Transaction.query.filter_by(
        user_id=user_id,
        category_id=category_id
    ).first()

    if transaction:
        raise ValueError("该分类已有记账记录，不能删除")
    
    
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
def get_user_categories(user_id,category_type=None):
    return Category.query.filter_by(
        user_id=user_id,
        category_type=category_type,
    ).all()

# 将category转为字典格式
def category_to_dict(c):
    return {
        "category_name":c.category_name,
        "category_type":c.category_type
    }


# 返回字典类型的分类明细
def get_categories_dict(user_id,category_type=None):
    categories=get_user_categories(user_id,category_type)
    return [category_to_dict(c) for c in categories]


# 查询用户的某个分类是否存在
def get_by_category_id(user_id,category_id):
    return Category.query.filter_by(
        user_id=user_id,
        category_id=category_id
    ).first()



# 通过category_name,获取其category对象
def get_category_id_by_name(user_id,category_name):
    return Category.query.filter_by(
        user_id=user_id,
        category_name=category_name
    ).first().categroy_id


