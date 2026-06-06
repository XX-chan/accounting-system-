from flask import Bluepirnt,request,session,jsonify,render_template
from app.services import verify_user,create_user


#注册蓝图
user_bp = Bluepirnt("user",__name__)

#登录
@user_bp.route("/login",methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False,
            "message":"请求体不能为空"    
        }),400
        
    username=data.get("username")
    password=data.get("password")

    if not username or password:
        return jsonify({
            "success": False,
            "message":"用户名和密码不能为空"    
        }),400
        
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

#注册
@user_bp.route("/register",methods=["POST"])
def register():
  
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False,
            "message":"请求体不能为空"    
        }),400
        
    username=data.get("username")
    password=data.get("password")
    if not username or password:
        return jsonify({
            "success": False,
            "message":"用户名和密码不能为空"    
        }),400
        
    create_user(username,password)
    return jsonify({
        "success":True,
        "message":"注册成功"
    }),201
    

@user_bp.route("/logout")
def logout():
    session.clear()
    return jsonify({
        "success": True,
        "message":"已登出"
    }),200
    


