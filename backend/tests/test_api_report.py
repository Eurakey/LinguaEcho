"""
Tests for /api/report/generate endpoint.
"""

import pytest
from unittest.mock import patch, AsyncMock


class TestReportEndpoint:
    """Test cases for /api/report/generate endpoint."""

    def test_report_endpoint_success(self, client, sample_report_request):
        """Test successful report generation."""
        with patch('app.services.llm_service.llm_service.generate_report', new_callable=AsyncMock) as mock_report:
            # Setup mock
            mock_report.return_value = {
                "overview": {
                    "language": "japanese",
                    "scenario": "restaurant",
                    "turns": 2,
                    "word_count": 50
                },
                "grammar_errors": [],
                "vocabulary_issues": [],
                "naturalness": [],
                "positive_feedback": ["Great conversation!"]
            }

            response = client.post("/api/report/generate", json=sample_report_request)

            # Assertions
            assert response.status_code == 200
            data = response.json()
            assert "report" in data
            assert "overview" in data["report"]
            assert data["report"]["overview"]["language"] == "japanese"

    def test_report_endpoint_missing_fields(self, client):
        """Test report request with missing required fields."""
        invalid_request = {
            "session_id": "test-123",
            "language": "japanese"
            # Missing: scenario, conversation
        }

        response = client.post("/api/report/generate", json=invalid_request)

        # Should return 422 for validation error
        assert response.status_code == 422

    def test_report_endpoint_empty_conversation(self, client):
        """Test report request with empty conversation."""
        with patch('app.services.llm_service.llm_service.generate_report', new_callable=AsyncMock) as mock_report:
            mock_report.return_value = {
                "overview": {"language": "japanese", "scenario": "restaurant", "turns": 0, "word_count": 0},
                "grammar_errors": [],
                "vocabulary_issues": [],
                "naturalness": [],
                "positive_feedback": []
            }

            invalid_request = {
                "session_id": "test-123",
                "language": "japanese",
                "scenario": "restaurant",
                "conversation": []
            }

            response = client.post("/api/report/generate", json=invalid_request)

            # May accept empty conversation or return validation error
            assert response.status_code in [200, 422]

    def test_report_endpoint_with_grammar_errors(self, client, sample_report_request):
        """Test report generation with grammar errors in response."""
        with patch('app.services.llm_service.llm_service.generate_report', new_callable=AsyncMock) as mock_report:
            mock_report.return_value = {
                "overview": {
                    "language": "japanese",
                    "scenario": "restaurant",
                    "turns": 2,
                    "word_count": 50
                },
                "grammar_errors": [
                    {
                        "error": "Incorrect particle usage",
                        "correction": "レストランに",
                        "explanation": "Use に for destinations",
                        "error_type": "particle"
                    }
                ],
                "vocabulary_issues": [],
                "naturalness": [],
                "positive_feedback": ["Good attempt!"]
            }

            response = client.post("/api/report/generate", json=sample_report_request)

            assert response.status_code == 200
            data = response.json()
            assert len(data["report"]["grammar_errors"]) > 0
            assert data["report"]["grammar_errors"][0]["error_type"] == "particle"

    def test_report_endpoint_with_vocabulary_issues(self, client, sample_report_request):
        """Test report generation with vocabulary suggestions."""
        with patch('app.services.llm_service.llm_service.generate_report', new_callable=AsyncMock) as mock_report:
            mock_report.return_value = {
                "overview": {
                    "language": "japanese",
                    "scenario": "restaurant",
                    "turns": 2,
                    "word_count": 50
                },
                "grammar_errors": [],
                "vocabulary_issues": [
                    {
                        "original": "食べ物",
                        "suggestion": "料理",
                        "explanation": "料理 is more appropriate in restaurant context"
                    }
                ],
                "naturalness": [],
                "positive_feedback": ["Good vocabulary overall!"]
            }

            response = client.post("/api/report/generate", json=sample_report_request)

            assert response.status_code == 200
            data = response.json()
            assert len(data["report"]["vocabulary_issues"]) > 0

    def test_report_endpoint_with_naturalness_feedback(self, client, sample_report_request):
        """Test report generation with naturalness suggestions."""
        with patch('app.services.llm_service.llm_service.generate_report', new_callable=AsyncMock) as mock_report:
            mock_report.return_value = {
                "overview": {
                    "language": "japanese",
                    "scenario": "restaurant",
                    "turns": 2,
                    "word_count": 50
                },
                "grammar_errors": [],
                "vocabulary_issues": [],
                "naturalness": [
                    {
                        "unnatural": "メニューを見せてください",
                        "natural": "メニューをいただけますか",
                        "context": "More polite and natural in restaurants"
                    }
                ],
                "positive_feedback": ["Great politeness!"]
            }

            response = client.post("/api/report/generate", json=sample_report_request)

            assert response.status_code == 200
            data = response.json()
            assert len(data["report"]["naturalness"]) > 0

    def test_report_endpoint_perfect_conversation(self, client, sample_report_request):
        """Test report generation for a perfect conversation (no errors)."""
        with patch('app.services.llm_service.llm_service.generate_report', new_callable=AsyncMock) as mock_report:
            mock_report.return_value = {
                "overview": {
                    "language": "japanese",
                    "scenario": "restaurant",
                    "turns": 2,
                    "word_count": 50
                },
                "grammar_errors": [],
                "vocabulary_issues": [],
                "naturalness": [],
                "positive_feedback": [
                    "Perfect grammar!",
                    "Natural expressions!",
                    "Excellent politeness level!"
                ]
            }

            response = client.post("/api/report/generate", json=sample_report_request)

            assert response.status_code == 200
            data = response.json()
            assert len(data["report"]["grammar_errors"]) == 0
            assert len(data["report"]["vocabulary_issues"]) == 0
            assert len(data["report"]["naturalness"]) == 0
            assert len(data["report"]["positive_feedback"]) > 0

    def test_report_endpoint_invalid_language(self, client):
        """Test report request with invalid language."""
        invalid_request = {
            "session_id": "test-123",
            "language": "spanish",  # Not supported
            "scenario": "restaurant",
            "conversation": [
                {"role": "user", "content": "Hola"}
            ]
        }

        response = client.post("/api/report/generate", json=invalid_request)

        # Should return 422 for invalid enum
        assert response.status_code == 422

    def test_report_endpoint_long_conversation(self, client):
        """Test report generation for a long conversation."""
        with patch('app.services.llm_service.llm_service.generate_report', new_callable=AsyncMock) as mock_report:
            mock_report.return_value = {
                "overview": {
                    "language": "japanese",
                    "scenario": "restaurant",
                    "turns": 10,
                    "word_count": 200
                },
                "grammar_errors": [],
                "vocabulary_issues": [],
                "naturalness": [],
                "positive_feedback": ["Sustained great conversation!"]
            }

            # Create long conversation
            conversation = []
            for i in range(20):  # 10 turns = 20 messages
                conversation.append({"role": "user", "content": f"Message {i}"})
                conversation.append({"role": "assistant", "content": f"Response {i}"})

            request = {
                "session_id": "test-123",
                "language": "japanese",
                "scenario": "restaurant",
                "conversation": conversation
            }

            response = client.post("/api/report/generate", json=request)

            assert response.status_code == 200
            data = response.json()
            assert data["report"]["overview"]["turns"] == 10

    def test_report_endpoint_llm_service_error(self, client, sample_report_request):
        """Test report endpoint when LLM service raises an error."""
        with patch('app.services.llm_service.llm_service.generate_report', new_callable=AsyncMock) as mock_report:
            mock_report.side_effect = Exception("LLM error")

            response = client.post("/api/report/generate", json=sample_report_request)

            # Should return 500 for internal server error
            assert response.status_code == 500
            data = response.json()
            assert "detail" in data
