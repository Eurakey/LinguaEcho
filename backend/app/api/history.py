"""
Conversation history and data migration API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID, uuid4

from ..db.database import get_db
from ..models.schemas import (
    ConversationListItem,
    ConversationDetail,
    MigrateDataRequest,
    Message,
    Report as ReportSchema
)
from ..crud.conversation import (
    get_user_conversations,
    get_conversation_by_session_id,
    delete_conversation,
    create_conversation,
    create_report
)
from ..dependencies.auth import require_current_user
from ..db.models import User

router = APIRouter(tags=["Conversations"])


@router.post("/migrate", status_code=status.HTTP_200_OK)
async def migrate_local_storage_data(
    data: MigrateDataRequest,
    current_user: User = Depends(require_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Migrate localStorage conversations to database for authenticated user

    - **conversations**: List of conversation objects from localStorage

    This endpoint is called automatically on first login to migrate existing data
    """
    migrated_count = 0

    for conv_data in data.conversations:
        try:
            session_id = UUID(conv_data.get("session_id", str(uuid4())))

            # Check if conversation already exists
            existing = await get_conversation_by_session_id(db, session_id)
            if existing:
                continue  # Skip duplicates

            # Create conversation
            conversation = await create_conversation(
                db=db,
                session_id=session_id,
                user_id=current_user.id,
                language=conv_data.get("language", "english"),
                scenario=conv_data.get("scenario", "casual_chat"),
                messages=conv_data.get("messages", [])
            )

            # If there's a report, create it
            if "report" in conv_data and conv_data["report"]:
                await create_report(
                    db=db,
                    conversation_id=conversation.id,
                    report_data=conv_data["report"]
                )

            migrated_count += 1

        except Exception as e:
            # Log error but continue with other conversations
            print(f"Error migrating conversation: {e}")
            continue

    return {
        "message": f"Successfully migrated {migrated_count} conversations",
        "migrated_count": migrated_count
    }


@router.get("/conversations", response_model=List[ConversationDetail])
async def get_conversations(
    current_user: User = Depends(require_current_user),
    db: AsyncSession = Depends(get_db),
    limit: int = 50
):
    """
    Get all conversations for the authenticated user

    - **limit**: Maximum number of conversations to return (default 50)

    Returns full conversation details including messages and reports
    """
    conversations = await get_user_conversations(db, current_user.id, limit)

    # Transform to response model with full details
    result = []
    for conv in conversations:
        # Parse messages from JSONB
        messages = [Message(**msg) for msg in conv.messages] if conv.messages else []

        # Parse report from relationship
        report = None
        if conv.report:
            report_data = conv.report.report_data
            report = ReportSchema(
                overview=report_data.get('overview', {}),
                grammar_errors=report_data.get('grammar_errors', []),
                vocabulary_issues=report_data.get('vocabulary_issues', []),
                naturalness=report_data.get('naturalness', []),
                positive_feedback=report_data.get('positive_feedback', [])
            )

        result.append(ConversationDetail(
            id=conv.id,
            session_id=conv.session_id,
            language=conv.language,
            scenario=conv.scenario,
            messages=messages,
            created_at=conv.created_at,
            report=report
        ))

    return result


@router.get("/conversations/{session_id}", response_model=ConversationDetail)
async def get_conversation(
    session_id: UUID,
    current_user: User = Depends(require_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get detailed conversation by session ID

    Returns conversation with all messages and report (if exists)
    """
    conversation = await get_conversation_by_session_id(db, session_id)

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    # Verify ownership
    if conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this conversation"
        )

    # Convert messages to Message objects
    messages = [Message(**msg) for msg in conversation.messages]

    # Build response
    return ConversationDetail(
        id=conversation.id,
        session_id=conversation.session_id,
        language=conversation.language,
        scenario=conversation.scenario,
        messages=messages,
        created_at=conversation.created_at,
        report=conversation.report.report_data if conversation.report else None
    )


@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation_endpoint(
    conversation_id: UUID,
    current_user: User = Depends(require_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a conversation (and its report)

    Only the owner can delete their conversation
    """
    # Get conversation to verify ownership
    from sqlalchemy import select
    from ..db.models import Conversation

    result = await db.execute(
        select(Conversation).where(Conversation.id == conversation_id)
    )
    conversation = result.scalar_one_or_none()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    if conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this conversation"
        )

    # Delete conversation
    success = await delete_conversation(db, conversation_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete conversation"
        )

    return None
