"""
API endpoints for chat and report generation
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse, ReportRequest, ReportResponse
from app.services.llm_service import llm_service

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Handle conversation turn

    Args:
        request: ChatRequest with session_id, language, scenario, message, and history

    Returns:
        ChatResponse with AI reply and session_id
    """
    try:
        # Get AI response
        reply = await llm_service.get_conversation_response(
            language=request.language,
            scenario=request.scenario,
            user_message=request.message,
            history=request.history
        )

        return ChatResponse(
            reply=reply,
            session_id=request.session_id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")


@router.post("/report/generate", response_model=ReportResponse)
async def generate_report(request: ReportRequest):
    """
    Generate detailed feedback report for conversation

    Args:
        request: ReportRequest with session_id, language, scenario, and full conversation

    Returns:
        ReportResponse with detailed analysis report
    """
    try:
        # Generate report
        report = await llm_service.generate_report(
            language=request.language,
            scenario=request.scenario,
            conversation=request.conversation
        )

        return ReportResponse(report=report)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")
