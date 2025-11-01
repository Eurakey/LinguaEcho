"""
API endpoints for chat and report generation
"""
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
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


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Handle conversation turn with streaming response (Server-Sent Events)

    Args:
        request: ChatRequest with session_id, language, scenario, message, and history

    Returns:
        StreamingResponse with SSE format containing AI response chunks
    """
    async def generate():
        """Generator function for SSE streaming"""
        try:
            full_response = []

            # Stream response from LLM
            async for chunk in llm_service.get_conversation_response_stream(
                language=request.language,
                scenario=request.scenario,
                user_message=request.message,
                history=request.history
            ):
                full_response.append(chunk)

                # Send SSE formatted data
                # Format: data: {JSON}\n\n
                sse_data = json.dumps({
                    "type": "chunk",
                    "content": chunk,
                    "session_id": request.session_id
                }, ensure_ascii=False)
                yield f"data: {sse_data}\n\n"

            # Send completion event with full response
            complete_data = json.dumps({
                "type": "done",
                "content": "".join(full_response),
                "session_id": request.session_id
            }, ensure_ascii=False)
            yield f"data: {complete_data}\n\n"

        except Exception as e:
            # Send error event
            error_data = json.dumps({
                "type": "error",
                "error": str(e),
                "session_id": request.session_id
            }, ensure_ascii=False)
            yield f"data: {error_data}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering for proxies
        }
    )


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
