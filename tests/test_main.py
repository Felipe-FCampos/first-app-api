from fastapi.testclient import TestClient

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "First App - API"}

def test_get_contacts():
    response = client.get("/contatos")
    assert response.status_code == 200
    contacts = response.json()
    assert len(contacts) == 5
    assert contacts[0]['firstName'] == 'Lucas'