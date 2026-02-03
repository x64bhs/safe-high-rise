# Quick Deploy Guide

## TL;DR Version

1. **GitHub:** Push your code
2. **Railway:** Deploy backend → Get backend URL
3. **Vercel:** Deploy frontend (set Root = `frontend`, add `VITE_API_URL` = Railway URL)
4. **Railway:** Add `ALLOWED_ORIGINS` = Vercel URL

## Detailed Steps

### 1. Push to GitHub
```bash
git init && git add . && git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/REPO.git
git push -u origin main
```

### 2. Deploy Backend (Railway)
- Visit [railway.app](https://railway.app) → Login with GitHub
- New Project → Deploy from GitHub → Select repo
- Settings → Root Directory: `backend`
- Settings → Domains → Generate Domain
- **Copy the URL**

### 3. Deploy Frontend (Vercel)
- Visit [vercel.com](https://vercel.com) → Login with GitHub
- Add Project → Import repo
- **Root Directory:** `frontend`
- **Environment Variable:** `VITE_API_URL` = [Railway URL from step 2]
- Deploy

### 4. Fix CORS
- Railway → Variables → Add `ALLOWED_ORIGINS` = [Vercel URL]

**Done!** ✅


