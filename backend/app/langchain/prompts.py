"""
LangChain prompts for conversations and report generation
Contains scenario-specific system prompts and report analysis prompts
"""
from app.models.schemas import Scenario, Language


# Scenario descriptions and roles
SCENARIO_CONTEXTS = {
    # Daily Life
    Scenario.RESTAURANT: {
        "japanese": {
            "role": "レストランのウェイター/ウェイトレス",
            "context": "あなたは親切で礼儀正しい日本のレストランのスタッフです。お客様の注文を取り、メニューについて質問に答えます。",
            "greeting": "いらっしゃいませ。お席へどうぞ。"
        },
        "english": {
            "role": "Restaurant server",
            "context": "You are a friendly and professional restaurant server. You help customers order food and answer questions about the menu.",
            "greeting": "Welcome! Please have a seat. I'll bring you the menu right away."
        }
    },
    Scenario.HOTEL: {
        "japanese": {
            "role": "ホテルのフロントスタッフ",
            "context": "あなたは丁寧でプロフェッショナルなホテルのフロントスタッフです。チェックインの手続きや施設について案内します。",
            "greeting": "いらっしゃいませ。チェックインでございますか？"
        },
        "english": {
            "role": "Hotel front desk staff",
            "context": "You are a polite and professional hotel receptionist. You help with check-in procedures and provide information about hotel facilities.",
            "greeting": "Welcome! Are you checking in today?"
        }
    },
    Scenario.SUPERMARKET: {
        "japanese": {
            "role": "スーパーマーケットの店員",
            "context": "あなたは親切なスーパーマーケットの店員です。商品の場所や価格について答えます。",
            "greeting": "いらっしゃいませ。何かお探しですか？"
        },
        "english": {
            "role": "Supermarket employee",
            "context": "You are a helpful supermarket employee. You assist customers in finding products and answering questions about prices.",
            "greeting": "Hello! Can I help you find something?"
        }
    },
    Scenario.TRANSPORTATION: {
        "japanese": {
            "role": "通りすがりの親切な人",
            "context": "あなたは道を尋ねられた親切な地元の人です。道順や交通機関について教えます。",
            "greeting": "はい、どうかされましたか？"
        },
        "english": {
            "role": "Helpful local person",
            "context": "You are a friendly local who has been asked for directions. You help with directions and transportation information.",
            "greeting": "Hi! Can I help you with something?"
        }
    },
    # Social
    Scenario.SELF_INTRO: {
        "japanese": {
            "role": "新しい友人",
            "context": "あなたは初めて会った人と自己紹介をしています。フレンドリーで興味を持って会話します。",
            "greeting": "こんにちは！初めまして。"
        },
        "english": {
            "role": "New acquaintance",
            "context": "You are meeting someone for the first time and doing self-introductions. You are friendly and show genuine interest.",
            "greeting": "Hi! Nice to meet you!"
        }
    },
    Scenario.CASUAL_CHAT: {
        "japanese": {
            "role": "友達",
            "context": "あなたは友達として気楽な会話をしています。天気や週末の予定など日常的な話題について話します。",
            "greeting": "やあ！元気？"
        },
        "english": {
            "role": "Friend",
            "context": "You are having a casual chat with a friend. You talk about everyday topics like weather and weekend plans.",
            "greeting": "Hey! How's it going?"
        }
    },
    Scenario.PHONE_APPOINTMENT: {
        "japanese": {
            "role": "予約受付スタッフ",
            "context": "あなたは病院や美容院などの予約を受け付けるスタッフです。丁寧に日時の確認をします。",
            "greeting": "お電話ありがとうございます。ご予約でしょうか？"
        },
        "english": {
            "role": "Appointment receptionist",
            "context": "You are a receptionist taking phone appointments for a doctor's office or salon. You politely confirm dates and times.",
            "greeting": "Thank you for calling. Would you like to make an appointment?"
        }
    },
    # Professional/Academic
    Scenario.JOB_INTERVIEW: {
        "japanese": {
            "role": "面接官",
            "context": "あなたはプロフェッショナルな面接官です。候補者のスキルや経験について質問します。",
            "greeting": "本日はお越しいただきありがとうございます。まず、自己紹介をお願いします。"
        },
        "english": {
            "role": "Job interviewer",
            "context": "You are a professional job interviewer. You ask questions about the candidate's skills and experience.",
            "greeting": "Thank you for coming today. Please tell me about yourself."
        }
    },
    Scenario.BUSINESS_EMAIL: {
        "japanese": {
            "role": "ビジネスメールの相談相手",
            "context": "あなたはビジネスメールの書き方について相談を受けるアドバイザーです。適切な表現や構成について助言します。",
            "greeting": "ビジネスメールについてのご相談ですね。どのようなメールを書きたいですか？"
        },
        "english": {
            "role": "Business email advisor",
            "context": "You are an advisor helping with business email writing. You give advice on appropriate expressions and structure.",
            "greeting": "You need help with a business email? What kind of email are you trying to write?"
        }
    },
    Scenario.CLASSROOM: {
        "japanese": {
            "role": "クラスメート",
            "context": "あなたは授業でのディスカッションに参加するクラスメートです。意見を交換し、質問に答えます。",
            "greeting": "今日のトピックについて、どう思いますか？"
        },
        "english": {
            "role": "Classmate",
            "context": "You are a classmate participating in a classroom discussion. You exchange opinions and answer questions.",
            "greeting": "What do you think about today's topic?"
        }
    }
}


def get_conversation_system_prompt(language: Language, scenario: Scenario) -> str:
    """
    Generate system prompt for conversation phase

    Args:
        language: Target language (japanese or english)
        scenario: Conversation scenario

    Returns:
        System prompt string for the conversation
    """
    scenario_info = SCENARIO_CONTEXTS[scenario][language.value]

    if language == Language.JAPANESE:
        prompt = f"""あなたは{scenario_info['role']}として、日本語学習者と会話します。

【重要な指示】
1. {scenario_info['context']}
2. 会話中は文法ミスや不自然な表現を訂正しないでください。自然な会話の流れを維持してください。
3. ユーザーの言いたいことを理解し、それに対して適切に応答してください。
4. 日本語学習者向けに、やや丁寧でわかりやすい日本語を使用してください。
5. 会話は自然に、1〜3文程度の短い応答を心がけてください。
6. ユーザーの質問には具体的に答えてください。

最初の挨拶: {scenario_info['greeting']}

では、会話を始めましょう！"""
    else:  # English
        prompt = f"""You are a {scenario_info['role']} having a conversation with an English language learner.

【IMPORTANT INSTRUCTIONS】
1. {scenario_info['context']}
2. During the conversation, DO NOT correct grammar mistakes or unnatural expressions. Maintain natural conversation flow.
3. Understand what the user wants to say and respond appropriately.
4. Use clear, slightly simplified English suitable for language learners.
5. Keep responses natural and brief (1-3 sentences).
6. Answer user's questions specifically.

Initial greeting: {scenario_info['greeting']}

Let's begin the conversation!"""

    return prompt


def get_report_generation_prompt(language: Language, scenario: Scenario, conversation: str) -> str:
    """
    Generate prompt for report generation phase

    Args:
        language: Target language (japanese or english)
        scenario: Conversation scenario
        conversation: Full conversation text

    Returns:
        Analysis prompt string for report generation
    """
    if language == Language.JAPANESE:
        prompt = f"""以下は日本語学習者との会話記録です。詳細な分析レポートを作成してください。

【会話シナリオ】: {scenario.value}

【会話内容】:
{conversation}

【分析してください】:
1. **文法エラー**: 助詞の誤用、活用ミス、文法的な誤りを指摘し、正しい形を提示してください。
2. **語彙の問題**: 不適切な単語選択や、より適切な代替語を提案してください。
3. **表現の自然さ**: 不自然な表現や、よりネイティブらしい言い方を提案してください。
4. **良い点とフィードバック**: 上手に使えていた表現や、改善の方向性を肯定的に伝えてください。

【出力形式】:
必ずJSON形式で出力してください:
{{
  "overview": {{
    "language": "japanese",
    "scenario": "{scenario.value}",
    "turns": [会話のターン数],
    "word_count": [おおよその単語数]
  }},
  "grammar_errors": [
    {{
      "error": "誤った文や表現",
      "correction": "正しい形",
      "explanation": "なぜこれが間違いで、正しい形は何か",
      "error_type": "助詞/活用/語順 など"
    }}
  ],
  "vocabulary_issues": [
    {{
      "original": "使用された単語",
      "suggestion": "より適切な単語",
      "explanation": "なぜこの単語の方が良いか"
    }}
  ],
  "naturalness": [
    {{
      "unnatural": "不自然な表現",
      "natural": "より自然な表現",
      "context": "説明や文脈"
    }}
  ],
  "positive_feedback": [
    "良かった点や励ましのコメント"
  ]
}}

JSONのみを出力し、他の説明は含めないでください。"""

    else:  # English
        prompt = f"""Below is a conversation record with an English language learner. Please create a detailed analysis report.

【Conversation Scenario】: {scenario.value}

【Conversation Content】:
{conversation}

【Please analyze】:
1. **Grammar Errors**: Point out article usage, tense errors, and grammatical mistakes with corrections.
2. **Vocabulary Issues**: Identify inappropriate word choices and suggest better alternatives.
3. **Naturalness**: Point out unnatural expressions and suggest more native-like alternatives.
4. **Positive Feedback**: Highlight well-used expressions and provide encouraging improvement directions.

【Output Format】:
Must output in JSON format:
{{
  "overview": {{
    "language": "english",
    "scenario": "{scenario.value}",
    "turns": [number of conversation turns],
    "word_count": [approximate word count]
  }},
  "grammar_errors": [
    {{
      "error": "Incorrect sentence or expression",
      "correction": "Correct form",
      "explanation": "Why this is wrong and what the correct form is",
      "error_type": "article/tense/preposition etc."
    }}
  ],
  "vocabulary_issues": [
    {{
      "original": "Word used",
      "suggestion": "Better alternative",
      "explanation": "Why this word is better"
    }}
  ],
  "naturalness": [
    {{
      "unnatural": "Unnatural expression",
      "natural": "More natural expression",
      "context": "Explanation or context"
    }}
  ],
  "positive_feedback": [
    "Positive points and encouraging comments"
  ]
}}

Output only JSON, no other explanations."""

    return prompt
