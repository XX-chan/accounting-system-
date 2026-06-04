from app import db
from app.models import Transaction,User
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
# 查询用户的全部交易明细

def get_user_transaction(user_id):
    return Transaction.query.fliter_by(user_id=user_id).all()


# 查询用户某个交易类型的明细
def get_transaction_by_id(user_id,transaction_id):
    transaction =  Transaction.query.fliter(
        and_(
            Transaction.id==transaction_id,User.id==user_id
        )
    ).first()
    return transaction


# 按分类查询交易明细
def get_transactions_by_category(user_id,category_id):
    return Transaction.query.fliter_by(
        user_id=user_id,
        category_id=category_id
    ).all()

# 按月份查询明细
def get_transactions_by_month(user_id,year,month):
    return Transaction.query.fliter_by(
        Transaction.user_id==user_id,
        extract("year",Transaction.date)==year,
        extract("month",Transaction.date)==month
    ).all()






