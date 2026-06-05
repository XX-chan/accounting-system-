from flask import Bluepirnt,request,session,jsonify
from app.services import verify_user

#注册蓝图
user_bp = Bluepirnt("user",__name__)

#登录
@user_bp.route("/login",methods=["POST"])
def login():
    username=request.json["user_name"]
    password=request.json["password"]
    user=verify_user(username,password)
    if user:
        session["user_id"]=user.user_id
        return jsonify({
            "success":True,
            "message":"登陆成功"
        })
    return jsonify({
        "success":False,
        "message":"账号或密码错误"
    })

