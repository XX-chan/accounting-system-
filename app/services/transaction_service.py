from app import db
from app.models import Transaction,User,Category
from operator import and_
from sqlalchemy import extract,func
from app.services.category_service import get_category_id_by_name
from datetime import datetime


# 根据获得的data，添加交易
def add_ts(user_id,data):

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
    
    if "user_id" in kwargs and kwargs["user_id"] != user_id:
        raise ValueError("不允许更改交易所属用户")

    if "transaction_id" in kwargs and kwargs["transatcion_id"] != transaction_id:
        raise ValueError("不允许修改交易ID")

    for field in ["amount","note","date","category_id"]:
        if field in kwargs:
            setattr(transaction,field,kwargs[field])

    db.session.commit()
    return transaction

def delete_ts(user_id,transaction_id):
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
            Transaction.transaction_id==transaction_id,User.user_id==user_id
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


# 路由的辅助方法

#将transactions转为字典格式
def transaction_to_dict(t):
    return {
        "amount":t.amount,
        "note":t.nont,
        "date":t.date,
        "category_id":t.category_id
    }

# 根据获得的data，返回月交易明细(字典类型)
def get_all_ts_dict(user_id,request_obj):
    year,month=extra_year_month_from_request(request_obj)

    transactions=get_transactions(user_id=user_id,year=year,month=month)
    return [transaction_to_dict(t) for t in transactions]


# 返回用户指定的年月
def extra_year_month_from_request(request_obj):
    
    if request_obj.method=="POST":
        data=request_obj.get_json()
        year=data.get("year")
        month=data.get("month")

        if month < 1 or month > 12:
            raise ValueError("月份必须在1-12之间")

    #GET请求，使用当前年月
    else:
        year=datetime.now().year
        month=datetime.now().month

    return year,month




