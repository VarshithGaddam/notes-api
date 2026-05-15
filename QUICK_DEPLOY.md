# Quick Deploy Guide (5 Minutes)

## 1. Update Your Info (30 seconds)
Open `app/main.py` and update line ~220:
```python
"name": "Your Actual Name",
"email": "your.actual@email.com",
```

## 2. Generate Secret Key (10 seconds)
Run this command and copy the output:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## 3. Push to GitHub (2 minutes)

```bash
# Initialize git (if not done)
git init
git add .
git commit -m "Notes API ready for deployment"

# Create repo on GitHub: https://github.com/new
# Name it: notes-api

# Push code
git remote add origin https://github.com/YOUR_USERNAME/notes-api.git
git branch -M main
git push -u origin main
```

## 4. Deploy on Render (2 minutes)

### Option A: One-Click Deploy (Easiest)
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Blueprint"
4. Connect your `notes-api` repository
5. Render will read `render.yaml` and set everything up automatically!
6. Wait 5 minutes for deployment

### Option B: Manual Setup
1. Go to https://render.com
2. Sign up with GitHub
3. Create PostgreSQL Database:
   - Click "New +" → "PostgreSQL"
   - Name: `notes-db`, Plan: Free
   - Copy "Internal Database URL"
4. Create Web Service:
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Add Environment Variables:
     - `DATABASE_URL` = (paste Internal Database URL)
     - `SECRET_KEY` = (paste generated key from step 2)
     - `ALGORITHM` = `HS256`
     - `ACCESS_TOKEN_EXPIRE_MINUTES` = `30`
5. Click "Create Web Service"

## 5. Test Your API (30 seconds)

Your URL: `https://notes-api-XXXX.onrender.com`

Test in browser:
- https://your-url.onrender.com/
- https://your-url.onrender.com/about
- https://your-url.onrender.com/docs

## 6. Submit URL

Submit your base URL:
```
https://notes-api-XXXX.onrender.com
```

Done! 🎉

---

## Troubleshooting

**App not starting?**
- Check logs in Render dashboard
- Verify DATABASE_URL uses "Internal" URL
- Make sure all environment variables are set

**First request slow?**
- Free tier sleeps after 15 min inactivity
- First request takes 30-60 seconds to wake up
- This is normal for free tier

**Need faster deployment?**
Try Railway.app - same steps but no sleep time!
