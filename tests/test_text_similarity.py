import os
import pytest
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, edit_dist, similarity

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_edit_dist():
    s1 = "Hello"
    s2 = "Hell"
    assert edit_dist(s1, s2) == 1

    s1 = "Hello"
    s2 = " Hello!"
    assert edit_dist(s1, s2) == 2

def test_similarity():
    target = "Hello"
    transcribed = "Hell"
    assert similarity(target, transcribed) == 0.8

def test_text_similarity_perfect_match(client):
    # Open the audio file in binary mode
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'hello.mp3')), 'rb') as audio_file:
        data = {
            'audio': (audio_file, 'hello.mp3')
        }
        response = client.post('/text-similarity/hello', content_type='multipart/form-data', data=data)
    
    # Assertions
    assert response.status_code == 200
    assert response.get_json() == {
        "transcribed": "hello",
        "target": "hello",
        "similarity": 1.0
    }

def test_text_similarity_partial_match(client):
    # Open the audio file in binary mode
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'hello.mp3')), 'rb') as audio_file:
        data = {
            'audio': (audio_file, 'hello.mp3')
        }
        response = client.post('/text-similarity/hell', content_type='multipart/form-data', data=data)
    
    # Assertions
    assert response.status_code == 200
    assert response.get_json() == {
        "transcribed": "hello",
        "target": "hell",
        "similarity": 0.75
    }

def test_text_similarity_no_match(client):
    # Open the audio file in binary mode
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'hello.mp3')), 'rb') as audio_file:
        data = {
            'audio': (audio_file, 'hello.mp3')
        }
        response = client.post('/text-similarity/skibidi', content_type='multipart/form-data', data=data)
    
    # Assertions
    assert response.status_code == 200
    assert response.get_json() == {
        "transcribed": "hello",
        "target": "skibidi",
        "similarity": 0.0
    }
