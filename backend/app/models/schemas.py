"""
Pydantic models for API requests and responses
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from enum import Enum


class Language(str, Enum):
    """Supported languages"""
    JAPANESE = "japanese"
    ENGLISH = "english"


class Scenario(str, Enum):
    """Available conversation scenarios"""
    # Daily Life
    RESTAURANT = "restaurant"
    HOTEL = "hotel"
    SUPERMARKET = "supermarket"
    TRANSPORTATION = "transportation"

    # Social
    SELF_INTRO = "self_intro"
    CASUAL_CHAT = "casual_chat"
    PHONE_APPOINTMENT = "phone_appointment"

    # Professional/Academic
    JOB_INTERVIEW = "job_interview"
    BUSINESS_EMAIL = "business_email"
    CLASSROOM = "classroom"


class Message(BaseModel):
    """Individual message in conversation"""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Request model for /api/chat endpoint"""
    session_id: str = Field(..., description="Unique session identifier")
    language: Language = Field(..., description="Target language")
    scenario: Scenario = Field(..., description="Conversation scenario")
    message: str = Field(..., description="User's message")
    history: List[Message] = Field(default=[], description="Conversation history")


class ChatResponse(BaseModel):
    """Response model for /api/chat endpoint"""
    reply: str = Field(..., description="AI's response")
    session_id: str = Field(..., description="Session identifier")


class ConversationOverview(BaseModel):
    """Overview section of the report"""
    language: str
    scenario: str
    turns: int
    word_count: int


class ErrorAnalysis(BaseModel):
    """Individual error analysis item"""
    error: str = Field(..., description="The error found")
    correction: str = Field(..., description="Corrected version")
    explanation: str = Field(..., description="Explanation of the error")
    error_type: Optional[str] = Field(None, description="Type/category of error")


class VocabularyIssue(BaseModel):
    """Vocabulary issue item"""
    original: str = Field(..., description="Original word/phrase used")
    suggestion: str = Field(..., description="Better alternative")
    explanation: str = Field(..., description="Why the suggestion is better")


class NaturalnessIssue(BaseModel):
    """Naturalness/expression issue item"""
    unnatural: str = Field(..., description="Unnatural expression")
    natural: str = Field(..., description="More natural alternative")
    context: str = Field(..., description="Context or explanation")


class Report(BaseModel):
    """Complete conversation report"""
    overview: ConversationOverview
    grammar_errors: List[ErrorAnalysis]
    vocabulary_issues: List[VocabularyIssue]
    naturalness: List[NaturalnessIssue]
    positive_feedback: List[str]


class ReportRequest(BaseModel):
    """Request model for /api/report/generate endpoint"""
    session_id: str = Field(..., description="Unique session identifier")
    language: Language = Field(..., description="Target language")
    scenario: Scenario = Field(..., description="Conversation scenario")
    conversation: List[Message] = Field(..., description="Full conversation history")


class ReportResponse(BaseModel):
    """Response model for /api/report/generate endpoint"""
    report: Report
