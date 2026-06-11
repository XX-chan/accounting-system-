from flask import render_template,Blueprint,request,session,jsonify,render_template
from app.services.user_service import verify_user,create_user


#注册蓝图
user_bp = Blueprint("user",__name__)

#首页
@user_bp.route("/")
def index():
    return render_template("home.html")


#登录页面路由
@user_bp.route("/login-page")
def login_page():
    return render_template("login.html")


#登录
@user_bp.route("/login",methods=["POST"])
def login():
    data = request.form
    if not data:
        return jsonify({
            "success": False,
            "data":None,
            "message":"请求体不能为空"    
        }),400
        
    username=data.get("username")
    password=data.get("password")

    if not username or not password:
        return jsonify({
            "success": False,
            "data":None,
            "message":"用户名和密码不能为空"    
        }),400
        
    user=verify_user(username,password)

    if user:
        session["user_id"]=user.user_id
        return jsonify({
            "success":True,
            "data":None,
            "message":"登陆成功"
        })
    
    return jsonify({
        "success":False,
        "data":None,
        "message":"账号或密码错误"
    })

#注册
@user_bp.route("/register",methods=["POST"])
def register():
  
    data = request.form
    if not data:
        return jsonify({
            "success": False,
            "data":None,
            "message":"请求体不能为空"    
        }),400
        
    username=data.get("username")
    password=data.get("password")
    if not username or not password:
        return jsonify({
            "success": False,
            "data":None,
            "message":"用户名和密码不能为空"    
        }),400
        
    create_user(username,password)
    return jsonify({
        "success":True,
        "data":None,
        "message":"注册成功"
    }),201
    

#注册页面
@user_bp.route("/register-page",methods=["GET"])
def register_page():
    return render_template("register.html")



@user_bp.route("/logout")
def logout():
    session.clear()
    return jsonify({
        "success": True,
        "data":None,
        "message":"已登出"
    }),200
    


