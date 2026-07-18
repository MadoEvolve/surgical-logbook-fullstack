

# read all public
def test_read_procedures_return_list(client):
    response = client.get("/procedures/")

    assert response.status_code == 200
    data = response.json()["data"]

    assert isinstance(data, list)

# create procedure admin only
def test_admin_create_procedure(client, admin_token_headers, new_procedure):

    response = client.post("/procedures/",headers=admin_token_headers,json=new_procedure.model_dump())
    assert response.status_code == 201
    data = response.json()["data"]

    assert data["name"] == new_procedure.name.title()
    assert data["specialty"] == new_procedure.specialty.title()

def test_user_create_procedure(client, user_token_headers, new_procedure):

    response = client.post("/procedures/",headers=user_token_headers,json=new_procedure.model_dump())
    assert response.status_code == 403

# get procedure public
def test_read_procedure_by_id(client, admin_token_headers, new_procedure):
    # create procedure first
    new_entry = client.post("/procedures/",headers=admin_token_headers,json=new_procedure.model_dump())
    created_data = new_entry.json()["data"]
    procedure_id = created_data["id"]

    # test read from created data within the test
    response = client.get(f"/procedures/{procedure_id}")
    assert response.status_code == 200

    data = response.json()["data"]
    assert data["id"] == procedure_id
    assert data["name"] == new_procedure.name.title()

# update procedure
def test_update_procedure(client, admin_token_headers, new_procedure, updated_procedure):
    # create procedure first
    new_entry = client.post("/procedures/",headers=admin_token_headers,json=new_procedure.model_dump())
    created_data = new_entry.json()["data"]
    procedure_id = created_data["id"]

    # test update from created data within the test
    response = client.put(f"/procedures/{procedure_id}",headers=admin_token_headers,json=updated_procedure.model_dump())
    assert response.status_code == 200

    data = response.json()["data"]
    assert data["id"] == procedure_id
    assert data["name"] == updated_procedure.name.title()
    assert data["specialty"] == updated_procedure.specialty.title()

def test_user_update_procedure(client, user_token_headers,admin_token_headers,new_procedure,updated_procedure):

    new_entry = client.post("/procedures/",headers=admin_token_headers,json=new_procedure.model_dump())
    procedure_id = new_entry.json()["data"]["id"]

    response = client.put(f"/procedures/{procedure_id}",headers=user_token_headers,json=updated_procedure.model_dump())
    assert response.status_code == 403

# delete procedure
def  test_delete_procedure(client, admin_token_headers, new_procedure):
    new_entry = client.post("/procedures/",headers=admin_token_headers, json=new_procedure.model_dump())
    created_data= new_entry.json()["data"]
    procedure_id = created_data["id"]

    response = client.delete(f"/procedures/{procedure_id}",headers=admin_token_headers)
    assert response.status_code == 204

    get_response = client.get(f"/procedures/{procedure_id}")
    assert get_response.status_code == 404

def test_user_delete_procedure(client, user_token_headers,admin_token_headers,new_procedure):

    new_entry = client.post("/procedures/",headers=admin_token_headers,json=new_procedure.model_dump())
    procedure_id = new_entry.json()["data"]["id"]

    response = client.delete(f"/procedures/{procedure_id}",headers=user_token_headers)

    assert response.status_code == 403