# Phase 2 Setup Guide - Authentication & Database

## 🎉 Implementation Complete!

All Phase 2 code is ready. Follow these steps to set up and test.

---

## Prerequisites

You need PostgreSQL installed on your system.

### macOS
```bash
# Install PostgreSQL
brew install postgresql@14

# Start PostgreSQL service
brew services start postgresql@14
```

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### Windows
Download and install from: https://www.postgresql.org/download/windows/

---

## Database Setup

### 1. Create Database

```bash
# Connect to PostgreSQL
psql postgres

# In psql prompt, create database and user
CREATE DATABASE linguaecho;
CREATE USER linguaecho_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE linguaecho TO linguaecho_user;

# Exit psql
\q
```

### 2. Update Backend .env

The `.env` file has been updated with database settings. **Important: Change the SECRET_KEY in production!**

```bash
cd backend

# Generate a secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Update SECRET_KEY in .env with the generated value
```

Current `.env` settings (already configured):
```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost/linguaecho
SECRET_KEY=your-secret-key-change-in-production-use-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Run Database Migrations

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run migrations to create tables
python -m alembic upgrade head
```

You should see:
```
INFO  [alembic.runtime.migration] Running upgrade  -> 001, Initial migration: users, conversations, reports tables
```

---

## Start the Application

### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

Backend should start at: http://localhost:8000
API docs available at: http://localhost:8000/docs

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

Frontend should start at: http://localhost:5173

---

## Testing Phase 2 Features

### 1. Test Guest Mode (No Login)
- ✅ Open http://localhost:5173
- ✅ Start a conversation (Home → Select language/scenario)
- ✅ Chat with AI
- ✅ Generate report
- ✅ Check History page - should see localStorage data

### 2. Test User Registration
- ✅ Click "Register" in header
- ✅ Enter email and password
- ✅ Submit registration
- ✅ Should auto-login and redirect to home
- ✅ **Check**: localStorage conversations should migrate to database
- ✅ **Verify**: History page shows migrated conversations

### 3. Test Authenticated Mode
- ✅ Start a new conversation
- ✅ Chat with AI (data auto-saves to database)
- ✅ Generate report
- ✅ Check History - should fetch from database
- ✅ Delete a conversation - should remove from database

### 4. Test Login/Logout
- ✅ Click "Logout" in header
- ✅ Should return to guest mode
- ✅ History shows only localStorage data (if any)
- ✅ Click "Login"
- ✅ Enter credentials
- ✅ Should login and show database conversations

---

## Verify Database Tables

```bash
# Connect to database
psql linguaecho

# List tables
\dt

# Should show:
# users
# conversations
# reports

# Check users
SELECT id, email, created_at FROM users;

# Check conversations
SELECT id, user_id, language, scenario, created_at FROM conversations;

# Exit
\q
```

---

## API Endpoints

### Authentication Endpoints
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login with email/password
- `GET /api/auth/me` - Get current user info

### Conversation Endpoints
- `POST /api/migrate` - Migrate localStorage to database
- `GET /api/conversations` - Get user's conversations
- `GET /api/conversations/{session_id}` - Get specific conversation
- `DELETE /api/conversations/{conversation_id}` - Delete conversation

### Existing Endpoints (Now Dual-Mode)
- `POST /api/chat` - Works for guests AND authenticated users
- `POST /api/chat/stream` - SSE streaming with optional auth
- `POST /api/report/generate` - Auto-saves if authenticated

---

## Architecture Summary

### Dual-Mode Operation
- **Guest Mode**: No authentication, localStorage only
- **Authenticated Mode**: JWT tokens, PostgreSQL persistence
- **Seamless Transition**: Auto-migrates data on first login

### Authentication Flow
1. User registers/logs in → Receives JWT token
2. Token stored in localStorage
3. Axios automatically attaches token to all requests
4. Backend validates token for each request
5. If valid, saves data to database
6. If no token, works as guest

### Database Schema
```sql
-- Users
users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  hashed_password VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL
)

-- Conversations
conversations (
  id UUID PRIMARY KEY,
  user_id UUID FOREIGN KEY → users.id,
  session_id UUID UNIQUE NOT NULL,
  language VARCHAR(50) NOT NULL,
  scenario VARCHAR(100) NOT NULL,
  messages JSONB NOT NULL,
  created_at TIMESTAMP NOT NULL
)

-- Reports
reports (
  id UUID PRIMARY KEY,
  conversation_id UUID FOREIGN KEY → conversations.id,
  report_data JSONB NOT NULL,
  created_at TIMESTAMP NOT NULL
)
```

---

## Troubleshooting

### Backend won't start
```bash
# Check if all dependencies are installed
pip install -r requirements.txt

# Check if PostgreSQL is running
pg_isready

# Check database connection
psql linguaecho
```

### Alembic migration fails
```bash
# Check if database exists
psql -l | grep linguaecho

# If not, create it
createdb linguaecho

# Try migration again
alembic upgrade head
```

### Frontend auth not working
```bash
# Check browser console for errors
# Check if backend is running: http://localhost:8000/health
# Check if token is in localStorage: Application → Local Storage
```

### CORS errors
- Verify `CORS_ORIGINS` in backend `.env` includes frontend URL
- Default: `http://localhost:5173,http://localhost:3000`

---

## What's New in Phase 2

### Backend (21 new files)
- ✅ Database models and migrations
- ✅ JWT authentication system
- ✅ CRUD operations for users and conversations
- ✅ 7 new API endpoints
- ✅ Updated existing endpoints for dual-mode

### Frontend (6 new files)
- ✅ Auth service and Pinia store
- ✅ JWT interceptors (Axios + SSE)
- ✅ Login and Register components
- ✅ AppHeader with auth UI
- ✅ Updated history store for dual-mode
- ✅ Auto-migration logic

---

## Next Steps

1. **Test thoroughly** using the checklist above
2. **Change SECRET_KEY** to a secure random string
3. **Consider deploying** to production (Railway + Vercel)
4. **Add features** like email verification, password reset, etc.

---

## Security Notes

- 🔒 Passwords are hashed with bcrypt (never stored in plain text)
- 🔒 JWT tokens expire after 30 minutes
- 🔒 Optional authentication (guests can use without account)
- 🔒 CORS configured to prevent unauthorized access
- ⚠️ **IMPORTANT**: Change `SECRET_KEY` in production!

---

Enjoy your fully authenticated LinguaEcho! 🎉
