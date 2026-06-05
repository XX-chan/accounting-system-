from app import db
from app.models import Transaction,User,Category
from operator import and_
from sqlalchemy import extract,func


def add(user_id,category_id,amount,date,note=None):
    transaction = Transaction(
        user_id=user_id,
        category_id=category_id,
        amount=amount,
        date=date,
        note=note
    )
    db.session.add(transaction)
    db.session.commit()
    return transaction

# user_id和transaction_id,具有唯一性和不可更改性。
def edit(user_id,transaction_id,**kwargs):
    transaction = get_transaction_by_id(user_id,transaction_id)
    if not transaction:
        raise ValueError("Transaction 不存在")
    
    if "user_id" in kwargs and kwargs["user_id"] != user_id:
        raise ValueError("不允许更改交易所属用户")

    if "transaction_id" in kwargs and kwargs["transatcion_id"] != transaction_id:
        raise ValueError("不允许修改交易ID")

    for field in ["amount","note","date","category_id"]:
        if field in kwargs:
            setattr(transaction,field,kwargs[field])

    db.session.commit()
    return transaction

def delete(user_id,transaction_id):
    transaction = get_transaction_by_id(user_id,transaction_id)
    if not transaction:
        raise ValueError("Transaction不存在")
    
    db.session.delete(transaction)
    db.session.commit()
    return True




# 以下是查询明细方法
# 查询用户某个交易类型的明细
def get_transaction_by_id(user_id,transaction_id):
    transaction =  Transaction.query.fliter(
        and_(
            Transaction.id==transaction_id,User.id==user_id
        )
    ).first()
    return transaction


# 查询用户交易明细
# 可以是全部交易明细，也可以按分类类型，分类id，年，月做选择筛选
def get_transactions(user_id,category_type=None,category_id=None,year=None,month=None):
    query = Transaction.query.join(Category).fliter_by(Transaction.user_id==user_id)

    if category_type:
        query=query.fliter(Category.category_type==category_type)
    if category_id:
        query=query.fliter(Category.category_id==category_id)
    if year:
        query=query.fliter(extract("year",Transaction.date)==year)
    if month:
        query=query.fliter(extract("month",Transaction.date)==month)

    return query.all()





# 用户分类汇总
# 可以筛选分类类型，年，月不同
def get_summary(user_id,category_type=None,year=None,month=None,top_n=None):
    """
    返回结果格式如下：
    [
    ('餐饮', 5000),
    ('交通', 1800),
    ('住房', 600)
    ]
    """
    query = db.session.query(
        Category.category_name,  #按类名分组
        func.sum(Transaction.amount)              #每组的金额
        ).join(Category).fliter(Transaction.user_id==user_id)
    
    if category_type:
        query=query.fliter(category_type==category_type)
    if year:
        query=query.fliter(extract("year",Transaction.date)==year)
    if month:
        query=query.fliter(extract("month",Transaction.date)==month)
    
    query = query.group_by(Category.category_name)
    query = query.order_by(func.sum(Transaction.amount).desc())

    if top_n:
        query=query.limit(top_n)

    return query.all()




    





