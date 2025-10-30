/**
 * Constants for languages and scenarios
 */

export const LANGUAGES = {
  JAPANESE: 'japanese',
  ENGLISH: 'english'
}

export const LANGUAGE_LABELS = {
  [LANGUAGES.JAPANESE]: '日本語 (Japanese)',
  [LANGUAGES.ENGLISH]: 'English'
}

export const SCENARIOS = {
  // Daily Life
  RESTAURANT: 'restaurant',
  HOTEL: 'hotel',
  SUPERMARKET: 'supermarket',
  TRANSPORTATION: 'transportation',

  // Social
  SELF_INTRO: 'self_intro',
  CASUAL_CHAT: 'casual_chat',
  PHONE_APPOINTMENT: 'phone_appointment',

  // Professional/Academic
  JOB_INTERVIEW: 'job_interview',
  BUSINESS_EMAIL: 'business_email',
  CLASSROOM: 'classroom'
}

export const SCENARIO_INFO = {
  // Daily Life
  [SCENARIOS.RESTAURANT]: {
    title: {
      japanese: 'レストラン注文',
      english: 'Restaurant Ordering'
    },
    description: {
      japanese: 'レストランでの注文、メニューについて質問',
      english: 'Ordering food and asking about menu items'
    },
    category: 'daily'
  },
  [SCENARIOS.HOTEL]: {
    title: {
      japanese: 'ホテルチェックイン',
      english: 'Hotel Check-in'
    },
    description: {
      japanese: 'チェックイン手続き、施設について質問',
      english: 'Check-in procedures and facility inquiries'
    },
    category: 'daily'
  },
  [SCENARIOS.SUPERMARKET]: {
    title: {
      japanese: 'スーパー買い物',
      english: 'Supermarket Shopping'
    },
    description: {
      japanese: '商品を探す、価格やプロモーションについて質問',
      english: 'Finding products and asking about prices'
    },
    category: 'daily'
  },
  [SCENARIOS.TRANSPORTATION]: {
    title: {
      japanese: '道案内・交通',
      english: 'Directions/Transportation'
    },
    description: {
      japanese: '道を尋ねる、切符を買う',
      english: 'Asking for directions and buying tickets'
    },
    category: 'daily'
  },

  // Social
  [SCENARIOS.SELF_INTRO]: {
    title: {
      japanese: '自己紹介',
      english: 'Self-introduction'
    },
    description: {
      japanese: '初対面での自己紹介、背景や興味の紹介',
      english: 'Introducing yourself and sharing background'
    },
    category: 'social'
  },
  [SCENARIOS.CASUAL_CHAT]: {
    title: {
      japanese: '気楽な会話',
      english: 'Casual Chat'
    },
    description: {
      japanese: '天気や週末の予定などについて友達と話す',
      english: 'Chatting with friends about weather and plans'
    },
    category: 'social'
  },
  [SCENARIOS.PHONE_APPOINTMENT]: {
    title: {
      japanese: '電話予約',
      english: 'Phone Appointment'
    },
    description: {
      japanese: '電話で病院や美容院の予約',
      english: 'Making appointments by phone'
    },
    category: 'social'
  },

  // Professional/Academic
  [SCENARIOS.JOB_INTERVIEW]: {
    title: {
      japanese: '就職面接',
      english: 'Job Interview'
    },
    description: {
      japanese: '面接官の質問に答える、能力をアピール',
      english: 'Answering interview questions and showcasing skills'
    },
    category: 'professional'
  },
  [SCENARIOS.BUSINESS_EMAIL]: {
    title: {
      japanese: 'ビジネスメール',
      english: 'Business Email'
    },
    description: {
      japanese: 'フォーマルなビジネスメールの書き方を学ぶ',
      english: 'Learning to write formal business emails'
    },
    category: 'professional'
  },
  [SCENARIOS.CLASSROOM]: {
    title: {
      japanese: '教室ディスカッション',
      english: 'Classroom Discussion'
    },
    description: {
      japanese: '学術的な環境で意見を表現し質問する',
      english: 'Expressing opinions and asking questions in class'
    },
    category: 'professional'
  }
}

export const CATEGORY_LABELS = {
  daily: {
    japanese: '日常生活',
    english: 'Daily Life'
  },
  social: {
    japanese: '社交',
    english: 'Social'
  },
  professional: {
    japanese: '仕事・学問',
    english: 'Professional/Academic'
  }
}
