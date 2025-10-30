"""
LangChain service for LLM interactions
Handles OpenRouter, Groq, and Google AI Studio providers
"""
import json
from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from app.config import settings
from app.models.schemas import Language, Scenario, Message, Report
from app.langchain.prompts import get_conversation_system_prompt, get_report_generation_prompt


class LLMService:
    """Service for interacting with LLM via LangChain"""

    def __init__(self):
        """Initialize LLM client based on configured provider"""
        if settings.LLM_PROVIDER == "groq":
            self.llm = ChatGroq(
                groq_api_key=settings.GROQ_API_KEY,
                model_name=settings.GROQ_MODEL,
                temperature=0.7
            )
        elif settings.LLM_PROVIDER == "google":
            self.llm = ChatGoogleGenerativeAI(
                model=settings.GOOGLE_MODEL,
                google_api_key=settings.GOOGLE_API_KEY,
                temperature=0.7
            )
        else:  # openrouter
            self.llm = ChatOpenAI(
                openai_api_key=settings.OPENROUTER_API_KEY,
                openai_api_base="https://openrouter.ai/api/v1",
                model_name=settings.OPENROUTER_MODEL,
                temperature=0.7
            )

    def _convert_messages(self, history: List[Message]) -> List:
        """Convert Message objects to LangChain message format"""
        lc_messages = []
        for msg in history:
            if msg.role == "user":
                lc_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                lc_messages.append(AIMessage(content=msg.content))
        return lc_messages

    async def get_conversation_response(
        self,
        language: Language,
        scenario: Scenario,
        user_message: str,
        history: List[Message]
    ) -> str:
        """
        Get AI response for conversation

        Args:
            language: Target language
            scenario: Conversation scenario
            user_message: User's latest message
            history: Previous conversation history

        Returns:
            AI's response string
        """
        # Build messages
        system_prompt = get_conversation_system_prompt(language, scenario)
        messages = [SystemMessage(content=system_prompt)]

        # Add conversation history
        messages.extend(self._convert_messages(history))

        # Add current user message
        messages.append(HumanMessage(content=user_message))

        # Get response from LLM
        response = await self.llm.ainvoke(messages)

        return response.content

    async def generate_report(
        self,
        language: Language,
        scenario: Scenario,
        conversation: List[Message]
    ) -> Report:
        """
        Generate detailed feedback report for conversation

        Args:
            language: Target language
            scenario: Conversation scenario
            conversation: Full conversation history

        Returns:
            Report object with analysis
        """
        # Format conversation for analysis
        conversation_text = "\n".join([
            f"{'User' if msg.role == 'user' else 'AI'}: {msg.content}"
            for msg in conversation
        ])

        # Get analysis prompt
        analysis_prompt = get_report_generation_prompt(language, scenario, conversation_text)

        # Get report from LLM
        messages = [HumanMessage(content=analysis_prompt)]
        response = await self.llm.ainvoke(messages)

        # Parse JSON response
        try:
            # Clean the response to extract JSON
            content = response.content.strip()

            # Remove markdown code blocks if present
            if content.startswith("```json"):
                content = content[7:]  # Remove ```json
            if content.startswith("```"):
                content = content[3:]  # Remove ```
            if content.endswith("```"):
                content = content[:-3]  # Remove trailing ```

            content = content.strip()

            # Parse JSON
            report_data = json.loads(content)

            # Create Report object
            report = Report(**report_data)
            return report

        except json.JSONDecodeError as e:
            # If JSON parsing fails, return a basic report
            print(f"JSON parsing error: {e}")
            print(f"Response content: {response.content}")

            # Create a fallback report
            return Report(
                overview={
                    "language": language.value,
                    "scenario": scenario.value,
                    "turns": len([m for m in conversation if m.role == "user"]),
                    "word_count": sum(len(m.content.split()) for m in conversation if m.role == "user")
                },
                grammar_errors=[],
                vocabulary_issues=[],
                naturalness=[],
                positive_feedback=["レポートの生成中にエラーが発生しました。後ほど再試行してください。" if language == Language.JAPANESE else "An error occurred while generating the report. Please try again later."]
            )


# Singleton instance
llm_service = LLMService()
