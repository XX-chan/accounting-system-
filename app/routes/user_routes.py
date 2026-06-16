from flask import redirect,url_for,render_template,Blueprint,request,session,jsonify,render_template
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
        return render_template("login.html",error="请求体不能为空")
        
    username=data.get("username")
    password=data.get("password")

    if not username or not password:
        return render_template("login.html",error="用户名和密码不能为空")
        
    user=verify_user(username,password)

    if user:
        session["user_id"]=user.user_id
        return redirect(url_for("user.index"))
    
    return render_template("login.html",error="账号或密码错误")

#注册
@user_bp.route("/register",methods=["POST"])
def register():
  
    data = request.form
    if not data:
        return render_template("register.html",error="请求体不能为空")
        
    username=data.get("username")
    password=data.get("password")
    if not username or not password:
        return render_template("register.html",error="用户名和密码不能为空")
        
    create_user(username,password)
    return redirect(url_for("user.login_page"))
    

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
    


