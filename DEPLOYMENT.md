# LinguaEcho Deployment Guide

Complete guide for deploying LinguaEcho to production using Railway (backend) and Vercel (frontend).

## Prerequisites

- GitHub account with LinguaEcho repository
- Google AI Studio API key (from https://aistudio.google.com/app/apikey)
- Git repository pushed to GitHub

---

## Deployment Overview

**Stack:**
- Backend: Railway (FastAPI + LangChain)
- Frontend: Vercel (Vue 3 + Vite)
- LLM: Google AI Studio (Gemini)

**Timeline:** ~30-45 minutes total

---

## Phase 1: Backend Deployment (Railway)

### Step 1: Create Railway Account

1. Go to https://railway.app
2. Click "Start a New Project"
3. Sign up with GitHub
4. Authorize Railway to access your repositories

### Step 2: Deploy from GitHub

1. In Railway dashboard, click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your "LinguaEcho" repository
4. Railway will detect the project structure

### Step 3: Configure Service

1. Railway should auto-detect Python app
2. Set root directory: `backend`
3. Railway will use the `Procfile` to start the server

### Step 4: Set Environment Variables

In Railway project dashboard → Variables tab, add:

```bash
# Required
LLM_PROVIDER=google
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_MODEL=gemini-2.0-flash-exp

# CORS - Add localhost for testing, will update later with Vercel URL
CORS_ORIGINS=http://localhost:5173

# Optional
RATE_LIMIT_PER_HOUR=100
```

### Step 5: Deploy

1. Railway automatically deploys after adding environment variables
2. Wait 2-3 minutes for build to complete
3. Check deployment logs for any errors
4. Once deployed, Railway provides a URL like: `https://linguaecho-production.up.railway.app`

### Step 6: Verify Backend

Test your deployed backend:

```bash
# Health check
curl https://your-railway-url.railway.app/health

# Should return: {"status":"healthy"}

# API documentation
# Open in browser: https://your-railway-url.railway.app/docs
```

**Save your Railway backend URL - you'll need it for frontend deployment!**

---

## Phase 2: Frontend Deployment (Vercel)

### Step 1: Create Vercel Account

1. Go to https://vercel.com
2. Click "Sign Up"
3. Sign up with GitHub
4. Authorize Vercel to access your repositories

### Step 2: Import Project

1. In Vercel dashboard, click "Add New" → "Project"
2. Select your "LinguaEcho" GitHub repository
3. Vercel auto-detects it as a Vite project

### Step 3: Configure Build Settings

Vercel should auto-detect:
- **Framework Preset:** Vite
- **Root Directory:** `frontend`
- **Build Command:** `npm run build`
- **Output Directory:** `dist`

If not auto-detected, manually set:
- **Root Directory:** `frontend`
- **Build Command:** `npm install && npm run build`
- **Output Directory:** `dist`

### Step 4: Set Environment Variable

In the configuration screen, add environment variable:

**Name:** `VITE_API_BASE_URL`
**Value:** `https://your-railway-url.railway.app` (your Railway backend URL from Phase 1)

### Step 5: Deploy

1. Click "Deploy"
2. Wait 1-2 minutes for build
3. Vercel provides a URL like: `https://lingua-echo.vercel.app`

### Step 6: Verify Frontend

1. Open your Vercel URL in browser
2. Check browser console for errors (F12 → Console)
3. Should see the LinguaEcho home page with language selection

---

## Phase 3: Connect Frontend to Backend (CORS)

### Update Backend CORS Configuration

1. Go back to Railway dashboard
2. Navigate to your project → Variables
3. Update `CORS_ORIGINS` to include your Vercel URL:

```bash
CORS_ORIGINS=http://localhost:5173,https://lingua-echo.vercel.app
```

**Important:** Replace `lingua-echo.vercel.app` with your actual Vercel URL

4. Railway will auto-redeploy with new CORS settings (30-60 seconds)

---

## Phase 4: Test End-to-End

### Functional Testing

1. Open your Vercel URL
2. Select a language (Japanese or English)
3. Select a scenario (e.g., Restaurant)
4. Click "Start Conversation"
5. Send a test message
6. Verify AI responds correctly
7. Click "End Conversation"
8. Verify report generates properly
9. Check History page shows saved conversation

### Debug if Issues

**Frontend can't reach backend:**
- Check browser Console (F12) for CORS errors
- Verify `VITE_API_BASE_URL` is set in Vercel
- Check Network tab for failed requests

**Backend not responding:**
- Check Railway deployment logs
- Verify environment variables are set correctly
- Test backend health endpoint: `curl https://your-url/health`

**API rate limits:**
- Check Google AI Studio dashboard for quota
- Increase `RATE_LIMIT_PER_HOUR` if needed

---

## Post-Deployment Operations

### How to Update Code

**Automatic Deployment:**

Both Railway and Vercel auto-deploy when you push to GitHub:

```bash
# Make changes to your code
git add .
git commit -m "feat: Update feature"
git push origin master

# Railway and Vercel automatically detect push and redeploy
# Check their dashboards for deployment status
```

### View Logs

**Railway Logs:**
1. Dashboard → Your Project → Deployments
2. Click latest deployment
3. View real-time logs

**Vercel Logs:**
1. Dashboard → Your Project → Deployments
2. Click latest deployment
3. View build and function logs

### Monitor Usage

**Railway:**
- Dashboard → Usage
- Shows: CPU, Memory, Network, Build time
- Free tier: 500 hours/month

**Vercel:**
- Dashboard → Usage
- Shows: Bandwidth, Functions, Build time
- Free tier: Generous limits for hobby projects

**Google AI Studio:**
- Visit https://aistudio.google.com
- Manage API Keys section
- View request counts and rate limits

### Custom Domain (Optional)

**Vercel Custom Domain:**
1. Dashboard → Your Project → Settings → Domains
2. Add your domain
3. Configure DNS records as instructed
4. Update Railway CORS to include custom domain

**Railway Custom Domain:**
1. Dashboard → Your Project → Settings
2. Add custom domain
3. Configure DNS
4. Update Vercel `VITE_API_BASE_URL`

---

## Troubleshooting

### Issue: CORS Errors in Browser Console

```
Access to XMLHttpRequest has been blocked by CORS policy
```

**Solution:**
1. Check Railway environment variable `CORS_ORIGINS`
2. Ensure it includes exact Vercel URL: `https://your-project.vercel.app`
3. No trailing slashes
4. Redeploy backend after CORS change

### Issue: 404 on Backend Routes

**Solution:**
1. Verify Procfile exists: `backend/Procfile`
2. Check Railway logs for startup errors
3. Ensure `main.py` is in `backend/` directory
4. Verify Railway root directory is set to `backend`

### Issue: Frontend Build Fails on Vercel

**Solution:**
1. Check Vercel build logs
2. Ensure `package.json` exists in `frontend/`
3. Verify root directory is set to `frontend`
4. Check for dependency version conflicts

### Issue: API Timeout Errors

**Solution:**
1. Google AI Studio may have rate limits
2. Check Railway resource usage (may need upgrade)
3. Increase timeout in `frontend/src/services/api.js` if needed

### Issue: Environment Variables Not Working

**Solution:**
- Railway: Variables take effect immediately, but need redeploy
- Vercel: Must redeploy after adding variables
- Check variable names are exact (case-sensitive)
- VITE_ prefix required for Vite variables

---

## Rollback Procedure

If deployment breaks:

**Railway:**
1. Dashboard → Deployments
2. Find previous working deployment
3. Click "Redeploy"

**Vercel:**
1. Dashboard → Deployments
2. Find previous working deployment
3. Click "..." → "Promote to Production"

---

## Cost Estimates

**Free Tier (sufficient for MVP):**
- Railway: 500 hours/month = ~$0
- Vercel: Unlimited deployments = $0
- Google AI Studio: 60 RPM = $0
- **Total: $0/month**

**After Free Tier:**
- Railway: ~$0.50/hour after 500 hrs
- Vercel: Still free for most hobby projects
- Google AI Studio: Pay per use after quota

**Estimated cost at scale:** $10-50/month depending on usage

---

## Security Checklist

- [ ] API keys stored in platform environment variables (not in code)
- [ ] `.env` files in `.gitignore`
- [ ] CORS restricted to specific domains (not `*`)
- [ ] Rate limiting enabled
- [ ] HTTPS enabled (automatic on Railway/Vercel)
- [ ] Secrets never committed to Git

---

## Next Steps

After successful deployment:

1. **Share your app!** Your frontend URL is public and ready to use
2. **Monitor usage:** Check Railway and Vercel dashboards regularly
3. **Implement Phase 2:** Add PostgreSQL for persistent storage (see CLAUDE.md)
4. **Custom domain:** Configure custom domains for professional look
5. **Analytics:** Add Google Analytics or Vercel Analytics

---

## Support

- Railway Docs: https://docs.railway.app
- Vercel Docs: https://vercel.com/docs
- Google AI Studio: https://ai.google.dev/docs

---

**Congratulations! Your LinguaEcho app is now live! 🎉**

Your app is accessible at:
- Frontend: `https://your-project.vercel.app`
- Backend: `https://your-project.railway.app`
- API Docs: `https://your-project.railway.app/docs`
