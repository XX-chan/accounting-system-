from app import create_app

app = create_app()

#post
# login
def test_login():
    with app.test_client() as client:
        response=client.post("/login",json={
            "username":"test",
            "password":"123"
        })
        print(response.get_json())
  

# register
def test_register():
    with app.test_client() as client:
        response=client.post("/register",json={
            "username":"testregister",
            "password":"456"
        })
        print(response.get_json())

# test_all_ts
def test_all_ts():
    with app.test_client() as client:
        client.post("/all_ts",json={
            "category_name":"交通",
            "amount":"50",
        })
        res=client.get("/all_ts")
        data=res.get_json()
        print(data)

def test_add_ts():
    with app.test_client() as client:
        res=client.post("/add_expense",json={
            "category_type":"购物",
            "amount":"380",
            "note":"买衣服"
        })
        print(res.status_code)
        print(res.get_json())


def test_edit_ts():
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["user_id"] = 1
            res=client.post("/edit/1",json={
                "amount":"46"
            })
            print(res.status_code)
            print(res.get_json())

def test_delete_ts():
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["user_id"]=2
            res=client.delete("/delet_ts/1")

            print(res.status_code)
            print(res.get_json())



# 下面是category routes的测试
def test_add_cg():
    with app.test_client() as client:
        res=client.post("/add_cg",json={
            "category_name":"医疗",
            "category_type":"expense"
        })
        print(res.status_code)
        print(res.get_json())

def test_delete_cg():
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["user_id"]=3
            res=client.delete("/delete_cg/5")
            print(res.status_code)
            print(res.get_json())


if __name__ == "__main__":
    test_login()
    test_register()
    test_all_ts()
    test_add_ts()
    test_edit_ts()
    test_delete_ts()
    test_add_cg()
    test_delete_cg()