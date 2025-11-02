"""
CRUD operations for Conversation and Report models
"""
from typing import List, Optional
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from uuid import UUID
from datetime import datetime

from ..db.models import Conversation, Report


async def create_conversation(
    db: AsyncSession,
    session_id: UUID,
    user_id: Optional[UUID],
    language: str,
    scenario: str,
    messages: list
) -> Conversation:
    """
    Create a new conversation
    """
    conversation = Conversation(
        session_id=session_id,
        user_id=user_id,
        language=language,
        scenario=scenario,
        messages=messages
    )

    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)

    return conversation


async def get_conversation_by_session_id(
    db: AsyncSession,
    session_id: UUID
) -> Optional[Conversation]:
    """
    Get conversation by session ID
    """
    result = await db.execute(
        select(Conversation)
        .where(Conversation.session_id == session_id)
        .options(selectinload(Conversation.report))
    )
    return result.scalar_one_or_none()


async def get_user_conversations(
    db: AsyncSession,
    user_id: UUID,
    limit: int = 50
) -> List[Conversation]:
    """
    Get all conversations for a user, ordered by most recent first
    """
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(desc(Conversation.created_at))
        .limit(limit)
        .options(selectinload(Conversation.report))
    )
    return list(result.scalars().all())


async def update_conversation_messages(
    db: AsyncSession,
    conversation: Conversation,
    messages: list
) -> Conversation:
    """
    Update conversation messages
    """
    conversation.messages = messages
    await db.commit()
    await db.refresh(conversation)

    return conversation


async def delete_conversation(db: AsyncSession, conversation_id: UUID) -> bool:
    """
    Delete a conversation (and its associated report via cascade)
    """
    result = await db.execute(
        select(Conversation).where(Conversation.id == conversation_id)
    )
    conversation = result.scalar_one_or_none()

    if not conversation:
        return False

    await db.delete(conversation)
    await db.commit()

    return True


async def create_report(
    db: AsyncSession,
    conversation_id: UUID,
    report_data: dict
) -> Report:
    """
    Create a report for a conversation
    """
    report = Report(
        conversation_id=conversation_id,
        report_data=report_data
    )

    db.add(report)
    await db.commit()
    await db.refresh(report)

    return report


async def get_report_by_conversation_id(
    db: AsyncSession,
    conversation_id: UUID
) -> Optional[Report]:
    """
    Get report by conversation ID
    """
    result = await db.execute(
        select(Report).where(Report.conversation_id == conversation_id)
    )
    return result.scalar_one_or_none()
