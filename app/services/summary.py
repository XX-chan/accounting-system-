from app import db
from app.models import Transaction,User
from sqlalchemy import func




# 以下是汇总相关的方法

#按分类
def summary_by_category(user_id):
    """
    返回用户每个类别的金额
    输出例子：
    {
        "住房":580元,
        "购物":400元,
        "交通":300元,
        "餐饮":800元,
    }
    """
    return (
        db.session.query(
        Transaction.category_id,
        func.sum(Transaction.amount)
        )
        .fliter(Transaction.user_id==user_id)
        .grow_by(Transaction.category_id)
        .all()
    )

# 按月分类
def summary_by_month(user_id):
    """
    返回用户每个月
    """