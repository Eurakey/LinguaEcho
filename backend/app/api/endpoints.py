"""
API endpoints for chat and report generation
"""
import json
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID

from app.models.schemas import ChatRequest, ChatResponse, ReportRequest, ReportResponse
from app.services.llm_service import llm_service
from ..db.database import get_db
from ..db.models import User
from ..dependencies.auth import get_current_user
from ..crud.conversation import (
    create_conversation,
    get_conversation_by_session_id,
    update_conversation_messages,
    create_report
)

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: Optional[User] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Handle conversation turn

    Works for both guests (no auth) and authenticated users.
    If authenticated, conversation is saved to database.

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

        # If user is authenticated, save to database
        if current_user:
            session_id = UUID(request.session_id)

            # Check if conversation exists
            existing_conv = await get_conversation_by_session_id(db, session_id)

            # Build updated messages
            updated_messages = [msg.model_dump() for msg in request.history]
            updated_messages.append({"role": "user", "content": request.message})
            updated_messages.append({"role": "assistant", "content": reply})

            if existing_conv:
                # Update existing conversation
                await update_conversation_messages(db, existing_conv, updated_messages)
            else:
                # Create new conversation
                await create_conversation(
                    db=db,
                    session_id=session_id,
                    user_id=current_user.id,
                    language=request.language.value,
                    scenario=request.scenario.value,
                    messages=updated_messages
                )

        return ChatResponse(
            reply=reply,
            session_id=request.session_id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")


@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    current_user: Optional[User] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Handle conversation turn with streaming response (Server-Sent Events)

    Works for both guests (no auth) and authenticated users.
    If authenticated, conversation is saved to database after streaming completes.

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

            complete_response = "".join(full_response)

            # If user is authenticated, save to database
            if current_user:
                try:
                    session_id = UUID(request.session_id)

                    # Check if conversation exists
                    existing_conv = await get_conversation_by_session_id(db, session_id)

                    # Build updated messages
                    updated_messages = [msg.model_dump() for msg in request.history]
                    updated_messages.append({"role": "user", "content": request.message})
                    updated_messages.append({"role": "assistant", "content": complete_response})

                    if existing_conv:
                        # Update existing conversation
                        await update_conversation_messages(db, existing_conv, updated_messages)
                    else:
                        # Create new conversation
                        await create_conversation(
                            db=db,
                            session_id=session_id,
                            user_id=current_user.id,
                            language=request.language.value,
                            scenario=request.scenario.value,
                            messages=updated_messages
                        )
                except Exception as db_error:
                    # Log database error but don't fail the stream
                    print(f"Database save error: {db_error}")

            # Send completion event with full response
            complete_data = json.dumps({
                "type": "done",
                "content": complete_response,
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
async def generate_report(
    request: ReportRequest,
    current_user: Optional[User] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate detailed feedback report for conversation

    Works for both guests (no auth) and authenticated users.
    If authenticated, report is saved to database.

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

        # If user is authenticated, save report to database
        if current_user:
            try:
                session_id = UUID(request.session_id)
                conversation = await get_conversation_by_session_id(db, session_id)

                if conversation and conversation.user_id == current_user.id:
                    # Save or update report
                    await create_report(
                        db=db,
                        conversation_id=conversation.id,
                        report_data=report.model_dump()
                    )
            except Exception as db_error:
                # Log database error but don't fail the report generation
                print(f"Database save error: {db_error}")

        return ReportResponse(report=report)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")
