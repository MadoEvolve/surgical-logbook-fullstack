

# testing real user login
def test_login_success(client,test_user):
    response = client.post("/authentication/login",data={"username": test_user.registration,"password": "test123"})

    assert response.status_code == 200

    json_data = response.json()

    assert "access_token" in json_data
    assert json_data["token_type"] == "bearer"

# login helper for pytest users
def login(client, registration, password):

    return client.post("/authentication/login", data= {"username":registration, "password":password})

# test_user login
def test_user_login_success(client, test_user):
    response = login(client, test_user.registration, "test123")
    assert response.status_code == 200

    token = response.json()["access_token"]
    assert token is not None
    assert isinstance(token, str)

# test_admin login
def test_admin_login_success(client, test_admin):
    response = login(client, test_admin.registration, "admin123")
    assert response.status_code == 200

    token = response.json()["access_token"]
    assert token is not None
    assert isinstance(token, str)