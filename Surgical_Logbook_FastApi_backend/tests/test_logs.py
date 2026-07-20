
# create a log
def test_create_log(create_log):
    response = create_log()
    assert response.status_code == 201

#read all logs
def test_read_all_logs_only_admin(client, admin_token_headers):
    response = client.get("/logs/", headers=admin_token_headers)

    assert response.status_code == 200
    data = response.json()["data"]

    assert "result" in data
    assert "total" in data
    assert isinstance(data["result"], list)
    assert isinstance(data["total"], int)

def test_read_all_logs_user(client,user_token_headers):
    response = client.get("/logs/",headers=user_token_headers)
    assert response.status_code == 403

# update log
def test_update_log(client, user_token_headers,create_log,updated_log):
    created= create_log()
    log_id = created.json()["data"]["id"]

    response= client.put(f"/logs/{log_id}",headers=user_token_headers,json=updated_log.model_dump(mode="json"))
    assert response.status_code == 200

# delete log
def test_delete_log(client, user_token_headers,create_log):
    created = create_log()
    log_id = created.json()["data"]["id"]

    response = client.delete(f"/logs/{log_id}", headers=user_token_headers)
    assert response.status_code == 204

    get_response = client.get(f"/logs/{log_id}")
    assert get_response.status_code == 404
