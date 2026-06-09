from flask import Flask
from config import get_config
from flask_sqlalchemy import SQLAlchemy

#创建db实例
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config.from_object(get_config())

    # 将db与app关联
    db.init_app(app)


    from .routes.user_routes import user_bp
    from .routes.transaction_routes import ts_bp
    from .routes.category_routes import cg_bp
    #注册蓝图
    app.register_blueprint(user_bp)
    app.register_blueprint(ts_bp)
    app.register_blueprint(cg_bp)

    return app