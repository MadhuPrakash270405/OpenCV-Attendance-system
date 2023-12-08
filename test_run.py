import pytest
import threading
from flask import Flask
from run import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_start_webcam(client):
    response = client.get('/start-webcam')
    assert response.status_code == 200
    assert b"Webcam started" in response.data

def test_stop_webcam(client):
    response = client.get('/stop-webcam')
    assert response.status_code == 200
    assert b"Webcam stopped" in response.data

def test_send_otp(client):
    data = {
        'student_id': '12345'
    }
    response = client.post('/send-otp', json=data)
    assert response.status_code == 200
    assert b"OTP Sent Successful" in response.data

def test_verify_otp(client):
    data = {
        'student_id': '12345',
        'otp': 123456
    }
    response = client.post('/verify-otp', json=data)
    assert response.status_code == 200
    assert b"Valid OTP." in response.data



def test_login(client):
    data = {
        'username': 'admin',
        'password': 'admin'
    }
    response = client.post('/login', json=data)
    assert response.status_code == 200
    assert b"Login Sucessfull" in response.data

def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 200

def test_update_data(client):
    data = {
        'student_id': '12345',
        'total_attendance': 50
    }
    response = client.post('/update', data=data)
    assert response.status_code == 302  # Redirect status code



if __name__ == '__main__':
    pytest.main()
