from flask import Blueprint,session,request,jsonify
from app.services.transaction_service import get_all_ts_dict,add_ts,edit_transaction,delete_ts
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
    
    data=get_all_ts_dict(request)
    
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

    


#添加交易
@ts_bp.route("/add_expense",methods=["POST"])
def add_ts():
    user_id=session.get("user_id")
    if not user_id:
        return jsonify({
            "success": False,
            "data":None,
            "message":"未登录"
        }),401
    
    data=request.get_json()
    
    result=add_ts(user_id,data)

    if result:
        return jsonify({
            "success":True,
            "data":result,
            "message":"添加成功"
        }),200
    else:
        return jsonify({
            "success": False,
            "data":None,
            "message":"添加失败"
        }),500
  

#编辑交易明细
@ts_bp.route("/edit/<int:ts_id>",methods=["POST"])
def edit_ts(ts_id):
    data=request.get_json()
    user_id=session.get("user_id")
    result=edit_transaction(user_id=user_id,transaction_id=ts_id,kwargs=data)
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
@ts_bp.route("/delets_ts/<int:ts_id>",methods=["DELETE"])
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