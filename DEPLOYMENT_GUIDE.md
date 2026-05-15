# Deployment Guide - Render.com (Free)

## Prerequisites
- GitHub account
- Render.com account (free)

---

## Step 1: Update Your Info

1. Open `app/main.py`
2. Find the `/about` endpoint (line ~220)
3. Replace:
   - `"Your Name Here"` with your actual name
   - `"your.email@example.com"` with your actual email

---

## Step 2: Push to GitHub

### If you don't have Git initialized:

```bash
git init
git add .
git commit -m "Initial commit - Notes API"
```

### Create a new repository on GitHub:
1. Go to https://github.com/new
2. Name it: `notes-api`
3. Don't initialize with README (we already have files)
4. Click "Create repository"

### Push your code:
```bash
git remote add origin https://github.com/YOUR_USERNAME/notes-api.git
git branch -M main
git push -u origin main
```

---

## Step 3: Deploy on Render

### A. Sign up for Render
1. Go to https://render.com
2. Sign up with GitHub (easiest)

### B. Create PostgreSQL Database
1. Click "New +" → "PostgreSQL"
2. Name: `notes-db`
3. Database: `notesdb`
4. User: `notesuser`
5. Region: Choose closest to you
6. Plan: **Free**
7. Click "Create Database"
8. **Wait 2-3 minutes** for database to be ready
9. **Copy the "Internal Database URL"** (starts with `postgresql://`)

### C. Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository `notes-api`
3. Configure:
   - **Name**: `notes-api` (or your preferred name)
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: **Free**

4. **Add Environment Variables** (click "Advanced"):
   - `DATABASE_URL` = Paste the Internal Database URL from step B
   - `SECRET_KEY` = Generate one: run `python -c "import secrets; print(secrets.token_hex(32))"`
   - `ALGORITHM` = `HS256`
   - `ACCESS_TOKEN_EXPIRE_MINUTES` = `30`

5. Click "Create Web Service"

### D. Wait for Deployment
- First deployment takes 5-10 minutes
- Watch the logs for any errors
- When you see "Application startup complete", it's ready!

---

## Step 4: Test Your Deployed API

Your API will be at: `https://notes-api-XXXX.onrender.com`

### Test endpoints:
```bash
# Test root
curl https://your-app.onrender.com/

# Test about
curl https://your-app.onrender.com/about

# Test register
curl -X POST https://your-app.onrender.com/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

---

## Step 5: Submit Your URL

Submit the base URL to the assignment:
```
https://notes-api-XXXX.onrender.com
```

The automated tests will call:
- `https://notes-api-XXXX.onrender.com/about`
- `https://notes-api-XXXX.onrender.com/register`
- `https://notes-api-XXXX.onrender.com/login`
- etc.

---

## Troubleshooting

### Database Connection Issues
- Make sure you used the **Internal Database URL** (not External)
- Check that DATABASE_URL environment variable is set correctly
- Verify database is in "Available" status

### App Won't Start
- Check logs in Render dashboard
- Verify all environment variables are set
- Make sure requirements.txt has all dependencies

### 502 Bad Gateway
- App is still starting (wait 1-2 minutes)
- Check logs for errors

---

## Alternative: Railway.app

If Render doesn't work, try Railway:

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Python and PostgreSQL
6. Add environment variables in Settings
7. Deploy!

---

## Free Tier Limitations

**Render Free Tier:**
- App sleeps after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds
- 750 hours/month (enough for testing)

**Railway Free Tier:**
- $5 credit/month
- No sleep time
- Better for demos

---

## Need Help?

Common issues:
1. **Database not connecting**: Use Internal URL, not External
2. **Module not found**: Check requirements.txt has all packages
3. **Port error**: Make sure start command uses `$PORT`

Your API is ready to deploy! 🚀
