"""
Pytest configuration and fixtures for backend testing.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app


@pytest.fixture
def client():
    """
    Create a test client for FastAPI app.
    """
    return TestClient(app)


@pytest.fixture
def mock_llm_response():
    """
    Mock LLM response for testing without calling actual API.
    """
    return {
        "reply": "こんにちは！ご注文をお伺いします。",
        "session_id": "test-session-123"
    }


@pytest.fixture
def mock_report_response():
    """
    Mock report generation response.
    """
    return {
        "report": {
            "overview": {
                "language": "japanese",
                "scenario": "restaurant",
                "turns": 5,
                "word_count": 50
            },
            "grammar_errors": [
                {
                    "error": "を particle incorrect",
                    "correction": "レストランに行きたいです",
                    "explanation": "Use に for destinations, not を",
                    "error_type": "particle"
                }
            ],
            "vocabulary_issues": [],
            "naturalness": [],
            "positive_feedback": [
                "Good use of polite form",
                "Clear pronunciation"
            ]
        }
    }


@pytest.fixture
def sample_chat_request():
    """
    Sample chat request data.
    """
    return {
        "session_id": "test-session-123",
        "language": "japanese",
        "scenario": "restaurant",
        "message": "すみません、メニューをください",
        "history": []
    }


@pytest.fixture
def sample_report_request():
    """
    Sample report generation request data.
    """
    return {
        "session_id": "test-session-123",
        "language": "japanese",
        "scenario": "restaurant",
        "conversation": [
            {"role": "user", "content": "すみません、メニューをください"},
            {"role": "assistant", "content": "かしこまりました。こちらがメニューでございます。"},
            {"role": "user", "content": "ラーメンをください"},
            {"role": "assistant", "content": "ラーメンですね。かしこまりました。"}
        ]
    }


@pytest.fixture
def mock_llm_service():
    """
    Mock LLM service to avoid actual API calls.
    """
    with patch('app.services.llm_service.LLMService') as mock_service:
        # Configure mock
        mock_instance = Mock()
        mock_service.get_instance.return_value = mock_instance

        # Mock chat method
        async def mock_chat(language, scenario, message, history):
            return "Mock AI response for testing"

        mock_instance.chat = mock_chat

        # Mock generate_report method
        async def mock_generate_report(language, scenario, conversation):
            return {
                "overview": {"language": language, "scenario": scenario, "turns": len(conversation), "word_count": 100},
                "grammar_errors": [],
                "vocabulary_issues": [],
                "naturalness": [],
                "positive_feedback": ["Great conversation!"]
            }

        mock_instance.generate_report = mock_generate_report

        yield mock_service
