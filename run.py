from app import creat_app,db

app = creat_app()

with app.app_context:
    db.creat_all()

if __name__ == "__main__":
    app.run(debug=app.config["DEBUGE"])