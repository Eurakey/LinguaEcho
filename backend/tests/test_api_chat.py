"""
Tests for /api/chat endpoint.
"""

import pytest
from unittest.mock import patch, AsyncMock


class TestChatEndpoint:
    """Test cases for /api/chat endpoint."""

    def test_chat_endpoint_success(self, client, sample_chat_request):
        """Test successful chat request."""
        with patch('app.services.llm_service.llm_service.get_conversation_response', new_callable=AsyncMock) as mock_chat:
            # Setup mock
            mock_chat.return_value = "こんにちは！ご注文をお伺いします。"

            # Make request
            response = client.post("/api/chat", json=sample_chat_request)

            # Assertions
            assert response.status_code == 200
            data = response.json()
            assert "reply" in data
            assert "session_id" in data
            assert data["session_id"] == sample_chat_request["session_id"]
            assert isinstance(data["reply"], str)
            assert len(data["reply"]) > 0

    def test_chat_endpoint_missing_fields(self, client):
        """Test chat request with missing required fields."""
        invalid_request = {
            "session_id": "test-123",
            "language": "japanese"
            # Missing: scenario, message, history
        }

        response = client.post("/api/chat", json=invalid_request)

        # Should return 422 Unprocessable Entity for validation error
        assert response.status_code == 422

    def test_chat_endpoint_invalid_language(self, client):
        """Test chat request with invalid language."""
        invalid_request = {
            "session_id": "test-123",
            "language": "invalid_language",
            "scenario": "restaurant",
            "message": "Hello",
            "history": []
        }

        response = client.post("/api/chat", json=invalid_request)

        # Should return 422 for invalid enum value
        assert response.status_code == 422

    def test_chat_endpoint_invalid_scenario(self, client):
        """Test chat request with invalid scenario."""
        invalid_request = {
            "session_id": "test-123",
            "language": "japanese",
            "scenario": "invalid_scenario",
            "message": "Hello",
            "history": []
        }

        response = client.post("/api/chat", json=invalid_request)

        # Should return 422 for invalid enum value
        assert response.status_code == 422

    def test_chat_endpoint_empty_message(self, client):
        """Test chat request with empty message."""
        # Empty message should still be accepted, but may trigger validation
        invalid_request = {
            "session_id": "test-123",
            "language": "japanese",
            "scenario": "restaurant",
            "message": "",
            "history": []
        }

        with patch('app.services.llm_service.llm_service.get_conversation_response', new_callable=AsyncMock) as mock_chat:
            mock_chat.return_value = "Empty message response"
            response = client.post("/api/chat", json=invalid_request)

            # May return 200 or 422 depending on validation rules
            assert response.status_code in [200, 422]

    def test_chat_endpoint_with_history(self, client):
        """Test chat request with conversation history."""
        with patch('app.services.llm_service.llm_service.get_conversation_response', new_callable=AsyncMock) as mock_chat:
            # Setup mock
            mock_chat.return_value = "かしこまりました。"

            request_with_history = {
                "session_id": "test-123",
                "language": "japanese",
                "scenario": "restaurant",
                "message": "ラーメンをください",
                "history": [
                    {"role": "user", "content": "メニューをください"},
                    {"role": "assistant", "content": "こちらがメニューです"}
                ]
            }

            response = client.post("/api/chat", json=request_with_history)

            assert response.status_code == 200
            data = response.json()
            assert "reply" in data

    def test_chat_endpoint_llm_service_error(self, client, sample_chat_request):
        """Test chat endpoint when LLM service raises an error."""
        with patch('app.services.llm_service.llm_service.get_conversation_response', new_callable=AsyncMock) as mock_chat:
            # Setup mock to raise exception
            mock_chat.side_effect = Exception("LLM service error")

            response = client.post("/api/chat", json=sample_chat_request)

            # Should return 500 for internal server error
            assert response.status_code == 500
            data = response.json()
            assert "detail" in data

    def test_chat_endpoint_all_scenarios(self, client):
        """Test chat endpoint with all valid scenarios."""
        scenarios = [
            "restaurant", "hotel", "supermarket", "transportation",
            "self_intro", "casual_chat", "phone_appointment",
            "job_interview", "business_email", "classroom"
        ]

        with patch('app.services.llm_service.llm_service.get_conversation_response', new_callable=AsyncMock) as mock_chat:
            mock_chat.return_value = "Test response"

            for scenario in scenarios:
                request = {
                    "session_id": f"test-{scenario}",
                    "language": "japanese",
                    "scenario": scenario,
                    "message": "テストメッセージ",
                    "history": []
                }

                response = client.post("/api/chat", json=request)
                assert response.status_code == 200, f"Failed for scenario: {scenario}"

    def test_chat_endpoint_both_languages(self, client):
        """Test chat endpoint with both supported languages."""
        languages = ["japanese", "english"]

        with patch('app.services.llm_service.llm_service.get_conversation_response', new_callable=AsyncMock) as mock_chat:
            mock_chat.return_value = "Test response"

            for language in languages:
                request = {
                    "session_id": f"test-{language}",
                    "language": language,
                    "scenario": "restaurant",
                    "message": "Test message",
                    "history": []
                }

                response = client.post("/api/chat", json=request)
                assert response.status_code == 200, f"Failed for language: {language}"
