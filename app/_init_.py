from flask import Flask
from config import get_config
from sqlalchemy import SQLALchemy

#创建db实例
db = SQLALchemy()

def create_app():
    app = Flask(__name__)

    app.config.from_object(get_config())

    # 将db与app关联
    db.init_app(app)


    from routes import user_bp,ts_bp,cg_bp
    #注册蓝图
    app.register_blueprint(user_bp)
    app.register_blueprint(ts_bp)
    app.register_blueprint(cg_bp)

    return app