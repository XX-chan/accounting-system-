from flask import Flask
from config import get_config

def create_app():
    app = Flask(__name__)

    app.config.from_object(get_config())

    #注册蓝图
    app.register_blueprint(user_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(category_bp)

    return app