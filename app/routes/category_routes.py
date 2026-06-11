from flask import render_template,Blueprint,session,request,jsonify
from app.services.category_service import category_to_dict,get_categories_dict,delete_category
from app.models import Category

cg_bp=Blueprint("category",__name__)


#新增分类页面路由
@cg_bp.route("/addcg-page")
def add_cg_page():
    return render_template("add_cg.html")


#新增分类
@cg_bp.route("/add_cg",methods=["POST"])
def add_cg():
    user_id=session.get("userid")
    name=request.get_json("category_name")
    type=request.get_json("category_type")
    category=Category(user_id=user_id,category_name=name,category_type=type)
    if category:
        return jsonify({
            "success": True,
            "data":category_to_dict(category),
            "message":"添加分类成功"
        }),200
    return jsonify({
            "success": False,
            "data":None,
            "message":"添加分类失败"
        }),500


#获取不同type的分类明细
@cg_bp.route("/get_cgs/String:cg_type")
def get_categories(cg_type):
    user_id=session.get("user_id")
    categories=get_categories_dict(user_id=user_id,category_type=cg_type)
    if categories:
        return jsonify({
            "success": True,
            "data":categories,
            "message":"请求成功"
        }),200
    return jsonify({
            "success": False,
            "data":None,
            "message":"请求出错"
        }),500


#删除分类
@cg_bp.route("/delete_cg/<int:cg_id>",methods=["DELETE"])
def delete_cg(cg_id):
    user_id=session.get("user_id")
    result=delete_category(user_id=user_id,category_id=cg_id)
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