from flask import redirect,url_for,Blueprint,session,request,jsonify,render_template
from app.services.transaction_service import get_monthly_ts_dict,add_transaction,edit_transaction,delete_ts,get_summary,get_all_ts_to_dict
from datetime import datetime

#创建蓝图
ts_bp = Blueprint("transaction",__name__)


#返回用户月支出，默认是当月。
#可选择年月
@ts_bp.route("/all_ts",methods=["GET","POST"])
def all_ts():
    user_id=session.get("user_id")
    if not user_id:
        return jsonify({
            "success": False,
            "data":None,
            "message":"未登录"
            }),401
    
    data=get_monthly_ts_dict(request)
    
    if data:
        return jsonify({
            "success": True,
            "data":data,
            "message":"请求成功"
        }),200
    
    return jsonify({
        "success": False,
        "data":None,
        "message":"请求失败"
    }),400

#历史交易页面路由
@ts_bp.route("/all-ts-page")
def all_ts_page():
    return render_template("transactions.html")

    
#添加交易页面路由
@ts_bp.route("/addts-page")
def add_ts_page():
    return render_template("add_transaction.html")

#添加交易
@ts_bp.route("/add_expense",methods=["POST"])
def add_ts():
    user_id=session.get("user_id")
    if not user_id:
        return render_template("login.html",error="请先登录")
    
    
    data=request.form
    
    if data:
        result=add_transaction(user_id,data)

    if result:
        return redirect(url_for("user.index"))
    else:
        return redirect(url_for("transaction.add_ts_page"))
  
#当月报告,返回当月总支出，总收入，盈余的金额
@ts_bp.route("/monthly-report",methods=["POST"])
def monthly_report():
    user_id=session.get("user_id")
    data=request.get_json()
    year=data.get("year")
    month=data.get("month")
    expense=get_summary(user_id=user_id,year=year,month=month,category_type="expense")
    income=get_summary(user_id=user_id,year=year,month=month,category_type="income")
    remaining=expense-income
    redata={
        "expense":expense,
        "income":income,
        "remaining":remaining
    }
    return jsonify({
        "success": True,
        "data":redata,
        "message":"返回成功"
    }),200


#当月支出前10明细。
@ts_bp.route("/monthly-top",methods=["POST"])
def monthly_top():
    user_id=session.get("user_id")
    data=request.get_json()
    if data:
        redata=get_all_ts_to_dict(user_id,**data)
        return jsonify({
            "success": True,
            "data":redata,
            "message":"获取成功"
        }),200
    
    return jsonify({
        "success": False,
        "data":None,
        "message":"请输入需求"
    }),500

    
    






#编辑交易明细
@ts_bp.route("/edit/<int:ts_id>",methods=["POST"])
def edit_ts(ts_id):
    data=request.get_json()
    user_id=session.get("user_id")
    result=edit_transaction(user_id=user_id,transaction_id=ts_id,**data)
    if result:
        return jsonify({
            "success":True,
            "data":result,
            "message":"修改成功"
        }),200
    return jsonify({
        "success": False,
        "data":None,
        "message":"添加失败"
    }),403


#删除交易
@ts_bp.route("/delete_ts/<int:ts_id>",methods=["DELETE"])
def delete_ts(ts_id):
    user_id=session.get("user_id")
    result=delete_ts(user_id=user_id,transaction_id=ts_id)
    if result:
        return jsonify({
            "success": True,
            "data":None,
            "message":"删除成功"
        }),200
    return jsonify({
        "success": False,
        "data":None,
        "message":"删除失败"
    }),500