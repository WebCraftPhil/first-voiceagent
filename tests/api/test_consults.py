"""
API tests for consult scheduling endpoints.
Tests the backend API for creating, retrieving, and managing consults.
"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

# Assuming your FastAPI app is in app.main
# from app.main import app
# client = TestClient(app)

# For now, using a placeholder - replace with your actual app
BASE_URL = "http://localhost:8000/api"


class TestConsultScheduling:
    """Test consult scheduling functionality."""
    
    def test_create_consult_success(self, client):
        """Test successful consult creation."""
        consult_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "preferred_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "duration_minutes": 30,
            "notes": "Initial consultation"
        }
        
        response = client.post("/consults", json=consult_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == consult_data["name"]
        assert data["email"] == consult_data["email"]
        assert "id" in data
        assert "created_at" in data
    
    def test_create_consult_missing_required_fields(self, client):
        """Test consult creation with missing required fields."""
        incomplete_data = {
            "name": "John Doe"
            # Missing email, which should be required
        }
        
        response = client.post("/consults", json=incomplete_data)
        assert response.status_code == 422  # Validation error
    
    def test_get_consult_by_id(self, client):
        """Test retrieving a specific consult by ID."""
        # First create a consult
        consult_data = {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "preferred_date": (datetime.now() + timedelta(days=5)).isoformat()
        }
        create_response = client.post("/consults", json=consult_data)
        consult_id = create_response.json()["id"]
        
        # Then retrieve it
        response = client.get(f"/consults/{consult_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == consult_id
        assert data["name"] == consult_data["name"]
    
    def test_get_all_consults(self, client):
        """Test retrieving all consults."""
        response = client.get("/consults")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # If there are consults, verify structure
        if len(data) > 0:
            assert "id" in data[0]
            assert "name" in data[0]
            assert "email" in data[0]
    
    def test_schedule_conflict_detection(self, client):
        """Test that overlapping consults are rejected."""
        base_time = datetime.now() + timedelta(days=1)
        
        # Create first consult
        consult1 = {
            "name": "Client A",
            "email": "clienta@example.com",
            "preferred_date": base_time.isoformat(),
            "duration_minutes": 30
        }
        client.post("/consults", json=consult1)
        
        # Try to create overlapping consult
        consult2 = {
            "name": "Client B",
            "email": "clientb@example.com",
            "preferred_date": (base_time + timedelta(minutes=15)).isoformat(),
            "duration_minutes": 30
        }
        response = client.post("/consults", json=consult2)
        
        assert response.status_code == 409  # Conflict
    
    def test_update_consult_status(self, client):
        """Test updating consult status (e.g., confirmed, cancelled)."""
        # Create consult
        consult_data = {
            "name": "Test User",
            "email": "test@example.com",
            "preferred_date": (datetime.now() + timedelta(days=3)).isoformat()
        }
        create_response = client.post("/consults", json=consult_data)
        consult_id = create_response.json()["id"]
        
        # Update status
        response = client.patch(
            f"/consults/{consult_id}",
            json={"status": "confirmed"}
        )
        
        assert response.status_code == 200
        assert response.json()["status"] == "confirmed"
    
    def test_delete_consult(self, client):
        """Test deleting a consult."""
        # Create consult
        consult_data = {
            "name": "To Delete",
            "email": "delete@example.com",
            "preferred_date": (datetime.now() + timedelta(days=2)).isoformat()
        }
        create_response = client.post("/consults", json=consult_data)
        consult_id = create_response.json()["id"]
        
        # Delete it
        response = client.delete(f"/consults/{consult_id}")
        assert response.status_code == 204
        
        # Verify it's gone
        get_response = client.get(f"/consults/{consult_id}")
        assert get_response.status_code == 404


class TestFAQEndpoints:
    """Test FAQ-related endpoints."""
    
    def test_get_all_faqs(self, client):
        """Test retrieving all FAQs."""
        response = client.get("/faq")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert "id" in data[0]
            assert "question" in data[0]
            assert "answer" in data[0]
    
    def test_search_faqs(self, client):
        """Test searching FAQs by query."""
        response = client.get("/faq/search?query=hours")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Verify results are relevant
        for item in data:
            assert "hours" in item["question"].lower() or "hours" in item["answer"].lower()
    
    def test_get_faq_by_id(self, client):
        """Test retrieving a specific FAQ."""
        # First get all FAQs to get an ID
        all_faqs = client.get("/faq").json()
        if len(all_faqs) > 0:
            faq_id = all_faqs[0]["id"]
            
            response = client.get(f"/faq/{faq_id}")
            assert response.status_code == 200
            assert response.json()["id"] == faq_id
    
    def test_create_faq(self, client):
        """Test creating a new FAQ entry."""
        faq_data = {
            "question": "What are your operating hours?",
            "answer": "We are open Monday-Friday, 9 AM to 5 PM EST.",
            "category": "general"
        }
        
        response = client.post("/faq", json=faq_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["question"] == faq_data["question"]
        assert data["answer"] == faq_data["answer"]
        assert "id" in data


# Pytest fixtures
@pytest.fixture
def client():
    """Create a test client for the API."""
    # Replace with your actual FastAPI app import
    # from app.main import app
    # return TestClient(app)
    
    # Placeholder - replace with actual implementation
    import requests
    class MockClient:
        def __init__(self):
            self.base_url = BASE_URL
        
        def post(self, endpoint, json=None):
            # Mock implementation - replace with TestClient
            return type('Response', (), {'status_code': 201, 'json': lambda: json})()
        
        def get(self, endpoint):
            return type('Response', (), {'status_code': 200, 'json': lambda: []})()
        
        def patch(self, endpoint, json=None):
            return type('Response', (), {'status_code': 200, 'json': lambda: json})()
        
        def delete(self, endpoint):
            return type('Response', (), {'status_code': 204})()
    
    return MockClient()
