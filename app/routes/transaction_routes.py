from flask import Blueprint,session,request,jsonify
from app.services import get_all_ts_dict,add_ts,transaction_to_dict
from datetime import datetime

#创建蓝图
ts_bp = Blueprint("transaction",__name__)


#返回用户所有月支出，默认是当月。
#可选择年月
@ts_bp.route("all_ts",methods=["GET","POST"])
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
@ts_bp.route("add_expense",methods=["POST"])
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

    if result["success"]:
        return jsonify(result),200
    else:
        return jsonify(result),500
  