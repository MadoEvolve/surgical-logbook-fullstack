

def test_read_hospitals_return_list(client):
    response = client.get("/hospitals/")

    assert response.status_code == 200
    data = response.json()["data"]
    assert isinstance(data, list)

# Create hospital admin only
def test_admin_create_hospital(client,admin_token_headers,new_hospital):
    response = client.post("/hospitals/", headers=admin_token_headers, json=new_hospital.model_dump())

    assert response.status_code == 201
    data = response.json()["data"]
    assert data["name"] == new_hospital.name.title()
    assert data["location"] == new_hospital.location.title()

def test_user_create_hospital(client, user_token_headers,new_hospital):
    response = client.post("/hospitals/", headers=user_token_headers, json=new_hospital.model_dump())
    assert response.status_code == 403

# get hospital public
def test_read_hospital_by_id(client, admin_token_headers, new_hospital):
    # create hospital first
    new_entry = client.post("/hospitals/",headers=admin_token_headers,json=new_hospital.model_dump())
    created_data = new_entry.json()["data"]
    hospital_id = created_data["id"]

    # test read from created data within the test
    response = client.get(f"/hospitals/{hospital_id}")
    assert response.status_code == 200

    data = response.json()["data"]
    assert data["id"] == hospital_id
    assert data["name"] == new_hospital.name.title()

# Update hospital
def test_update_hospital(client,admin_token_headers,new_hospital,updated_hospital):

    new_entry = client.post("/hospitals/",headers=admin_token_headers,json=new_hospital.model_dump())
    created_data = new_entry.json()["data"]
    hospital_id = created_data["id"]

    response= client.put(f"/hospitals/{hospital_id}",headers=admin_token_headers,json=updated_hospital.model_dump())
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["id"] == hospital_id
    assert data["name"] == updated_hospital.name.title()
    assert data["location"] == updated_hospital.location.title()

def test_user_update_hospital(client,user_token_headers,admin_token_headers,new_hospital,updated_hospital):
    new_entry = client.post("/hospitals/",headers=admin_token_headers,json=new_hospital.model_dump())
    hospital_id = new_entry.json()["data"]["id"]

    response= client.put(f"/hospitals/{hospital_id}",headers=user_token_headers,json=updated_hospital.model_dump())
    assert response.status_code == 403

# Delete hospital
def test_delete_hospital(client,admin_token_headers, new_hospital):
    new_entry = client.post("/hospitals/",headers=admin_token_headers,json=new_hospital.model_dump())
    hospital_id = new_entry.json()["data"]["id"]

    response= client.delete(f"/hospitals/{hospital_id}", headers=admin_token_headers)
    assert response.status_code == 204

    get_response= client.get(f"/hospitals/{hospital_id}")
    assert get_response.status_code == 404

def test_user_delete_hospital(client,user_token_headers,admin_token_headers,new_hospital):
    new_entry = client.post("/hospitals/",headers=admin_token_headers,json=new_hospital.model_dump())
    hospital_id = new_entry.json()["data"]["id"]

    response= client.delete(f"/hospitals/{hospital_id}", headers=user_token_headers)
    assert response.status_code == 403