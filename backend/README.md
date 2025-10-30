# LinguaEcho Backend

FastAPI backend for LinguaEcho language learning platform.

## Setup

### 1. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Copy `.env.template` to `.env` and add your API keys:

```bash
cp .env.template .env
```

Edit `.env` and add your OpenRouter or Groq API key.

### 4. Run development server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## API Endpoints

- `POST /api/chat` - Conversation endpoint
- `POST /api/report/generate` - Report generation endpoint
- `GET /health` - Health check
