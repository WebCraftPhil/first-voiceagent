"""
API tests for voice agent endpoints.
Tests voice processing, transcription, and response generation.
"""
import pytest
import base64
from fastapi.testclient import TestClient


class TestVoiceProcessing:
    """Test voice input processing endpoints."""
    
    def test_voice_transcription(self, client):
        """Test converting audio to text."""
        # Mock audio data (base64 encoded)
        audio_data = base64.b64encode(b"fake_audio_data").decode('utf-8')
        
        response = client.post(
            "/api/voice/transcribe",
            json={"audio": audio_data, "format": "webm"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "transcription" in data
        assert isinstance(data["transcription"], str)
    
    def test_voice_response_generation(self, client):
        """Test generating response from voice input."""
        response = client.post(
            "/api/voice/process",
            json={
                "transcription": "What are your hours?",
                "session_id": "test-session-123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "audio_url" in data or "text_response" in data
    
    def test_voice_session_creation(self, client):
        """Test creating a new voice session."""
        response = client.post("/api/voice/session")
        
        assert response.status_code == 201
        data = response.json()
        assert "session_id" in data
        assert "expires_at" in data
    
    def test_voice_session_retrieval(self, client):
        """Test retrieving voice session data."""
        # Create session first
        create_response = client.post("/api/voice/session")
        session_id = create_response.json()["session_id"]
        
        # Retrieve it
        response = client.get(f"/api/voice/session/{session_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == session_id
        assert "history" in data or "messages" in data


@pytest.fixture
def client():
    """Create a test client for the API."""
    # Replace with your actual FastAPI app import
    # from app.main import app
    # return TestClient(app)
    
    # Placeholder - replace with actual implementation
    class MockClient:
        def post(self, endpoint, json=None):
            if "transcribe" in endpoint:
                return type('Response', (), {
                    'status_code': 200,
                    'json': lambda: {'transcription': 'test transcription'}
                })()
            elif "process" in endpoint:
                return type('Response', (), {
                    'status_code': 200,
                    'json': lambda: {'response': 'Our hours are 9-5', 'text_response': 'Our hours are 9-5'}
                })()
            elif "session" in endpoint:
                return type('Response', (), {
                    'status_code': 201,
                    'json': lambda: {'session_id': 'test-session-123', 'expires_at': '2024-12-31T23:59:59'}
                })()
        
        def get(self, endpoint):
            return type('Response', (), {
                'status_code': 200,
                'json': lambda: {'session_id': 'test-session-123', 'history': []}
            })()
    
    return MockClient()
