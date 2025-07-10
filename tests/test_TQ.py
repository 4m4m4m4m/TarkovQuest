def test_request_index(client):
    response = client.get("/")
    assert response.status_code == 200
    
def test_request_home(client):
    response = client.get("/home")
    assert response.status_code == 200

def test_request_login(client):
    response = client.get("/login")
    assert response.status_code == 200

def test_request_register(client):
    response = client.get("/register")
    assert response.status_code == 200

def test_request_account_unauthorized(client):
    response = client.get("/account")
    assert response.status_code == 302

def test_request_history_unauthorized(client):
    response = client.get("/history")
    assert response.status_code == 302

def test_request_generate_unauthorized(client):
    response = client.get("/generate")
    assert response.status_code == 302

def test_request_account_authorized(authenticated_client):
    response = authenticated_client.get("/account")
    assert response.status_code == 200

def test_request_history_authorized(authenticated_client):
    response = authenticated_client.get("/history")
    assert response.status_code == 200

def test_request_generate_authorized(authenticated_client):
    response = authenticated_client.get("/generate")
    assert response.status_code == 200