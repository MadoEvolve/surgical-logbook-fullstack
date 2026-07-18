
def test_create_user_duplicate_registration(client, test_user):

    payload = {
        "username": test_user.username,
        "registration": test_user.registration,
        "email": test_user.email,
        "password": "test123"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Registration already exists!"

# admin only access to all users
def test_admin_read_users_return_list(client, admin_token_headers):
    response = client.get("/users/", headers=admin_token_headers)

    assert response.status_code == 200
    data = response.json()["data"]
    assert isinstance(data, list)

def test_user_read_users(client, user_token_headers):
    response = client.get("/users/", headers=user_token_headers)

    assert response.status_code == 403

# user can read own profile
def test_user_read_own_profile(client, test_user, user_token_headers):

    response = client.get(f"/users/{test_user.id}",headers=user_token_headers)

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["id"] == test_user.id

def test_another_user_read_user(client,test_user,another_user,user_token_headers):

    response= client.get(f"/users/{another_user.id}", headers=user_token_headers)
    assert response.status_code == 403