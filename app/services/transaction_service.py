from app import db
from app.models import Transaction,User,Category
from operator import and_
from sqlalchemy import extract,func
from app.services.category_service import get_category_id_by_name
from datetime import datetime
from decimal import Decimal


# 根据获得的data，添加交易
def add_transaction(user_id,data):

    category_name=data.get("category_name")
    amount=data.get("amount")
    if not category_name or not amount:
        raise ValueError("分类和金额不能为空")
        
    note=data.get("note")
    category_id=get_category_id_by_name(user_id,category_name)

    if not category_id:
        raise ValueError ("该分类不存在")
       

    date=datetime.now().date()

    transaction=Transaction(
        user_id=user_id,
        category_id=category_id,
        amount=amount,
        date=date,
        note=note,
        )
    
    if transaction:
        db.session.add(transaction)
        db.session.commit()
        return transaction_to_dict(transaction)
    
    else:
        return False
  
    

# user_id和transaction_id,具有唯一性和不可更改性。
def edit_transaction(user_id,transaction_id,**kwargs):
    transaction = get_transaction_by_id(user_id,transaction_id)
    if not transaction:
        raise ValueError("Transaction 不存在")
    
    trans_date=transfer_format(**kwargs)

    for field in ["amount","note","date","category_id"]:
        if field in trans_date:
            setattr(transaction,field,trans_date[field])

    db.session.commit()
    return transaction


#将前端修改的transaction数据格式转化为正确的格式
#date由字符串转为Python的date对象
#amount由字符串转为float
def transfer_format(**kwargs):
    if kwargs["amount"] is not None:
        kwargs["amount"]=Decimal(kwargs.get("amount"))

    kwargs["date"]=datetime.strptime(kwargs.get("date"),"%Y-%m-%d").date()

    return kwargs
    




def delete_trans(user_id,transaction_id):
    transaction = get_transaction_by_id(user_id,transaction_id)
    if not transaction:
        raise ValueError("Transaction不存在")
    
    db.session.delete(transaction)
    db.session.commit()
    return True




# 以下是查询明细方法
# 查询用户某个交易类型的明细
def get_transaction_by_id(user_id,transaction_id):
    transaction =  Transaction.query.filter(
        and_(
            Transaction.transaction_id==transaction_id,Transaction.user_id==user_id
        )
    ).first()
    return transaction


# 查询用户交易明细
# 可以是全部交易明细，也可以按分类类型，分类id，年，月做选择筛选
def get_transactions(user_id,**kwargs):
    query = db.session.query(Transaction,Category.category_name).join(Category).filter(Transaction.user_id==user_id)
    

    category_type=kwargs.get("category_type")
    if category_type:
        query=query.filter(Category.category_type==category_type)

    category_id=kwargs.get("category_id")
    if category_id:
        query=query.filter(Category.category_id==category_id)

    year=kwargs.get("year")
    if year:
        query=query.filter(extract("year",Transaction.date)==year)

    month=kwargs.get("month")
    if month:
        query=query.filter(extract("month",Transaction.date)==month)

    order=kwargs.get("order")
    if order:
        query=query.order_by(Transaction.amount.desc())

    top_n=kwargs.get("top_n")
    if top_n:
        query=query.limit(top_n)

    return query.all()

#返回所有ts明细-字典形式
def get_all_ts_to_dict(user_id,**kwargs):
    transactions=get_transactions(user_id,**kwargs)
    return [transaction_to_dict(t,cn) for t,cn in transactions]


# 用户分类汇总
# 可以筛选分类类型，年，月不同
def get_summary(user_id,**kwargs):
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
        ).join(Category).filter(Transaction.user_id==user_id)
    
    category_type=kwargs.get("category_type")
    if category_type:
        query=query.filter(Category.category_type==category_type)
    
    year=kwargs.get("year")
    if year:
        query=query.filter(extract("year",Transaction.date)==year)

    month=kwargs.get("month")
    if month:
        query=query.filter(extract("month",Transaction.date)==month)
    
    query = query.group_by(Category.category_name)
    query = query.order_by(func.sum(Transaction.amount).desc())

    top_n=kwargs.get("top_n")
    if top_n:
        query=query.limit(top_n)

    result =query.all()

    return sum(row[1] for row in result)


# 路由的辅助方法

#将transactions转为字典格式
def transaction_to_dict(t,cn=None):
    return {
        "transaction_id":t.transaction_id,
        "amount":t.amount,
        "note":t.note,
        "date":t.date.strftime("%Y-%m-%d"),
        "category_id":t.category_id,
        "category_name":cn
       
    }

# 根据获得的data，返回月交易明细(字典类型)
def get_monthly_ts_dict(user_id,data):
    year,month=extra_year_month_from_request(data)

    transactions=get_transactions(
        user_id=user_id,
        year=year,
        month=month
    )
    return [transaction_to_dict(t,cn) for t,cn in transactions]



# 返回用户指定的年月
def extra_year_month_from_request(data):
    
    if data:
        year=data.get("year")
        month=data.get("month")

    #GET请求，使用当前年月
    else:
        year=datetime.now().year
        month=datetime.now().month

    return year,month




