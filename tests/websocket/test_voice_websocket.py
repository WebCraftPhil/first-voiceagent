"""
WebSocket tests for voice agent real-time communication.
Tests bidirectional voice communication over WebSocket.
"""
import pytest
import asyncio
import json
from websockets.client import connect
from websockets.server import serve


class TestVoiceWebSocket:
    """Test voice agent WebSocket functionality."""
    
    @pytest.mark.asyncio
    async def test_websocket_connection(self):
        """Test establishing WebSocket connection."""
        async with connect("ws://localhost:8000/ws/voice") as websocket:
            # Connection should be established
            assert websocket.open
    
    @pytest.mark.asyncio
    async def test_send_audio_chunk(self):
        """Test sending audio data chunk to server."""
        async with connect("ws://localhost:8000/ws/voice") as websocket:
            # Send audio chunk
            audio_data = {
                "type": "audio_chunk",
                "data": "base64_encoded_audio_data",
                "format": "webm",
                "session_id": "test-session-123"
            }
            await websocket.send(json.dumps(audio_data))
            
            # Should receive acknowledgment
            response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            data = json.loads(response)
            assert data["type"] == "ack" or data["type"] == "transcription"
    
    @pytest.mark.asyncio
    async def test_receive_transcription(self):
        """Test receiving transcription from server."""
        async with connect("ws://localhost:8000/ws/voice") as websocket:
            # Send audio
            audio_data = {
                "type": "audio_chunk",
                "data": "base64_encoded_audio_data",
                "session_id": "test-session-123"
            }
            await websocket.send(json.dumps(audio_data))
            
            # Receive transcription
            response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
            data = json.loads(response)
            
            assert data["type"] == "transcription"
            assert "text" in data
            assert isinstance(data["text"], str)
    
    @pytest.mark.asyncio
    async def test_receive_voice_response(self):
        """Test receiving voice response from server."""
        async with connect("ws://localhost:8000/ws/voice") as websocket:
            # Send question
            question = {
                "type": "question",
                "text": "What are your hours?",
                "session_id": "test-session-123"
            }
            await websocket.send(json.dumps(question))
            
            # Receive response
            response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
            data = json.loads(response)
            
            assert data["type"] == "response"
            assert "text" in data or "audio_url" in data
    
    @pytest.mark.asyncio
    async def test_session_management(self):
        """Test WebSocket session creation and management."""
        async with connect("ws://localhost:8000/ws/voice") as websocket:
            # Create session
            session_request = {
                "type": "create_session",
                "user_id": "test-user-123"
            }
            await websocket.send(json.dumps(session_request))
            
            # Receive session info
            response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            data = json.loads(response)
            
            assert data["type"] == "session_created"
            assert "session_id" in data
    
    @pytest.mark.asyncio
    async def test_multiple_audio_chunks(self):
        """Test sending multiple audio chunks in sequence."""
        async with connect("ws://localhost:8000/ws/voice") as websocket:
            session_id = "test-session-123"
            
            # Send multiple chunks
            for i in range(3):
                chunk = {
                    "type": "audio_chunk",
                    "data": f"chunk_{i}_data",
                    "chunk_index": i,
                    "session_id": session_id
                }
                await websocket.send(json.dumps(chunk))
                await asyncio.sleep(0.1)  # Small delay between chunks
            
            # Should receive final transcription
            response = await asyncio.wait_for(websocket.recv(), timeout=15.0)
            data = json.loads(response)
            assert data["type"] == "transcription" or data["type"] == "final_transcription"
    
    @pytest.mark.asyncio
    async def test_error_handling_invalid_message(self):
        """Test server handles invalid messages gracefully."""
        async with connect("ws://localhost:8000/ws/voice") as websocket:
            # Send invalid message
            await websocket.send("invalid json")
            
            # Should receive error response
            response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            data = json.loads(response)
            assert data["type"] == "error"
            assert "message" in data
    
    @pytest.mark.asyncio
    async def test_connection_timeout(self):
        """Test connection timeout handling."""
        # Try to connect to non-existent server
        with pytest.raises(Exception):  # ConnectionError or similar
            async with connect("ws://localhost:9999/ws/voice", timeout=2) as websocket:
                pass
    
    @pytest.mark.asyncio
    async def test_heartbeat_mechanism(self):
        """Test WebSocket heartbeat/ping-pong mechanism."""
        async with connect("ws://localhost:8000/ws/voice") as websocket:
            # Send ping
            ping = {"type": "ping"}
            await websocket.send(json.dumps(ping))
            
            # Should receive pong
            response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            data = json.loads(response)
            assert data["type"] == "pong"


# Helper function for testing WebSocket server
@pytest.fixture
async def mock_websocket_server():
    """Create a mock WebSocket server for testing."""
    async def handler(websocket, path):
        async for message in websocket:
            data = json.loads(message)
            
            if data.get("type") == "ping":
                await websocket.send(json.dumps({"type": "pong"}))
            elif data.get("type") == "audio_chunk":
                await websocket.send(json.dumps({
                    "type": "transcription",
                    "text": "test transcription"
                }))
            elif data.get("type") == "question":
                await websocket.send(json.dumps({
                    "type": "response",
                    "text": "Our hours are 9-5 EST"
                }))
    
    server = await serve(handler, "localhost", 8765)
    yield server
    server.close()
    await server.wait_closed()
