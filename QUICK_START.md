# Quick Start: GitHub → Vercel Deployment

## 🚀 Super Quick Version

### 1. Push to GitHub

```bash
# Initialize git (if not done)
git init
git add .
git commit -m "Initial commit"

# Create repo on GitHub.com, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### 2. Deploy to Vercel

1. Go to [vercel.com](https://vercel.com) → Sign up with GitHub
2. **Add New Project** → Import your repository
3. **Configure:**
   - Root Directory: `frontend` ⚠️ **IMPORTANT!**
   - Build Command: `npm run build` (auto-detected)
   - Output Directory: `dist` (auto-detected)
4. **Add Environment Variable:**
   - Name: `VITE_API_URL`
   - Value: Your backend URL (deploy backend first - see below)
5. Click **Deploy**

### 3. Deploy Backend (Railway - Free & Easy)

1. Go to [railway.app](https://railway.app) → Sign up with GitHub
2. **New Project** → Deploy from GitHub repo
3. Select your repo → **Add Service**
4. **Configure:**
   - Root Directory: `backend`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Copy the generated URL (e.g., `https://xxx.railway.app`)
6. **Update Vercel:** Go back to Vercel → Your Project → Settings → Environment Variables → Update `VITE_API_URL` with Railway URL

### 4. Configure Backend CORS

In Railway, add environment variable:
- Name: `ALLOWED_ORIGINS`
- Value: `https://your-frontend.vercel.app`

Or manually set in Railway dashboard → Your service → Variables

## ✅ Done!

Visit your Vercel URL - it should work!

For detailed instructions, see `GITHUB_VERCEL_SETUP.md`


