# LinguaEcho - Quick Start Guide

> **AI-Powered Language Learning Conversation Platform**
>
> Practice Japanese and English through realistic scenarios and get detailed AI feedback reports.

## 🚀 Project Status

**Current Phase:** MVP Development - Core features implemented, ready for testing

### Completed ✅
- ✅ Backend API with FastAPI + LangChain
- ✅ Frontend UI with Vue 3 + Naive UI
- ✅ 10 conversation scenarios (Restaurant, Hotel, Shopping, etc.)
- ✅ Chat and Report generation endpoints
- ✅ LocalStorage persistence for conversation history
- ✅ Full routing and state management setup

### Next Steps 🎯
- [ ] Test backend server startup
- [ ] Test frontend development server
- [ ] Verify API connectivity
- [ ] Test conversation flow with LLM
- [ ] Test report generation
- [ ] Deploy to production (Vercel + Railway)

---

## 📋 Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.10+
- **API Key** for OpenRouter or Groq (free tier available)

---

## ⚡ Quick Start

### 1️⃣ Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your API key:
# OPENROUTER_API_KEY=your_key_here
# or
# GROQ_API_KEY=your_key_here

# Start development server
uvicorn app.main:app --reload

# Server runs at: http://localhost:8000
# API docs at: http://localhost:8000/docs
```

### 2️⃣ Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.template .env
# Edit .env if needed (default backend URL: http://localhost:8000)

# Start development server
npm run dev

# Server runs at: http://localhost:5173
```

### 3️⃣ Open Browser

Navigate to `http://localhost:5173` and start practicing! 🎉

---

## 🔑 Getting API Keys (Free)

### Option 1: OpenRouter (Recommended)
1. Visit https://openrouter.ai/
2. Sign up for free account
3. Go to Keys section and create new API key
4. Model used: `google/gemini-2.0-flash-exp:free` (completely free)

### Option 2: Groq
1. Visit https://console.groq.com/
2. Sign up for free account
3. Generate API key
4. Model used: `llama-3.1-8b-instant` (free tier)

---

## 📁 Project Structure

```
LinguaEcho/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints (chat, report)
│   │   ├── models/         # Pydantic request/response models
│   │   ├── services/       # Business logic (LLM service)
│   │   ├── langchain/      # LangChain prompts and integration
│   │   ├── config.py       # Configuration
│   │   └── main.py         # FastAPI app entry
│   └── requirements.txt
│
├── frontend/               # Vue 3 frontend
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── views/         # Page views (Home, Conversation, Report, History)
│   │   ├── stores/        # Pinia stores
│   │   ├── router/        # Vue Router
│   │   ├── services/      # API service layer
│   │   └── utils/         # Utilities (localStorage wrapper)
│   └── package.json
│
└── README.md              # Product Requirements (Chinese)
```

---

## 🎨 Features

### 10 Practice Scenarios

**Daily Life:**
- 🍜 Restaurant ordering
- 🏨 Hotel check-in
- 🛒 Supermarket shopping
- 🚇 Directions/Transportation

**Social:**
- 👋 Self-introduction
- ☕ Casual chat
- 📞 Phone appointment

**Professional:**
- 💼 Job interview
- 📧 Business email
- 🎓 Classroom discussion

### Conversation Flow
1. Select language (Japanese/English)
2. Choose scenario
3. Chat with AI naturally (10-15 turns)
4. End conversation and get detailed report

### Report Includes
- Grammar error analysis
- Vocabulary suggestions
- Naturalness feedback
- Positive reinforcement
- Improvement tips

---

## 🔧 Useful Commands

### Backend
```bash
# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn app.main:app --reload

# Run on custom port
uvicorn app.main:app --reload --port 8080

# View API documentation
open http://localhost:8000/docs
```

### Frontend
```bash
# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

---

## 🧪 Testing the API

### Test Chat Endpoint
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-123",
    "language": "japanese",
    "scenario": "restaurant",
    "message": "すみません、メニューをください",
    "history": []
  }'
```

### Test Report Generation
```bash
curl -X POST http://localhost:8000/api/report/generate \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-123",
    "language": "japanese",
    "scenario": "restaurant",
    "conversation": [
      {"role": "user", "content": "すみません、メニューをください"},
      {"role": "assistant", "content": "はい、こちらがメニューでございます"}
    ]
  }'
```

---

## 🚢 Deployment

### Frontend (Vercel)
```bash
cd frontend
npm run build
vercel --prod
```

### Backend (Railway)
1. Connect GitHub repo to Railway
2. Add environment variables (OPENROUTER_API_KEY)
3. Deploy automatically on git push

---

## 📚 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vue 3, Naive UI, Pinia, Vue Router, Axios |
| Backend | FastAPI, LangChain, Pydantic |
| LLM | OpenRouter (Gemini 2.0 Flash) / Groq (Llama 3.1) |
| Storage | LocalStorage (Phase 1), PostgreSQL (Phase 2) |
| Deployment | Vercel + Railway |

---

## 🛟 Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.10+)
- Check .env file exists with API key
- Try: `pip install --upgrade -r requirements.txt`

### Frontend won't start
- Check Node version: `node --version` (need 18+)
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- Check port 5173 is not in use

### API connection error
- Verify backend is running on http://localhost:8000
- Check frontend .env has correct VITE_API_BASE_URL
- Check CORS is enabled in backend

### LLM not responding
- Verify API key is correct in backend .env
- Check OpenRouter/Groq dashboard for rate limits
- Try switching to alternative LLM provider

---

## 📖 Full Documentation

- [Product Requirements (Chinese)](README.md)
- [Development Guidelines (CLAUDE.md)](CLAUDE.md)

---

## 📝 License

MIT License - Feel free to use for learning and portfolio purposes!

---

**Happy Language Learning! 📚✨**
